# Typography

Good typography is mostly restraint: a small scale, comfortable spacing, and
enough contrast beat any clever effect. A label, a table cell, a marketing
headline, and an article paragraph do not share one set of rules.

**Express every change in the project's existing styling system.** Tailwind
utilities in a Tailwind project, declarations in CSS, CSS Modules,
styled-components, or StyleX elsewhere. Never introduce a second styling approach
to apply a typography fix, and never introduce a new typeface to satisfy a
checklist — rendering details do not override the product's chosen family.

Copy itself is owned by `references/interface-copy.md`. Semantic heading
structure is owned by `references/accessibility-contract.md`; this file owns how
those headings render.

## Scale and roles

Define a small set of sizes and deviate from it as little as possible.
Hard-coded one-off sizes break down at scale. Name sizes by use (`text-body-sm`)
rather than by size (`text-sm`) on a team, where the usage rule must survive
without the author present.

A role pairs size, line-height, and weight so a role is one decision instead of
three. A workable starting point for a product interface:

| Role | Size | Line-height | Weight |
| --- | --- | --- | --- |
| Display | `2.25rem` / 36px | `1.1` | `600` |
| Title | `1.5rem` / 24px | `1.2` | `600` |
| Heading | `1.125rem` / 18px | `1.3` | `600` |
| Body | `1rem` / 16px | `1.5` | `400` |
| Caption | `0.8125rem` / 13px | `1.4` | `400` |

Emphasis within a role is one weight step (`400 → 500`), not a size change.

Size floors:

| Text | Size |
| --- | --- |
| Long-form body starting point | ~`16px`, verified in the actual typeface and measure |
| Inputs and menus | ~`14px` (but `16px` on mobile inputs, see below) |
| Captions | `13px` |
| Absolute floor | Rarely below `12px` |

**Heading sizes descend with level.** Map heading levels to descending steps of
the scale; a visually subordinate heading must not overpower its parent. Adjacent
levels may share a size at the small end as long as weight or spacing keeps them
distinct. Never pick a heading element for its default size.

## Line-height, measure, and letter-spacing

| Text | Line-height |
| --- | --- |
| Headings | ~`1.1` |
| Body copy | `1.5`–`1.6` |
| Anything wrapping to 3+ lines | at least `1.4`, even in height-constrained rows |

Prefer unitless values so line-height scales with font size; `line-height: 24px`
does not. A tightly leaded card description is harder to read than a taller row
is to fit.

**Cap the measure at 60–75 characters per line** for long-form text. Any unit
works: `65ch` measures characters directly; at a `16px` body size the same range
lands roughly between `560px` and `680px` depending on the font. What matters is
that a cap exists and the resulting line length sits in range — recheck it if the
body size changes.

**Letter-spacing is size-specific; one value for all sizes is wrong somewhere.**

- Large display text: slightly negative, around `-0.02em`. Letters read too far
  apart as they grow.
- Small uppercase labels: slightly positive, around `0.05em`.
- Body copy at reading sizes: neither.

Kerning is built into the font and applied automatically; disable it only
deliberately with `font-kerning: none`.

**Text trimming.** Fonts reserve space above and below the letters, which is why
text sits slightly low in buttons and badges. `text-box: trim-both cap alphabetic`
removes it. Treat it as progressive enhancement where support is incomplete.

## Wrapping, truncation, and punctuation

- `text-wrap: balance` on headings — distributes lines evenly.
- `text-wrap: pretty` on descriptions — prevents a single orphaned word.
- Skip both in long-form text. Browsers ignore `balance` past a few lines, and
  evening out a whole paragraph wastes space and hurts reading.
- `overflow-wrap: break-word` wherever long words, URLs, or IDs could escape the
  container.
- `white-space: nowrap` on labels and badges where a break looks broken.
- Truncate single lines with `text-overflow: ellipsis` plus `overflow: hidden`
  and `white-space: nowrap`; multiple lines with `line-clamp`.
- **Truncation hides content.** If the hidden text matters, keep the full value
  reachable — a tooltip, an expanded view, or a title attribute.
- `text-align: start`. Reserve `justify` for specific editorial layouts; it does
  not belong in an interface.

**Write copy in natural case and control presentation with `text-transform`,** so
a redesign never requires rewriting strings.

Use the right characters: curly quotes in prose (straight quotes in code), an en
dash for ranges (`2010–2020`), an em dash to set off a thought, the single
ellipsis character `…`, `&nbsp;` to keep values like `16 px` together, and `&shy;`
to control where a long word may break.

## Numbers

**Apply `font-variant-numeric: tabular-nums` to any value that changes.** Digits
have different widths by default, so timers, counters, prices, and live metrics
shift the layout as they update. Right-align numeric table columns to the
trailing edge.

`font-variant-numeric: slashed-zero` distinguishes `0` from `O` in identifiers
and codes.

## Fonts, formats, and features

| Category | Traits | Use for |
| --- | --- | --- |
| Serif | Terminal strokes guide the eye along a line | Long passages, editorial |
| Sans-serif | Even shapes that stay crisp small | Default for most interfaces |
| Monospace | Equal glyph widths so columns align | Code, tables, tabular data |
| Display | Drawn for large sizes | Marketing headlines, hero text |
| Script | Mimics handwriting | Rare decorative moments |

- **Serve `.woff2`.** `.woff` is a fallback for very old browsers; `.ttf` and
  `.otf` are raw desktop formats with no web compression.
- **Rarely more than three families.** Pair for contrast, not similarity: a serif
  headline over a sans body reads as deliberate; two near-identical sans-serifs
  read as a mistake.
- **Thin weights are display-only.** Below `18px`, stay at weight `400`+. Weights
  `100–300` disappear at text sizes and on low-DPI screens; reserve them for
  `28px`+ and verify they hold against the background.
- **"Display" in a font's name does not make it a display font.** Families that
  ship both `Display` and `Text` optical variants expect you to use the one
  matching the size you are setting.
- Two fonts at the same `font-size` can look like different sizes; x-height is
  usually why.

**Prefer the CSS property over the raw OpenType or variation tag.** Properties
keep working when a non-variable fallback renders; raw tags silently do nothing.

| Prefer | Over |
| --- | --- |
| `font-weight: 650` | `font-variation-settings: "wght" 650` |
| `font-optical-sizing: auto` | `font-variation-settings: "opsz" …` |
| `font-variant-numeric: tabular-nums` | `font-feature-settings: "tnum" 1` |
| `font-variant-caps: small-caps` | `font-feature-settings: "smcp" 1` |
| `font-variant-position: super` | manual `<sup>` styling |

Reserve `font-variation-settings` and `font-feature-settings` for custom axes
(`"GRAD" 80`) and numbered slots (`"ss01" 1`, `"cv11" 1`) that have no property
of their own. What each numbered slot does differs per font — check the font's
own documentation.

**Load the faces the design actually uses.** Browsers may synthesize a missing
weight or style. Set `font-synthesis: none` only after verifying that every
required bold, italic, small-cap, superscript, and subscript form stays visually
distinct across the whole fallback stack; the blanket shorthand disables all of
them at once and can erase emphasis. Prefer the specific longhand
(`font-synthesis-weight`, `font-synthesis-style`) when only one mode is unwanted.

## Details

- **Underlines from the font's own metrics**: `text-underline-position: from-font`
  and `text-decoration-thickness: from-font`, or tune manually with
  `text-decoration-thickness`, `text-underline-offset`, and
  `text-decoration-skip-ink: auto` so the line clears descenders.
- **Only the color of a real underline animates reliably.** If anything else must
  animate, build the underline as a separate element.
- A dotted underline (`text-decoration-style: dotted`) is the conventional hint
  that a word carries extra information — an abbreviation or a defined term.
- **Inputs at `16px` on mobile.** iOS Safari zooms the page when an input's text
  is smaller. Use `text-base sm:text-sm` or equivalent. Never use
  `maximum-scale=1` or `user-scalable=no` as the fix: Safari ignores the cap for
  pinch zoom while every other browser honors it and blocks zooming, which fails
  WCAG 1.4.4.
- **Font smoothing once at the root.** macOS renders text heavier than intended;
  `-webkit-font-smoothing: antialiased` and `-moz-osx-font-smoothing: grayscale`
  (Tailwind's `antialiased`) belong on the root layout, not scattered per
  component.
- **Keep text selectable by default**, including application chrome — users copy
  labels, identifiers, errors, and values in ways the designer cannot predict.
  Use `user-select: none` only on a specific draggable or gesture surface where
  accidental selection demonstrably conflicts with the interaction.
- `::selection` can carry brand into the reading experience as long as the
  selected pair stays legible.
- `caret-color` is about as far as caret styling usefully goes.

## Language and bidirectional text

- Set `lang` so browsers and assistive technology choose the right pronunciation,
  quotes, and hyphenation.
- Set `dir` at the document or content boundary where direction changes.
- **Digit order never reverses.** A phone number reads identically in RTL; do not
  fight the Unicode bidi algorithm with manual reordering. Wrap mixed
  number-and-text values in `<bdi>` when adjacent RTL text disturbs them.
- A one- or two-line snippet follows the surrounding UI's direction; a paragraph
  of three or more lines aligns to its own script's direction. `text-align: start`
  with the correct `lang`/`dir` on the paragraph handles this.
- Spatial mirroring and logical CSS properties belong to
  `references/layout-structure.md`.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| `.ttf` / `.otf` served on the web | Convert to `.woff2` |
| `font-variation-settings: "wght"` for weight | `font-weight` — survives fallback |
| `font-feature-settings: "tnum" 1` | `font-variant-numeric: tabular-nums` |
| Hard-coded one-off font sizes | Use the type scale |
| Child heading visually overpowers its parent | Map that section to descending scale steps |
| Heading element chosen for its default size | Choose semantics first, set size in CSS |
| `line-height: 24px` on scalable text | Unitless (`1.5`) |
| `leading-none` on a three-line description | At least `1.4` on anything wrapping 3+ lines |
| Full-width paragraphs | Cap at 60–75 characters |
| Orphan on a paragraph's last line | `text-wrap: pretty` |
| Lopsided two-line heading | `text-wrap: balance` |
| Changing numbers shift the layout | `tabular-nums` |
| Truncated text with no way to read it | Tooltip or expanded view |
| `UPPERCASE` typed into the copy | Natural case + `text-transform` |
| Justified text in an interface | `text-align: start` |
| Underline cuts through descenders | `from-font` metrics, `skip-ink: auto` |
| Inputs below `16px` zoom on iOS | `text-base sm:text-sm`; never block zoom |
| Font smoothing repeated per component | Once at the root |
| Thin or light weight on `14px` UI text | Weight `400`+ below `18px` |
| Selection disabled across app chrome | Restore it; suppress only on a verified drag conflict |
| One `letter-spacing` value across all sizes | Tighten large text, leave body near `0` |

## Verification

- Read one full paragraph for comfort rather than scanning the code.
- Squint at the page and confirm the hierarchy still holds.
- Resize the viewport to catch bad wrapping, widows, and truncation at real
  content lengths — not lorem ipsum.
- Test the longest realistic string in every supported language.
- Confirm changing values do not shift the layout.
- Zoom to 200% and confirm nothing clips or overlaps.
