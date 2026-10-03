# Layout structure

Layout communicates before a word is read. Position, spacing, and alignment carry
hierarchy on their own, and generous space beats decoration. A good layout also
survives stress: resize it, translate it, mirror it, zoom it, and it should still
hold.

Numeric values here are starting points for interfaces with no established
density or spacing system. Preserve deliberate platform chrome, compact
professional tools, and existing project tokens when they remain usable under
hit-area, zoom, localization, and viewport stress.

Hit-area minimums are owned by `references/accessibility-contract.md`; line
length and text spacing by `references/typography.md`; radius, shadows, and
material by `references/surfaces-and-depth.md`.

## Group with space, not lines

Three grouping tools, in order of preference:

1. **Negative space** — the default. Related items sit close; unrelated items sit
   far apart.
2. **Background shapes** — a card or filled container, when a group must read as
   one unit (a selectable row, a draggable card).
3. **Separator lines** — last resort, for dense data where space costs too much
   (tables, long settings lists).

**The structural rule: the gap between groups is at least 2× the gap within a
group.** `8px` inside → `16px`+ between. Below that ratio the eye cannot find
where one group ends and the grouping reads as noise.

```css
.field-group { display: flex; flex-direction: column; gap: 8px; }
.form        { display: flex; flex-direction: column; gap: 24px; }
```

When a separator is genuinely needed, keep it quiet — hairline width, low
contrast — and never combine it with a large gap. The gap already did the job.

## Keep controls distinct from content

Interactive elements need a visible signal that they are interactive: a
background, a border, an underline, or placement in a consistent control zone. A
control styled identically to the static text beside it is invisible.

The inverse holds too: a non-clickable badge shaped exactly like the buttons
around it collects dead clicks.

## Align to shared edges

Pick a small set of alignment edges and put everything on them. The eye tracks
straight edges to scan.

- Every stray edge — an icon 2px off the text edge, a card padded differently
  from its neighbor — reads as noise even when nobody can name it.
- Use one project spacing step per level of subordination; `16px` is a useful
  default when no scale exists, and deeper nesting repeats the same step.
- Text aligns to the leading edge; numeric table columns align to the trailing
  edge.

## Logical properties, not physical

Express direction-dependent horizontal position as leading/trailing so the layout
mirrors automatically under `dir="rtl"`.

| Avoid | Use |
| --- | --- |
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `left: 0` | `inset-inline-start: 0` |
| `text-align: left` | `text-align: start` |
| `border-right` | `border-inline-end` |

Reserve physical properties for genuinely physical geometry — positioning against
a device notch, or matching a fixed gesture direction.

When arrangement encodes progression (star ratings, step indicators, progress
bars), the sequence mirrors in RTL: stars fill from the trailing side. Flexbox and
grid with logical properties mirror automatically; hand-positioned elements do
not. Digit order inside a number never reverses — that rule lives in
`references/typography.md`.

## Order by importance

Readers scan top-to-bottom and leading-to-trailing.

- The most important information sits near the top and the leading edge.
- Give essential information room. Do not bury the one number the user came for
  under rows of secondary detail; push secondary content into collapsed sections,
  tabs, or detail views.
- Within a row, identifying content leads; metadata and actions trail.
- **The first screenful is a table of contents, not the whole book.** One primary
  action per view. Group secondary actions behind a menu once they exceed two or
  three. Prefer a short view that links deeper over a long view that shows
  everything at level one.

Think in leading/trailing rather than left/right, so the same hierarchy mirrors
correctly in RTL.

## Breathing room between targets

Without an established density scale:

| Between | Starting point |
| --- | --- |
| Adjacent bordered or filled controls (buttons, inputs) | `12px` |
| Around borderless controls (text buttons, icon buttons) | `24px` |
| Unrelated control groups | `24px`+ (2× the intra-group gap) |

Borderless controls need more clearance because nothing marks where one target
ends and the next begins — the space itself is the boundary. Compact professional
tools may use less as long as hit areas stay distinct and never overlap. These
clearances are *in addition to* minimum target sizes, so expanded hit areas
cannot collide.

## Progressive disclosure needs an affordance

Hiding complexity is good; hiding it without a cue is a trap. Content hidden with
zero cue may as well not exist.

- **Peeking items.** In a horizontal scroller, size items so the next one peeks
  `16–32px` past the container edge. A row that ends exactly at the edge looks
  complete and nobody scrolls it.
- **Disclosure controls.** Collapsed sections get a chevron or a labelled
  control, and the label states what is hidden — "Show 12 more results", not
  "More".
- **Truncation cues.** Clamped text shows an ellipsis plus a way to expand.

The peeking-scroller recipe — container padding creates the peek, and snap points
stay on the content edge:

```css
.scroller {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-inline: 24px;
  scroll-padding-inline: 24px;
  scroll-snap-type: x mandatory;
}
.scroller > * {
  flex: 0 0 calc(100% - 48px - 24px);   /* container − margins − peek */
  scroll-snap-align: start;
}
```

Preserve the product's established scroll indicator or disclosure pattern where
one exists.

## Content bleeds, controls float

The two layers behave differently at the edges:

- **Content layer** — backgrounds, hero media, and scrollable lists extend to the
  viewport edges.
- **Control layer** — text and controls stay inside the layout margins and safe
  areas, floating above the content.

```css
.article {
  display: grid;
  grid-template-columns: 1fr min(65ch, calc(100% - 48px)) 1fr;
}
.article > *            { grid-column: 2; }
.article > .full-bleed  { grid-column: 1 / -1; }

.fab {
  position: fixed;
  inset-inline-end: calc(16px + env(safe-area-inset-right));
  bottom: calc(16px + env(safe-area-inset-bottom));
}
```

**Inset buttons from the edges.** In content layouts, keep full-width buttons
inside the layout margins (start near `16px` inline on mobile) with a visible
radius. A button pressed against the viewport can read as system chrome and clip
against curved corners and gesture zones. Edge-to-edge actions stay valid when
they are intentionally platform or application chrome, account for safe areas,
and remain distinguishable from system UI.

Sticky chrome floats above the content layer; it does not dam it.

## Hold structure until it breaks

Breakpoints come from the content, not the device catalog.

- Break where the layout actually stops fitting — when a sidebar squeezes content
  below its minimum measure, when a card grid drops under a usable column width —
  not at `768px` because a preset says so.
- **Collapse late.** A layout that keeps its expanded structure as long as it
  genuinely fits stays stable and familiar; collapsing early throws away space
  the user paid for.
- **Prefer container queries for components.** A card should adapt to the column
  it occupies, not to the viewport.

```css
.card-list { container-type: inline-size; }
@container (max-width: 400px) {
  .card { grid-template-columns: 1fr; }
}
```

Test the smallest supported size and the largest first — those break first — then
the sizes between.

## Plan for growth and clipping

Layouts fail in two directions: content grows, and viewports shrink.

**String expansion varies substantially by language and by source-string length.**
Do not rely on one universal percentage.

- No fixed widths sized to English labels; use `max-width` plus wrapping.
- No fixed heights on text containers; use `min-height` when a floor is needed.
- Buttons size from their label via `padding-inline`, never a hardcoded width.
- Test with pseudo-localization or a long-string locale before shipping.

**Clipping:** never park a critical action where it can be cut off — the bottom
edge of a resizable pane, below the fold of a fixed-height modal, behind an
expanding keyboard. Keep primary actions in stable chrome with safe-area padding.
If a modal's content scrolls, its action row does not.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Separator line where spacing would do | Remove the line, double the gap between groups |
| Uniform spacing plus lines to compensate | Vary the gap; the ratio is the grouping |
| Action styled identically to the text beside it | Give the control a visible affordance |
| Non-clickable element shaped like a button | Restyle it, or make it interactive |
| Three unrelated leading edges in one column | One shared edge, one indent step |
| `margin-left` / `padding-right` in a localizable layout | `margin-inline-start` / `padding-inline-end` |
| Content-layout button touching the viewport | Inset within the layout margins |
| Carousel that looks complete at the edge | Let the next item peek `16–32px` |
| Adjacent controls merge, or hit areas overlap | Increase the gap; `12px` / `24px` starting points |
| Breakpoints at 768/1024 because they are defaults | Break where content stops fitting |
| Viewport media query breaking a card in a sidebar | Container query on the component |
| Fixed-width container sized to one language | `max-width` + wrapping; test pseudo-localization |
| Primary action at the clip-prone bottom of a pane | Sticky chrome with safe-area padding |
| Everything on the first screen is prominent | One primary action; demote the rest |

## Verification

- Narrowest and widest supported viewports first.
- 200% zoom and 320px reflow.
- RTL mirroring, including any progression-encoding arrangement.
- Longest realistic strings in every shipped locale.
- Reading order matches visual order with CSS disabled or in the accessibility
  tree.
- Every critical action reachable with the on-screen keyboard open and the pane
  resized to its minimum.
