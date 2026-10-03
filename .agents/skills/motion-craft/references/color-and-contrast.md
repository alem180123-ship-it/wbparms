# Color and contrast

Color carries meaning before it carries style. This reference covers palette
construction, contrast measurement, gamut, and how color is deployed in an
interface.

**Respect the project's existing color system.** Do not convert notation merely
because this reference was loaded. A consistent hex or RGB token system is better
than a second color representation introduced for one isolated fix. Convert only
when the user asks, when the project is already standardizing on OKLCH, or when
an agreed migration is in scope.

Whether contrast is required and how severe a failure is belongs to
`references/accessibility-contract.md`. This file owns measuring the rendered
pair and changing its values.

## Why a perceptual space

OKLCH separates lightness, chroma, and hue into controls that behave the way a
designer expects:

- **Perceptual uniformity.** Equal L steps read as equal brightness steps.
  HSL's `lightness: 50%` varies wildly by hue.
- **Stable hue.** An HSL blue drifts toward purple as it lightens — a `240°` ramp
  can shift ~18° across its range. OKLCH hue holds constant.
- **Independent chroma.** Chroma is an absolute measure of colorfulness that does
  not depend on lightness. HSL saturation does.
- **Finite gamut.** Not every OKLCH value is displayable; high chroma clips at
  certain hues. Gamut awareness is required, not optional.

```text
oklch(L C H)
oklch(L C H / alpha)
```

| Channel | Range | Meaning |
| --- | --- | --- |
| L — lightness | `0`–`1` | `0` black, `1` white; perceptually uniform |
| C — chroma | `0`–~`0.4` | Colorfulness; `0` is gray. Maximum depends on L and H |
| H — hue | `0`–`360` | Hue angle in degrees |
| alpha | `0`–`1` | Optional, slash syntax — never a comma |

Format with three decimals for L and C, up to three for H. Drop trailing zeros
and write `-0` as `0`.

## Building a palette

Design-system scales run `50` (lightest) to `950` (darkest):

| Steps | Labels |
| --- | --- |
| 5 | 100, 300, 500, 700, 900 |
| 9 | 50, 100, 200, 300, 500, 700, 800, 900, 950 |
| 11 | 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950 |

From a base color with lightness `L`, a chroma percentage, and hue `H`:

1. **Bound lightness.** `delta = 0.4`; `minL = max(0.05, L - delta)`;
   `maxL = min(0.95, L + delta)`. Clamping to `[0.05, 0.95]` avoids pure black and
   white, which carry zero chroma.
2. **Distribute lightness evenly** from `maxL` (step 50) to `minL` (step 950).
3. **Clamp chroma per step** against the maximum chroma available for that
   lightness and hue in the target space:
   `C = (chromaPercentage / 100) × maxChroma(L, H, space)`.

High-chroma base colors legitimately lose chroma at both ends of the scale.

**Across multiple hues, hold lightness and chroma *percentage* constant, not
absolute chroma.** Equal L guarantees equal perceived brightness; equal C% of
each hue's own maximum guarantees equal vividness. Identical absolute C values
make some hues look far more vivid than others.

```css
/* Same L, same 80% of each hue's max chroma — different absolute C */
--blue-500:  oklch(0.623 0.141 250);
--green-500: oklch(0.623 0.157 145);
--red-500:   oklch(0.623 0.202 25);
```

**Dark mode is not a mechanical reversal.** Start by swapping the semantic role
mappings, then tune chroma and lightness for the dark appearance and recheck every
foreground/background pair. Equal OKLCH steps do not guarantee a pair preserves
its contrast when inverted.

## Gamut

Every sRGB color exists in Display P3; the reverse is not true — P3 covers roughly
50% more colors.

Maximum chroma is irregular across the gamut. At `L = 0.5` in sRGB:

- purple (`H ≈ 285`) peaks around `C ≈ 0.29`;
- red-orange (`H ≈ 0–30`) around `C ≈ 0.20`;
- cyan (`H ≈ 195`) is lowest, around `C ≈ 0.09`.

The peak hue moves with lightness — magenta peaks near `L = 0.7`, green near
`L = 0.9`. Cyan is consistently the most constrained.

If chroma exceeds the maximum for its L/H/space, the color clips. Reduce chroma
while holding L and H constant.

```css
.accent { color: oklch(0.7 0.2 150); }              /* sRGB-safe */

@media (color-gamut: p3) {
  .accent { color: oklch(0.7 0.3 150); }            /* P3 enhancement */
}
```

When support requirements are unusually broad, wrap in `@supports (color: oklch(0 0 0))`
with a hex fallback rather than relying on a remembered global-coverage figure —
check the project's actual browser matrix.

In Tailwind v4, custom scales belong in `@theme` in OKLCH, matching the framework's
own default palette. The `/50` opacity modifier compiles to slash-syntax alpha
automatically.

## Measuring contrast

Contrast is always between a **foreground** (text, icon, or UI element) and the
**background it is actually rendered against** — normally the nearest ancestor
with a background.

**Report, do not repaint.** When a pair fails, report the pair, its measured
value, and the threshold it misses. A project's colors are a design decision;
change them only when asked.

### APCA (default)

APCA is more perceptually accurate than WCAG 2 and pairs naturally with OKLCH,
since both are grounded in perceptual lightness. Lc is signed — positive means
dark-on-light, negative light-on-dark; compare absolute values.

| Content | Minimum | Preferred |
| --- | --- | --- |
| Body text (columns or blocks) | Lc 75 | Lc 90 |
| Non-body text (labels, headlines) | Lc 60 | Lc 75 |
| Large text (≥36px) | Lc 45 | Lc 60 |
| UI components | Lc 30 | — |

Lc 30 is also the floor for disabled and placeholder text. Lc 15 is the absolute
threshold for a non-text element to be discernible at all.

### WCAG 2 (for formal conformance claims)

| Content | AA | AAA |
| --- | --- | --- |
| Normal text (<24px, or <18.5px bold) | 4.5:1 | 7:1 |
| Large text (≥24px, or ≥18.5px bold) | 3:1 | 4.5:1 |
| UI components and graphical objects | 3:1 | — |

WCAG defines large text in points: 18pt ≈ `24px`, 14pt bold ≈ `18.5px`.

### Quick reference

| Rule | Value |
| --- | --- |
| Light/dark text crossover | Background `L > 0.73` → dark text; at or below, light text scores higher |
| Lightness gap, light background | Background `L > 0.9` → foreground `L < 0.35` |
| Lightness gap, dark background | Background `L < 0.25` → foreground `L > 0.9` |
| Hue drift threshold | More than 10° spread across palette steps is visible drift |
| Mid-lightness ceiling | On a background near `L 0.75`, even pure black text reaches only ~Lc 60 |

The crossover sits higher than intuition suggests: between `L 0.6` and `L 0.73`
a background already looks light, but white text still scores meaningfully higher
than black. The light/dark gaps are asymmetric because APCA is polarity-aware —
mirrored pairs do not score identically. Always verify with a real calculation.

### Fixing contrast (only on request)

Adjust **L first**, preserving C and H where possible, then remeasure the rendered
pair. Reduce C only as far as gamut requires.

```css
/* Failing — foreground too close in lightness (Lc ≈ 50) */
color: oklch(0.65 0.08 250);
background: oklch(0.95 0.02 250);

/* Fixed — darken the foreground, C and H unchanged (Lc ≈ 90) */
color: oklch(0.30 0.08 250);
background: oklch(0.95 0.02 250);
```

Body text needs a background near one of the lightness extremes; a mid-lightness
surface caps the achievable contrast no matter what the foreground does.

## Using color in an interface

**One color, one meaning.** A hue used for interactive text (and anything within
±15° of it) must not also appear on non-interactive text — it tells users to click
something that is not clickable.

**Semantic tokens, used only in their role.** Name by role, not appearance, and
never borrow a token because its value happens to look right today:

```css
:root {
  --color-text-primary:   oklch(0.210 0.006 285.9);
  --color-text-secondary: oklch(0.552 0.016 285.9);
  --color-separator:      oklch(0.920 0.004 286.3);
  --color-surface:        oklch(1 0 0);
}
```

Using `--color-separator` as a caption color, or `--color-text-secondary` as a
background, breaks every future theme change that assumes the role. If a role has
no token, add one.

**One colored action per decision context.** Where filled color encodes primary
emphasis, exactly one primary action gets it and peer actions stay neutral. Put
the color on the background, not the label — a filled button reads as primary
from across the room, while colored label text on a neutral button reads as a
link. Multiple colored backgrounds are fine when they encode distinct states or
categories rather than competing as peer actions. Selected states (an active tab,
a checked segment) may use the accent on the glyph and label: that is state, not
emphasis.

**Never encode state through color alone.** Every status needs a redundant cue —
an icon, text, or an underline.

**Color meaning is not universal.** If a color is load-bearing for finance,
status, or alerts, verify the reading holds in every locale you ship to.

| Color | Common Western reading | Elsewhere |
| --- | --- | --- |
| Red | Danger, loss, error | Luck, prosperity; **gains** in Chinese financial UIs |
| Green | Success, gains | Losses in Chinese financial UIs |
| White | Purity, cleanliness | Mourning in parts of East Asia |
| Gold | Premium, luxury | Religious significance in some regions |

Where this applies, make the gain/loss colors a per-locale token, not a hardcoded
value.

## Appearance variants

Every custom color needs a light and a dark variant. Users who enable increased
contrast expect visibly stronger differentiation:

```css
:root { --color-accent: oklch(0.623 0.188 259.8); }

@media (prefers-color-scheme: dark) {
  :root { --color-accent: oklch(0.707 0.165 254.6); }
}

@media (prefers-contrast: more) {
  :root { --color-accent: oklch(0.488 0.243 264.4); }
}
```

The increased-contrast variant widens the foreground/background lightness gap by
at least `0.15` L over the default, then re-verifies against the preferred APCA
thresholds.

Two testing rules that catch most real failures:

- **Recheck every pair in both appearances.** A pair that passes in light mode can
  fail in dark mode; the palettes are not mirror images.
- **Account for translucency.** A color on a `backdrop-filter` surface or an
  overlay shifts with whatever scrolls behind it. Test it over the lightest and
  darkest content it can sit on, or make the surface opaque enough that the shift
  cannot break contrast.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Raw color bypasses the token system | Use or add the correct role token in the project's notation |
| Isolated OKLCH value in a hex codebase | Preserve the established notation unless migrating |
| HSL ramp with hue drift | Rebuild at constant OKLCH hue |
| Same absolute chroma across hues | Same chroma *percentage* of each hue's maximum |
| High chroma with no gamut check | Clamp to max chroma for that L and H |
| P3 color with no sRGB fallback | Add the fallback before `@media (color-gamut: p3)` |
| Dark mode by mechanically inverting the palette | Swap roles, then tune and recheck every pair |
| Alpha written with commas | Slash syntax: `oklch(L C H / alpha)` |
| One hue means two different things | One color, one meaning; give the second use a neutral |
| Token used outside its role | Add a token for the missing role |
| Several colored control backgrounds in one view | Fill only the primary action |
| Status communicated by color alone | Add an icon, label, or underline |
| Palette verified only in light mode | Verify both appearances, and over translucent surfaces |
| Contrast "fixed" by changing hue and chroma | Adjust L first, preserve C and H, then remeasure |
