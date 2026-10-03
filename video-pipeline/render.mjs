// Render stage.html frame-by-frame and pipe PNGs into ffmpeg.
// usage: node render.mjs out.mp4 [t0 t1]   |   node render.mjs --stills 1.0,12.3,...
import { spawn } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
// Uses the globally installed Playwright (cloud sessions ship it under /opt/node-tools).
const require = createRequire(process.env.PLAYWRIGHT_DIR || '/opt/node-tools/node_modules/');
const { chromium } = require('playwright');

const data = JSON.parse(readFileSync('work/data.json', 'utf8'));
const browser = await chromium.launch({ args: ['--allow-file-access-from-files', '--font-render-hinting=none'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto('file://' + process.cwd() + '/stage.html');
await page.evaluate(d => window.setup(d), data);

const args = process.argv.slice(2);
if (args[0] === '--stills') {
  for (const t of args[1].split(',').map(Number)) {
    await page.evaluate(t => window.render(t), t);
    await page.screenshot({ path: `work/still_${t.toFixed(2)}.png` });
  }
  await browser.close();
  process.exit(0);
}

const out = args[0], fps = 30;
const t0 = Number(args[1] ?? 0), t1 = Number(args[2] ?? data.duration);
const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
  '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const n = Math.round((t1 - t0) * fps);
const start = Date.now();
for (let f = 0; f < n; f++) {
  const t = t0 + f / fps;
  await page.evaluate(t => window.render(t), t);
  const buf = await page.screenshot({ type: 'png' });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (f % 150 === 0) console.log(`frame ${f}/${n}  t=${t.toFixed(1)}s  ${((Date.now() - start) / 1000).toFixed(0)}s elapsed`);
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
await browser.close();
console.log('done', out);
