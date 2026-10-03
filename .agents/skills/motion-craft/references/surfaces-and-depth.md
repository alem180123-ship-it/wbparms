# Surfaces and depth

Radius, optical alignment, elevation, materials, gradients, icons, and images.
These are the details users never consciously notice — which is the point. Their
aggregate is what separates an interface that feels considered from one that
feels assembled.

Apply this layer only after structure, states, and accessibility are sound.
Polish cannot compensate for an unresolved earlier layer.

## Concentric border radius

When rounded surfaces nest closely:

```text
outerRadius = innerRadius + padding
```

Mismatched radii on closely nested surfaces is the single most common source of
"something feels off" that nobody can name. Equal radii on both layers make the
inner surface look pinched.

```css
/* Correct */
.card       { border-radius: 20px; padding: 8px; }   /* 12 + 8 */
.card-inner { border-radius: 12px; }
```

**Escape condition:** when padding exceeds ~`24px`, or the layers are
independent rather than sharing a visible even inset, treat them as separate
surfaces and choose each radius on its own. Preserve an established component
token rather than forcing the math onto layers it was not meant for.

## Optical alignment

When geometric centering looks wrong, align optically. Geometry is a starting
point, not the answer.

- **Buttons with a trailing icon.** Equal padding makes the icon look pushed out.
  Start at `icon-side padding = text-side padding − 2px`.
- **Play triangles.** A triangle's geometric center is not its visual center.
  Shift roughly `2px` toward the point.
- **Asymmetric glyphs** (stars, arrows, carets) carry uneven visual weight. Fix
  the SVG's viewBox or path directly so no component needs a compensating margin;
  a `translate-x-px` wrapper is the fallback, not the goal.

## Elevation: shadows for depth, borders for structure

For buttons, cards, and containers whose border exists only to suggest depth,
prefer layered transparent shadows. Shadows adapt to any background because they
use transparency; a solid border color only works on the background it was picked
against.

**Keep borders that communicate structure or state**: dividers, list separators,
table cell boundaries, form input outlines, selected and focus states. Those are
not elevation.

A three-layer shadow — a hairline ring, a tight lift, and an ambient spread:

```css
:root {
  --shadow-border:
    0 0 0 1px oklch(0 0 0 / 0.06),
    0 1px 2px -1px oklch(0 0 0 / 0.06),
    0 2px 4px 0 oklch(0 0 0 / 0.04);
  --shadow-border-hover:
    0 0 0 1px oklch(0 0 0 / 0.08),
    0 1px 2px -1px oklch(0 0 0 / 0.08),
    0 2px 4px 0 oklch(0 0 0 / 0.06);
}
```

**In dark mode, simplify to a single ring.** Layered depth shadows are invisible
against a dark surface:

```css
--shadow-border:       0 0 0 1px oklch(1 0 0 / 0.08);
--shadow-border-hover: 0 0 0 1px oklch(1 0 0 / 0.13);
```

Transition `box-shadow` at ~150ms `ease-out` for hover.

Keep the light direction consistent across the product, prefer several
low-contrast layers over one heavy blur, and reduce or drop the shadow when a
surface already has sufficient contrast against its background.

| Use a shadow | Use a border |
| --- | --- |
| Cards and containers with depth | Dividers between list items |
| Buttons with a bordered style | Table cell boundaries |
| Elevated surfaces (dropdowns, modals) | Form input outlines |
| Elements sitting on varied backgrounds | Hairline separators in dense UI |
| Hover and focus lift | Selected and focus state rings |

## Image outlines

Add a 1px low-opacity outline to images so they gain the same definition as
bordered and shadowed elements around them.

```css
img {
  outline: 1px solid oklch(0 0 0 / 0.1);   /* light mode */
  outline-offset: -1px;
}
```

Dark mode uses pure white at the same opacity: `oklch(1 0 0 / 0.1)`.

**The color rule is non-negotiable: pure black in light mode, pure white in dark
mode.** Never a near-black or near-white from the palette — no slate, zinc,
neutral, `#0a0a0a`, or `#f5f5f7`. A tinted outline picks up the surface color
beneath it and reads as dirt along the image edge. Never match it to the accent
or ink color; the outline is a neutral separator, not a themed element.

Use `outline`, not `border`: `outline` never affects layout at any offset, and
`outline-offset: -1px` draws the ring just inside the edge so it hugs the corner
radius instead of sitting outside it.

## Translucent materials

Translucency is a floating functional layer that conveys hierarchy without
stealing focus.

- **Build navigation bars, toolbars, and sheets as translucent layers** —
  `backdrop-filter: blur()` plus a semi-transparent background — with content
  scrolling underneath, rather than opaque bars that consume a fixed strip.

  ```css
  .toolbar {
    background: oklch(1 0 0 / 0.6);
    backdrop-filter: blur(20px) saturate(1.8);
    border-top: 1px solid oklch(1 0 0 / 0.4);   /* bright edge = light catching the material */
  }
  ```
- **Material weight encodes hierarchy.** Heavier materials separate structural
  regions; lighter materials draw attention to interactive elements. **Never
  stack a light translucent surface on another** — legibility collapses.
- **Larger surfaces read as thicker**: stronger blur and a deeper shadow than a
  small chip. Consider a heavier shadow over busy or text-dense content and a
  lighter one over plain backgrounds.
- **Dim to focus, separate to keep flow.** A blocking modal pairs its surface
  with a dimming scrim and pushes the background back. A parallel, non-blocking
  panel uses translucency and offset *without* a scrim, so the flow is not
  interrupted. For stacked sheets, progressively dim each parent layer.
- **Keep foreground text legible over changing backgrounds.** Over a translucent
  surface, avoid flat mid-gray text — raise contrast, add a small weight step, and
  a slight letter-spacing bump. Put color on a solid layer, not on the translucent
  foreground.
- **Scroll edge effects rather than hard dividers.** Instead of a 1px border under
  sticky chrome, fade a small blur or gradient mask where content meets the
  floating layer, and only where the floating UI actually overlaps content.
- **Materialize, do not merely fade.** Animate blur radius and scale together on
  enter and exit, so a glass surface reads as a real material arriving rather
  than an opacity fade.
- Honor `prefers-reduced-transparency: reduce` — raise the background opacity and
  drop the blur.

## Gradients

Define the job before the values: lighting, depth, emphasis, material,
atmosphere, or transition. A gradient with no job is decoration competing with
content.

**Types and defaults**

| Type | Default |
| --- | --- |
| `linear-gradient` | Runs top → bottom; angles rotate clockwise |
| `radial-gradient` | `ellipse` shape, `farthest-corner` size, centered |
| `conic-gradient` | Starts at `0deg`, centered at `50% 50%` |

Radial size keywords — `closest-side`, `closest-corner`, `farthest-side`,
`farthest-corner` — change the falloff more than the position does. `circle`
holds a 1:1 aspect ratio; `ellipse` stretches with the container.

**Control the interpolation space explicitly.**

```css
background: linear-gradient(in oklab, var(--from), var(--to));
```

- `srgb` is the default and interpolates linearly in a non-perceptual space,
  which is where muddy midpoints come from.
- `oklab` interpolates linearly in a perceptual space and reaches P3 colors — the
  safe default for two colors that should blend cleanly.
- `oklch` interpolates hue circularly, so it travels *around* the hue wheel. It
  produces visibly different — often more vivid — results. Choose it when the hue
  path is the point, and specify the direction when the short way round is not
  what you want.

**Shape the ramp deliberately.**

- A color *hint* (a bare position between two stops) moves the midpoint without
  changing the endpoints — the cheapest way to control perceived velocity.
- Two stops at the same position create a hard edge: `blue 50%, red 50%`.
- Stops placed at equal percentages produce a mechanically even ramp, which is
  rarely how light behaves. Place them to shape the light, not to divide the
  space.

**The transparent-fade trap.** Fading to `transparent` interpolates toward
*transparent black* in sRGB, producing a gray or muddy fringe. Fade to the same
color at zero alpha instead:

```css
/* Muddy */
background: linear-gradient(oklch(0.98 0.01 250), transparent);

/* Clean */
background: linear-gradient(oklch(0.98 0.01 250), oklch(0.98 0.01 250 / 0));
```

**Banding.** Long, low-contrast ramps band on 8-bit displays. Fixes, in order of
preference: shorten the ramp, add intermediate stops, interpolate in `oklab`, or
overlay a very low-opacity noise texture. Reach for noise last and only when it
also serves the material.

**Performance.** Gradients are GPU-composited, and animating position, angle, or
size is cheap as long as the gradient definition itself does not change.
Re-interpolating stops every frame is not.

Never let a gradient reduce text contrast below its threshold or create a false
affordance — measure the pair over the lightest *and* darkest point of the ramp.

## Icons

- **Match icon stroke to adjacent text weight.** An icon beside text carries the
  text's optical weight: `1.5px` stroke beside regular (400), `2px` beside
  semibold (600). A hairline icon next to bold text reads as a mistake.
- **One stroke weight per icon set, one icon family per surface.** Never mix
  libraries in one view.
- **One SVG, recolored per state.** Icons use `currentColor` and take their
  hover, selected, and disabled states from CSS color and opacity — never from
  separate assets.
- **Outline is the default; fill marks the active state.** Filled icons
  everywhere removes the distinction that makes fill meaningful.
- Align icons optically with text, not by bounding box.
- Decorative icons get `aria-hidden="true"` and `focusable="false"`. Naming rules
  live in `references/accessibility-contract.md`.

**Contextual icon animation** (an icon appearing on hover, or swapping on a state
change) uses exactly these values:

- `scale`: `0.25 → 1`
- `opacity`: `0 → 1`
- `filter`: `blur(4px) → blur(0px)`
- transition: `{ type: "spring", duration: 0.3, bounce: 0 }` — bounce is always
  `0` here

With a motion library installed, match the package already in `package.json`
(`motion/react` or `framer-motion`) and follow the imports used by the nearest
peers; never mix one package's install with the other's import path. Without one,
keep both icons in the DOM (one absolutely positioned over the other) and
cross-fade with CSS transitions using `cubic-bezier(0.2, 0, 0, 1)` — that gives
both enter and exit animation with no dependency. The non-absolute icon defines
the layout size.

Animate icons that appear on hover, indicate a state change, or sit in a
contextual toolbar. Do not animate static navigation icons, decorative icons,
always-visible icons, or the text label beside an icon.

## Images

- Use the correct asset resolution and aspect behavior for the rendered size.
- Constrain with `max-width: 100%` and an explicit aspect ratio so loading does
  not shift the layout.
- Provide meaningful alternatives for informative imagery; alt-text rules live in
  `references/accessibility-contract.md`.
- Avoid decorative imagery that competes with the primary task.

## Polish order

1. content and structure;
2. layout and responsive behavior;
3. type and color roles;
4. states and accessibility;
5. shape, borders, and depth;
6. motion and micro-interaction;
7. decorative atmosphere.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Same radius on closely nested parent and child | `outerRadius = innerRadius + padding` |
| Icon looks off-center inside its button | Correct optically, or fix the SVG |
| Border used only to fake elevation | Layered transparent `box-shadow`; keep structural borders |
| One heavy shadow | Several low-contrast layers, consistent light direction |
| Layered depth shadow in dark mode | Single white ring at 8–13% |
| Image outline in slate/zinc/near-black | Pure black or pure white at 10% |
| `border` used for an image outline | `outline` with `outline-offset: -1px` |
| Light translucent surface stacked on another | Make one opaque, or change the material weight |
| Hard 1px divider under sticky chrome | Scroll-edge blur or gradient mask |
| Gradient fading to `transparent` | Fade to the same color at `/ 0` alpha |
| Muddy gradient midpoint | Interpolate `in oklab`, or move the color hint |
| Banded long ramp | Shorten it, add stops, or interpolate in `oklab` |
| Hairline icon beside bold text | Match stroke to text weight |
| Separate icon assets per state | One `currentColor` SVG, states via CSS |
| Filled icons everywhere | Outline default, fill for the active state |
| Mixed icon libraries on one surface | One family, one stroke weight |
