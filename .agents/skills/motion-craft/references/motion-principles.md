# Motion principles

Motion must explain change, preserve continuity, provide feedback, or express a
deliberate product character. Motion without a stated job is a candidate for
deletion, not tuning.

Values here are prescriptive. Use them as written unless the project has an
established motion system, in which case extend that system instead of adding a
parallel one. Where a value is a band, the band is the rule and the named context
decides where inside it you land.

Gesture, drag, and physics behavior live in `references/gesture-physics.md`.

## 1. The frequency gate

Run this before any other motion decision. It removes more bad animation than
every other rule combined.

| How often the user sees it | Decision |
| --- | --- |
| 100+ times/day — keyboard shortcuts, command palette, core navigation | **No animation. Ever.** |
| Tens of times/day — hover states, list rows, frequent toggles | Remove, or reduce to a ≤150ms opacity/color change |
| Occasional — modals, drawers, toasts, settings | Standard animation |
| Rare or first-run — onboarding, empty states, success, celebration | The delight budget lives here |

**Keyboard-initiated actions are a disqualifier, not a judgment call.** A command
palette that animates open feels lagged behind the keystroke that opened it. The
best-regarded launchers ship no open/close transition at all.

Do the arithmetic when a decision is contested: a 300ms transition on an action
performed 200 times a day costs a user roughly six hours a year of watching.

## 2. The purpose gate

Every surviving candidate must name its purpose as one of these, in one word:

- **Feedback** — the interface confirms it heard the user.
- **Continuity** — the same object stays identifiable across a change.
- **Spatial consistency** — the user learns where something came from or went.
- **State indication** — a change of state becomes legible.
- **Preventing a jarring change** — content that would otherwise teleport.
- **Explanation** — motion demonstrates how something works (marketing, onboarding).
- **Delight** — permitted only at the rare/first-run frequency tier.

"It looks good" is not on the list. If the purpose cannot be named, the correct
change is removal.

Record the decision:

```text
Purpose:
Frequency tier:
User benefit:
Cost or risk:
Static / reduced-motion equivalent:
Decision: keep | reduce | remove | prototype
```

## 3. Easing

Resolve easing in this order. Stop at the first match.

```text
Is the element entering or exiting the viewport / the DOM?
├── yes → ease-out
└── no
    ├── Is it moving or morphing while already on screen?
    │   └── yes → ease-in-out
    ├── Is it a hover, color, or opacity change?
    │   └── yes → ease
    ├── Is it constant motion (marquee, spinner, progress)?
    │   └── yes → linear
    └── default → ease-out
```

**Never `ease-in` on UI.** It withholds movement during the first moments — the
exact window the user is watching after their input. `ease-out` at 200ms is
perceived as faster than `ease-in` at 200ms even though both take 200ms.
`ease-in` remains legitimate for an autonomous wind-up in an ambient sequence
(§9), where no user input is waiting on it.

Built-in CSS easings are too weak to read as deliberate. Define tokens:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);      /* entrances, exits, direct response */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* on-screen travel between poses */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* iOS-like sheet and drawer motion */
--ease-soft: cubic-bezier(0.2, 0, 0, 1);         /* spring approximation for cross-fades */
```

Curves belong in one token file. Five hand-typed cubic-beziers that almost match
is a consolidation finding, not five decisions.

## 4. Duration

**UI motion stays under 300ms.** A 180ms dropdown reads as more responsive than a
400ms one; the slower version does not read as more considered.

| Element | Duration |
| --- | --- |
| Button and control press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects, menus | 150–250ms |
| Modals, drawers, sheets | 200–500ms |
| High-frequency hover / color change | ≤150ms |
| Marketing, onboarding, explanatory | May exceed 300ms with a stated reason |
| Ambient brand sequences (logo cycles) | Governed by §9, not this table |

Perceived speed is its own design surface. A faster spinner makes a load of
identical length feel shorter. A tooltip that opens instantly after the first one
in a toolbar makes the whole toolbar feel faster.

**Exit is faster than entrance** when the departing element no longer matters — a
common ratio is entrance 300ms / exit 150ms.

## 5. Physicality and origin

- **Never animate from `scale(0)`.** Nothing in the physical world appears from
  nothing. Enter from `scale(0.90–0.97)` with `opacity: 0`. Use the lower end for
  larger surfaces, the upper end for small controls.
- **Contextual icon swaps are the exception.** An icon replacing another icon
  inside a fixed box may scale `0.25 → 1` with `opacity 0 → 1` and
  `blur 4px → 0px`, because the box, not the glyph, carries the continuity. Pair
  it with `{ type: "spring", duration: 0.3, bounce: 0 }` — bounce is `0` here,
  always.
- **Trigger-anchored surfaces scale from their trigger**, not their own center:

  ```css
  .popover { transform-origin: var(--transform-origin); }
  ```

  Applies to popovers, dropdowns, menus, tooltips, and context menus.
  **Modals are exempt** — they are not anchored to a trigger, so
  `transform-origin: center` is correct there and must not be reported as a
  defect.
- **Press feedback**: `transform: scale(0.96)` on `:active`, transitioned at
  100–160ms `ease-out`. The usable band is `0.95–0.98`, `0.96` is the default,
  and anything below `0.95` reads as exaggerated. Applies to any pressable
  element. Provide an opt-out prop for controls where the motion would distract.
- **`translate` percentages are relative to the element's own size.**
  `translateY(100%)` moves an element exactly its own height regardless of
  content. Prefer percentages over hardcoded pixel offsets for enter and exit.
- **`scale()` scales children**, including text and icons. For press feedback
  that is the intended behavior, not a defect.

## 6. Interruptibility

Users change their minds mid-motion. Motion that cannot be redirected reads as
broken.

| | CSS transitions | CSS keyframes |
| --- | --- | --- |
| Behavior | Interpolate toward the latest value | Run a fixed timeline |
| Interrupted | Retargets from the current value | Restarts from the beginning |
| Use for | Interactive state changes, rapidly triggered UI | One-shot staged sequences |

Anything triggered rapidly or reversible mid-flight — toasts stacking, toggles,
expand and collapse, drags — must use transitions or springs. Keyframes on those
surfaces is a finding.

Entry without JavaScript:

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 400ms var(--ease-out), transform 400ms var(--ease-out);

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

Fall back to a `data-mounted` attribute set after first render where
`@starting-style` support is insufficient.

**Always animate from the presentation value.** On interrupt, read the element's
live on-screen transform and start there. Starting from the stored logical target
produces a visible jump.

## 7. Springs

Springs have no fixed duration; they settle from their parameters. They carry
velocity through an interruption, which duration-based curves cannot.

Reach for a spring when a gesture carried momentum into the motion, the element
should feel physically alive, the user can grab it mid-flight, or a decorative
value tracks the pointer.

Prefer the two-parameter form — it is easier to reason about than the physics
triplet:

```js
{ type: "spring", duration: 0.4, bounce: 0 }     // default UI: critically damped, no overshoot
{ type: "spring", duration: 0.5, bounce: 0.2 }   // momentum: only after a flick, throw, or drag release
```

- **Default to `bounce: 0`** (critically damped). Overshoot on a menu that merely
  faded in feels wrong; overshoot on a card the user flicked feels right.
- **Bounce band `0.1–0.3`** when used at all. Reserve visible bounce for
  drag-to-dismiss and deliberately playful moments.
- **Contextual icon swaps use `bounce: 0` unconditionally.**
- Traditional form when finer control is required:
  `{ mass: 1, stiffness: 100, damping: 10 }`.
- **Decompose 2D motion into independent X and Y springs.** One spring over a 2D
  distance desynchronizes when the axes carry different velocities.

## 8. Choreography for groups

- **Stagger group entrances.** Two bands, by content type:
  - `30–80ms` between peer items — list rows, grid cards, chips.
  - `~100ms` between semantic chunks — heading, description, action group in a
    staged hero or empty state. Words within a display heading can stagger at
    `~80ms`.
- Stagger is decorative. It must never block interaction while it plays, and it
  must not run on routine, high-frequency interactions.
- A reliable staged-entrance recipe combines three properties:
  `opacity 0 → 1`, `translateY 12px → 0`, `blur 4px → 0px`, over ~400ms
  `ease-out`.
- **Exits are softer than entrances.** Use a small fixed offset such as
  `translateY(-12px)` rather than the element's full height, at ~150ms. Slide
  fully out only when spatial context matters — a card returning to its list, a
  drawer closing. When motion adds no information, removing the element
  immediately is the correct choice.
- **Skip entrance animations on first paint** for elements already in their
  default state (icon swaps, toggles, tabs). In Motion this is `initial={false}`
  on the `AnimatePresence`. Verify it does not cancel an intentional page-level
  entrance.

## 9. Ambient and brand sequences

Ambient loops — logo cycles, idle motion, decorative orbits — are not UI feedback
and are not governed by the sub-300ms rule.

- Give the cycle real stillness. A detailed loop needs contrast between motion and
  rest; dwell is a designed value, not leftover time.
- An `ease-in` wind-up is legitimate as autonomous anticipation before a fast
  handoff. It is never legitimate for delaying feedback the user is waiting on.
- Preserve forward velocity across a visual swap: if the incoming layer represents
  the same moving object, it must not restart from zero.
- The loop seam must be exact. The final frame equals the first frame, with no
  size pop and no flash of unloaded content.
- Defer future cycles while the document is hidden; optionally defer while the
  pointer rests on a small identity mark.

## 10. Asymmetric timing

Slow where the user is deciding; fast where the system is responding.

```css
.overlay { transition: clip-path 200ms var(--ease-out); }      /* release: snaps back */
.button:active .overlay { transition: clip-path 2s linear; }   /* press: deliberate */
```

Symmetric timing on a press-and-release or hold-to-confirm interaction is a
finding.

## 11. Performance

- **Animate `transform` and `opacity` only.** They skip layout and paint and
  composite on the GPU. `width`, `height`, `margin`, `padding`, `top`, and `left`
  trigger all three stages every frame.
- **Never `transition: all`.** Name the properties:
  `transition-property: transform, opacity`.
- **Do not drive a child's transform through a CSS variable set on the parent.**
  Changing an inherited custom property recalculates style for every descendant.
  Set `transform` directly on the moving element.
- **Motion / Framer Motion shorthand props (`x`, `y`, `scale`) are not
  hardware-accelerated.** They run on the main thread and drop frames while the
  page is loading or scripting. Use the full transform string when motion must
  survive a busy main thread: `animate={{ transform: "translateX(100px)" }}`.
- **CSS beats JavaScript under load.** CSS animations run off the main thread;
  `requestAnimationFrame`-driven animation stutters while the browser is busy.
  Use CSS for predetermined motion, JS and springs for dynamic and gesture-driven
  motion.
- **WAAPI gives JS control at CSS performance** — hardware-accelerated,
  interruptible, no dependency:

  ```js
  element.animate(
    [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
    { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' }
  );
  ```
- **Keep transition-time `filter: blur()` under 20px.** Heavy blur is expensive,
  especially in Safari.
- Apply `will-change` only to `transform`, `opacity`, or `filter`, only around
  active motion, and only after observing first-frame stutter. Remove it after.
  Never `will-change: all`.
- `clip-path` is compositor-friendly and causes no layout shift; prefer it over
  animating `height` for reveals.

## 12. Accessibility

Motion is opt-in, not opt-out:

```css
.card { /* static styles */ }

@media (prefers-reduced-motion: no-preference) {
  .card { transition: transform 200ms var(--ease-out); }
}
```

For an existing codebase where opt-in is impractical, the global fallback uses
`0.01ms` rather than `none` so `transitionend` and `animationend` still fire and
code awaiting them does not hang:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Reduced motion means gentler, not absent.** It targets vestibular triggers, not
feedback:

| Disable entirely | Replace | Keep |
| --- | --- | --- |
| Parallax; autoplaying video, GIFs, looping decoration | Slide / scale / zoom → opacity crossfade | Loading spinners and progress |
| Large-scale movement across the viewport | Smooth scrolling → instant jump | Instant state changes (hover color, focus ring) |
| Spinning and continuous orbit | Auto-rotating carousels → start paused | Brief functional feedback (press) |

Also required:

- **Gate hover motion**: `@media (hover: hover) and (pointer: fine)`. Touch
  devices fire hover on tap, producing false positives.
- **React to a runtime preference change**, not only the value at mount.
- **Motion is never the only feedback channel.** Every state change an animation
  communicates must also be visible without it — a color, an icon, a label.
- Anything that moves, blinks, or auto-updates for more than five seconds needs a
  visible pause control. Muted looping hero video included.
- Never put the only path to an action inside an auto-dismissing element.

Reduced-motion requirements are owned by `references/accessibility-contract.md`;
this file owns the motion recipe used when motion is appropriate.

## 13. Masking an imperfect transition

When a crossfade still shows two overlapping states after tuning easing and
duration, add subtle `filter: blur(2px)` during the transition. Without it the eye
resolves two distinct objects; blur merges them into one perceived
transformation. Keep it brief and under 20px.

## 14. Verification and feel-checking

Motion can be mechanically correct and still feel wrong. Mechanical checks never
substitute for a feel check.

Mechanical:

- exact rest states before and after;
- repeated and rapid triggers;
- mid-flight reversal and interruption;
- resize, navigation, unmount, hidden-tab recovery;
- runtime `prefers-reduced-motion` change;
- keyboard and touch paths;
- dropped frames, layout shift, and paint cost on representative hardware.

Feel check:

- **Replay at 10% speed** in the browser's animation inspector, or temporarily
  multiply the duration by 2–5×. Watch for two states visibly overlapping in a
  crossfade, easing that stops abruptly, a transform origin in the wrong place,
  and coordinated properties drifting out of sync.
- **Step frame by frame** to find timing drift invisible at full speed.
- **Test gestures on real hardware**, not only a simulator.
- **Review with fresh eyes the next day.** Imperfections invisible during
  development surface later.

Report source inspection, automated tests, and runtime visual proof separately.
Static source inspection is not a visual pass.
