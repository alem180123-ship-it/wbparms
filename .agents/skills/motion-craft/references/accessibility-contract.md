# Accessibility contract

Accessibility is the floor for interface craft, not a compliance pass bolted on
at the end. Most of it is free if you use the platform: native elements ship with
keyboard support, real labels announce themselves, and a visible focus ring is
one CSS rule.

When unsure, prefer the platform default over a custom rebuild, and remove ARIA
rather than add it.

This reference owns *whether* something is required and *how severe* a failure
is. Measuring a rendered color pair and changing its values belongs to
`references/color-and-contrast.md`; visual text sizing to
`references/typography.md`; spatial mirroring to
`references/layout-structure.md`; the motion recipe used when motion is
appropriate to `references/motion-principles.md`.

## 1. Native elements first

| Element | Use for | What you get free |
| --- | --- | --- |
| `<a href>` | Navigation — anything that changes the URL | Cmd/Ctrl/middle-click, right-click → copy link, Enter |
| `<button>` | Actions — submit, toggle, open, delete | Focus, Enter *and* Space, form semantics |
| `<div onClick>` | Nothing | No role, no focus, no keyboard |

The rules of ARIA:

1. If a native element with the semantics and behavior exists, use it.
2. Do not change native semantics unless you must.
3. Every interactive ARIA control must be keyboard-operable. **A role is a
   promise** — `role="tab"` commits you to the full tab keyboard model.
4. Never put `aria-hidden="true"` or `role="presentation"` on, or above, a
   focusable element.
5. Every interactive element has an accessible name.

**No ARIA is better than bad ARIA.** A screen reader trusts your roles; a wrong
role is worse than none.

If it looks clickable it must be clickable, and if it is clickable it must be a
real interactive element. A "button" that navigates should be a styled `<a>`.

## 2. Focus

Style `:focus-visible`, never bare `:focus` — the browser shows it for keyboard
and assistive-tech focus and suppresses it for mouse clicks, where focus is
already obvious.

Preference order:

```css
/* Best: keep the browser's own indicator, just give it room */
:focus-visible { outline-offset: 2px; }

/* Custom ring when the design requires one: use the project's verified token */
:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}
```

The browser's unmodified indicator adapts to platform and forced-color settings
without the author predicting every background. A custom ring must be verified
around its **whole perimeter** against every color it crosses — component fills,
page surfaces, images, gradients, and hover/selected states. `currentColor` is
acceptable only after that check passes, because the ring may cross colors quite
different from the text's own background.

- At least a `2px` solid perimeter, or equivalent visible area.
- **Never `outline: none` without a verified replacement.**
- In `forced-colors: active`, keep the default color adjustment or use a system
  color such as `Highlight`. Do not freeze the authored color with
  `forced-color-adjust: none` unless the control stays perceivable.
- `:focus-within` when a wrapper should light up while an inner input has focus.

**tabindex:** only `0` (join the natural order) and `-1` (programmatic focus).
Positive values hijack the tab order for the whole page — fix DOM order instead.

**Roving tabindex** for composite widgets (tabs, menus, toolbars, radio groups):
one Tab stop for the group, the active item `tabindex="0"`, all others `-1`, and
arrow keys move both focus and the `0`.

**Trap and restore.** Modals set `inert` on the background, move focus inside on
open, and return focus to the trigger on close. Native `<dialog>` with
`showModal()` provides the trap, the inert background, and Escape handling — prefer
it. A custom overlay needs `role="dialog"`, `aria-modal="true"`, and an accessible
name via `aria-labelledby`. Either way:

- On open, focus the first focusable element. For a destructive confirmation,
  focus the least destructive action.
- On close, return focus to the trigger; if it no longer exists, move to the
  nearest logical container.
- `overscroll-behavior: contain` so scrolling inside never scrolls the page
  behind.

**SPA route changes** reset nothing on their own. Update `document.title`, then
move focus to the new view's `<h1>` (given `tabindex="-1"`) or to `<main>`.
Restore scroll on back/forward; scroll to top on forward navigation.

## 3. Keyboard patterns

Native elements ship these. Custom widgets must implement them.

| Widget | Keys |
| --- | --- |
| Dialog | Tab / Shift+Tab cycle inside and wrap; Escape closes |
| Tabs | Arrows move between tabs (wrapping); Tab exits to the panel; Home/End jump |
| Menu button | Enter/Space/ArrowDown opens and focuses first; ArrowUp opens and focuses last; Escape closes and refocuses the button |
| Disclosure / accordion | Header is `<button aria-expanded>`; Enter and Space toggle |
| Combobox | ArrowDown opens and moves in; Enter accepts; Escape closes and returns to the input; typing filters |
| Listbox / radio group | Arrows move selection; one Tab stop for the group |

Universal:

- Escape dismisses whatever opened last — tooltip, then menu, then dialog.
- Arrows move *within* a composite widget; Tab moves *between* widgets.
- Tabs choose an activation mode: automatic when panels render instantly, manual
  (Enter/Space) when switching is expensive.
- Enter submits from a focused input. In `<textarea>`, Enter inserts a newline and
  ⌘/Ctrl+Enter submits.
- Every pointer interaction has a keyboard path. Gestures are accelerators, never
  the only route.

## 4. Hit areas

| Standard | Minimum |
| --- | --- |
| WCAG 2.5.8 (AA) | 24×24px — the hard floor |
| WCAG 2.5.5 (AAA) | 44×44px |
| Apple HIG | 44×44pt |
| Material | 48×48dp |

Treat `44px` as the recommended touch target for primary controls and `40px` as a
useful desktop target when density permits. A smaller control is not
automatically a failure — check the spacing, equivalent-control, inline,
user-agent, and essential exceptions first.

Under the spacing exception, an undersized target passes if a 24px circle centred
on its bounding box does not intersect another target's circle. In the simple
case, 20px targets need at least a 4px gap.

**The visible element may stay small; the hit area is what must be large.** No
dead zones — a checkbox and its label share one target.

```css
/* Extend from the wrapping label or button, never the <input> itself */
.checkbox-label { position: relative; width: 20px; height: 20px; }
.checkbox-label::after {
  content: "";
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 44px; height: 44px;
}
```

Replaced elements do not render `::before`/`::after` reliably. When the element
can afford real box size, prefer `min-width`/`min-height` with
`display: inline-grid; place-items: center` — the browser then has the real
geometry for scrolling and gestures.

**Collision rule:** extended hit areas must never overlap. Shrink the
pseudo-element to the largest size that does not collide.

Add `touch-action: manipulation` to interactive elements to remove the legacy
double-tap delay, and set `-webkit-tap-highlight-color` deliberately.

## 5. Accessible names

Precedence: `aria-labelledby` > `aria-label` > native label (`<label>`, text
content, `alt`) > `title`.

- **Prefer visible text or `aria-labelledby` over `aria-label`.** `aria-label` is
  invisible, drifts out of sync with the UI, and translation tools handle it
  inconsistently.
- **Icon-only controls always need a name**: `<button aria-label="Close">` with
  the icon `aria-hidden="true"`.
- **The visible label must appear inside the accessible name** (WCAG 2.5.3). A
  button showing "Send" with `aria-label="Submit message"` breaks voice-control
  users who say "click Send".
- `aria-label` on a plain `<div>` or `<span>` with no role is ignored by most
  screen readers.
- `aria-labelledby` / `aria-describedby` pointing at a missing ID silently
  produces nothing — verify the IDs exist.
- `<button role="button">` is redundant noise.
- `role="menu"` on site navigation promises app-style arrow-key behavior; use
  `<nav>` with a list.
- Add `translate="no"` to brand names, code tokens, and identifiers.

## 6. Structure and landmarks

- Expose one visible primary `<main>` landmark. `<header>`, `<nav>`, `<aside>`,
  `<footer>` map to landmarks users jump between.
- Multiple landmarks of the same type need distinguishing labels:
  `<nav aria-label="Breadcrumbs">`.
- Headings describe their sections and form a coherent outline. One page-level
  `<h1>` with properly nested levels is the recommended default — not a
  standalone pass/fail rule; do not report either convention as a WCAG failure
  without a concrete navigation or comprehension impact.
- Headings are structure, not styling. Choose the level from the document, then
  set the visual size in CSS.
- When repeated navigation or chrome precedes the content, the **first focusable
  element is a "Skip to content" link** targeting `<main id="main">`, visually
  hidden until focused.
- Anchored headings get `scroll-margin-top` so a sticky header does not cover the
  target.
- `<title>` matches the current context, most specific first:
  `Billing · Settings · Acme`.

## 7. Forms

- **Every control has a programmatic label** — `<label for>` or a wrapping
  `<label>`. A placeholder is never a label; it disappears on input and usually
  fails contrast. Label and control share one hit target.
- Placeholders, *in addition to* a label, show the expected format:
  `placeholder="name@company.com"`.
- Mark required fields with native `required` plus a visible indicator explained
  once per form.
- **`autocomplete` with a meaningful `name`** is a WCAG 1.3.5 requirement for
  fields about the user: `name`, `email`, `tel`, `street-address`, `postal-code`,
  `cc-number`, `cc-exp`, `cc-csc`, `username`, `current-password`, `new-password`,
  `one-time-code`. Prefix with a section where relevant
  (`shipping street-address`).
- **Correct `type` and `inputmode`** pick the right mobile keyboard. Use
  `type="text" inputmode="numeric"` for OTP, PIN, and card numbers — it keeps text
  semantics and avoids the spinner. `type="number"` only for a true numeric
  quantity. `spellcheck="false"` on emails, codes, and usernames.
- **Never block paste.** Users paste passwords and one-time codes.
- Stay compatible with password managers and 2FA autofill: a real `<form>`,
  correct `autocomplete`, no fake inputs.
- **Accept free text and validate after.** Do not filter characters as the user
  types. Trim before validating — autocomplete and text expansion add trailing
  spaces.

**Errors that announce:**

```html
<label for="email">Email</label>
<input id="email" type="email" autocomplete="email"
       aria-invalid="true" aria-describedby="email-error" />
<p id="email-error">Enter a valid email address.</p>
```

- `aria-invalid="true"` on the failing field, removed once fixed.
- `aria-describedby` links the field to its inline error.
- Errors render inline beside their field, never as a red border alone.
- On submit, **focus the first invalid field** — the focus move is the
  announcement.
- **Do not disable submit until the form is valid.** Keep it enabled, validate on
  submit, and let validation surface what must be fixed. Once the request starts,
  disable it and show a spinner **while keeping the original label** — the label
  is what tells assistive tech which button is busy.
- Warn on unsaved changes before navigation, and never lose typed input to a
  re-render.

**Disabled states.** Native `disabled` removes the control from the tab order,
suppresses activation, applies `:disabled`, and excludes it from submission — use
it when a control is genuinely unavailable. `aria-disabled="true"` only announces
the state; with it you must block pointer and keyboard activation in code,
prevent submission, style the state explicitly including forced-colors, and
explain nearby why the action is unavailable. Never set both on one element.
Disabled controls are exempt from contrast minimums; keep them legible anyway.

## 8. Announcing change

Work down this list and stop at the first match:

1. **Focus moves there anyway** (opened modal, first invalid field) — nothing
   extra needed.
2. **Tied to a specific control** (field error, character count) —
   `aria-describedby` on the control.
3. **Non-urgent, not tied to a control** (toast, "Saved", result count, loading) —
   polite live region / `role="status"`.
4. **Urgent, not tied to a control** (form-level failure, session expiring) —
   `role="alert"`.

| Mechanism | Politeness | Use for |
| --- | --- | --- |
| `role="status"` (= polite + atomic) | Waits for a pause | Toasts, "Saved", counts, loading |
| `role="alert"` (= assertive + atomic) | Interrupts immediately | Errors and urgent problems only |

- **For repeated polite updates, render a stable empty region first** and then
  change its text. Inserting a region together with its content announces
  inconsistently.
- Dynamically inserted `role="alert"` is commonly announced but varies — test the
  target browser and screen-reader combinations.
- **Default to polite.** Overusing `assertive` is the most common live-region
  mistake; it interrupts whatever the user was reading.
- Keep messages short and self-contained — `aria-atomic` re-reads the whole
  region.
- **Do not move focus to a toast.** Announce it and leave focus where the user is
  working.
- For loading, set `aria-busy="true"` on the updating region, announce
  "Loading…", then announce the outcome.

**Visually hidden content** uses `1px` boxes, not `0` — some screen readers skip
zero-sized elements:

```css
.sr-only {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
```

Never use `display: none` or `visibility: hidden` for this — both remove the
content from assistive tech entirely.

## 9. Alternative text

Choose by purpose, not by what the image depicts:

| Purpose | Alt | Example |
| --- | --- | --- |
| Decorative, or redundant with adjacent text | `alt=""` — empty but present | Logo beside the company name in text |
| Informative | The meaning it adds | `alt="Ticket QR code"` |
| Functional (the image *is* the control) | The action or destination | `alt="Search"`, not `alt="magnifying glass"` |
| Image of text | The exact text — better, use real text | `alt="50% off everything"` |
| Complex (chart, diagram) | Short summary, full data nearby | `alt="Revenue by quarter, described below"` |

A missing `alt` attribute is worse than an empty one — screen readers fall back to
reading the file name.

**SVG:** decorative gets `aria-hidden="true"` and `focusable="false"`; meaningful
inline SVG gets `role="img"` with `aria-label`; `<img src="icon.svg" alt="…">` is
the most reliable delivery for simple cases.

Prerecorded video needs captions; audio needs a transcript. Never autoplay with
sound, and always render controls.

## 10. Color, motion, zoom

- **Never encode state through color alone.** Every status needs a redundant
  icon, label, or underline. Determine which contrast requirement applies from
  the content and state, then measure the rendered pair per
  `references/color-and-contrast.md`.
- **`prefers-reduced-motion` is required** wherever movement exists. Reduced means
  gentler, not absent — keep opacity and color feedback, drop movement, parallax,
  and autoplay. The full disable/replace/keep table lives in
  `references/motion-principles.md`.
- **Autoplay and timed UI**: anything moving, blinking, or auto-updating for more
  than five seconds needs a visible pause control (WCAG 2.2.2). Prefer explicit
  dismissal over timers — anything containing an action, an error, or information
  the user may act on stays until dismissed. If a toast must time out, five
  seconds is the floor, and hover or focus pauses the timer. Never put the only
  path to an action inside an auto-dismissing element.
- **200% zoom** (WCAG 1.4.4): all content and functionality survives text at 200%.
- **Reflow at 320px** (WCAG 1.4.10): at 400% zoom on a 1280px viewport the page
  works with vertical scrolling only. Genuinely two-dimensional content — tables,
  maps, code blocks — scrolls inside its own container.
- **Never block zoom.** No `user-scalable=no`, no `maximum-scale=1`. Safari
  ignores the cap for pinch zoom while every other browser enforces it.
- Fixed heights are what break under zoom — use `min-height` on anything
  containing text.

**`rem` vs `px`:** respect how the codebase is set up; do not mix units into
someone else's system. Where the choice is open:

| `rem` | `px` |
| --- | --- |
| `font-size` | Borders and hairlines |
| `max-width` of text containers | Focus outline width and offset |
| Media-query breakpoints | `box-shadow` details |
| Spacing that should scale with text | Fixed-size decorations |

Breakpoints are where it matters most: at a larger base font size a `rem` query
switches layout when the text needs it; a `px` query does not.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| `outline: none` to remove the ring | Style `:focus-visible`; mouse clicks will not show it |
| Custom focus color assumed to work everywhere | Verify the full perimeter and forced-colors mode |
| `<div onClick>` for a button or link | `<button>` for actions, `<a href>` for navigation |
| Placeholder as the only label | Add a visible `<label for>` |
| Positive `tabindex` to fix focus order | Fix DOM order; only `0` and `-1` |
| Repeated polite update announced inconsistently | Stable empty region, then change its text |
| `assertive` for a routine toast | `polite`; reserve `assertive` for errors |
| `aria-hidden="true"` on a focusable element | Remove it, or make the element non-focusable |
| `aria-labelledby` pointing at a missing ID | Verify the ID exists |
| Functional icon alt describes the picture | Describe the action: `alt="Search"` |
| `maximum-scale=1` to stop iOS input zoom | 16px input font on mobile; never block zoom |
| Submit disabled until the form is valid | Keep it enabled; validate on submit, focus the first error |
| Bare spinner replacing the button label | Keep the label, add the spinner |
| Focus moved to a toast | Announce it; leave focus where the user is working |
| Gesture with no keyboard equivalent | Add arrows / Enter / Escape parity |
| Extended hit areas overlapping | Shrink to the largest non-colliding size |

## Verification

Walk the interface as a keyboard-only user first — every flow must complete
without a mouse. Then as a screen-reader user: does each control announce a name,
a role, and its state?

- Tab through the entire flow; confirm order, visible focus, and no traps.
- Escape from every overlay; confirm focus returns to the trigger.
- Inspect accessible names in the accessibility tree, not the source.
- Trigger every error path and confirm the announcement and focus move.
- 200% zoom and 320px reflow.
- Forced-colors / high-contrast mode.
- `prefers-reduced-motion` at load and toggled at runtime.
- Touch targets on a real device.

State which checks were run and which remain unverified. Never convert a
verification gap into a finding.
