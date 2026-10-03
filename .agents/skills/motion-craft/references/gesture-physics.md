# Gesture physics

Use this reference for drag, swipe, sheets, drawers, sliders, reorderable lists,
scrubbing, and any interaction where the user's hand drives a value directly.

An interface feels fluid when motion starts from the value currently on screen,
inherits the user's velocity, projects momentum forward, and can be grabbed and
reversed at any instant. Every rule below serves one of those four properties.

General timing, easing, and reduced-motion rules live in
`references/motion-principles.md`. This file does not repeat them.

## 1. Response — latency is the foundation

Directness collapses the moment lag appears.

- **Respond on pointer-down, not on release.** Highlight or scale a control the
  instant it is pressed. Waiting for `click` to show feedback reads as dead.
- **Feedback is continuous during the gesture, not only at its end.** A drag, a
  slider, or a sheet must update 1:1 with the pointer the whole way through.
  Animating only on completion is a finding.
- **Audit every delay on the input path**: debounces, artificial timers,
  transition waits, and the legacy ~300ms tap delay
  (`touch-action: manipulation` removes it).

## 2. Direct manipulation — 1:1 tracking

- **Preserve the grab offset.** Track the distance between the pointer and the
  element's edge at `pointerdown` and maintain it. Snapping the element's center
  to the pointer breaks the illusion immediately.
- **Use Pointer Events with `setPointerCapture`** so tracking survives the
  pointer leaving the element's bounds.
- **Keep a short position/timestamp history** — the last few `pointermove`
  events, not just the current point. Release velocity is computed from it.
- **Ignore additional touch points once a drag has begun.** Without this,
  switching fingers mid-drag jumps the element to the new position.

```js
el.addEventListener('pointerdown', (e) => {
  if (isDragging) return;                       // multi-touch protection
  el.setPointerCapture(e.pointerId);
  grabOffset = e.clientY - el.getBoundingClientRect().top;
  history = [{ y: e.clientY, t: e.timeStamp }];
});
```

## 3. Interruptibility

The single most important property of gesture-driven motion. The user's thought
and their gesture happen in parallel.

- **Never lock out input during a transition.** A closing sheet the user grabs
  again must follow the finger, not finish closing and then reopen.
- **Start every new animation from the presentation (live) value.** Reading the
  logical target instead produces a visible jump.
- **Avoid CSS transitions and `@keyframes` for anything gesture-driven.** They
  cannot be grabbed and reversed smoothly mid-flight. Springs animate from the
  current value by default, which is exactly what an interrupt needs.
- **Blend velocity through a reversal; never hard-cut it.** Replacing one
  animation with another at the moment of reversal creates a velocity
  discontinuity the user reads as a wall. Use a spring implementation that
  retargets while carrying current velocity.

## 4. Velocity handoff

When the gesture ends, the animation must continue at the finger's exact
velocity. This seam is what most separates fluid from merely fine.

Pass the release velocity as the spring's initial velocity. Some APIs expect a
*relative* velocity, normalized by the remaining distance:

```text
relativeVelocity = gestureVelocity / (targetValue − currentValue)
```

Example: element at `y = 50`, target `y = 150` (100px remaining), finger moving
50px/s → initial spring velocity `0.5`. Motion / Framer Motion accept absolute
px/s directly via the `velocity` option.

## 5. Momentum projection

Do not snap to the boundary nearest the *release point*. Use velocity to project
where the gesture was going, then snap to the target nearest that projection.
This is what makes a flick feel like a throw.

```js
// decelerationRate ≈ 0.998 for a normal scroll feel; 0.99 is snappier
function project(initialVelocity /* px/s */, decelerationRate = 0.998) {
  return (initialVelocity / 1000) * decelerationRate / (1 - decelerationRate);
}

const projectedEndpoint = currentPosition + project(releaseVelocity);
const target = nearestSnapPoint(projectedEndpoint);
animateSpringTo(target, { velocity: releaseVelocity });   // then hand off velocity, §4
```

Use this exponential-decay form. The physics-textbook `v² / (2·deceleration)` is
not what shipping bottom sheets and carousels use and feels wrong by comparison.

## 6. Dismissal thresholds

**Distance alone is the wrong threshold.** A quick flick should dismiss even if
it travelled a short distance.

```js
const elapsed = Date.now() - dragStartTime;
const velocity = Math.abs(swipeAmount) / elapsed;   // px per ms

if (Math.abs(swipeAmount) >= SWIPE_THRESHOLD || velocity > 0.11) {
  dismiss();
}
```

- Velocity threshold `≈ 0.11` px/ms as a starting point; tune against a real
  device, not a trackpad.
- **Decide reverse-versus-commit from the velocity sign at release**, not from
  the position at release. A user dragging back toward the origin at the moment
  of release intends to cancel, even if the element is still past the midpoint.

## 7. Boundaries — rubber-band, never hard-stop

At an edge, resist progressively instead of stopping. A hard stop reads as
frozen; continuous resistance reads as responsive with nothing more to reveal.

```js
// The further past the bound, the less the element follows.
function rubberband(overshoot, dimension, constant = 0.55) {
  return (overshoot * dimension * constant) / (dimension + constant * Math.abs(overshoot));
}
```

Apply the same principle to axis constraints: allow the off-axis drag with rising
friction rather than clamping it to zero.

## 8. Gesture recognition details

- **Tap**: highlight on pointer-down, commit on pointer-up. Allow cancel by
  dragging away and re-commit by dragging back. Add roughly 10px of hit padding.
- **Drag and swipe**: require a small movement threshold (~10px hysteresis)
  before committing to a direction, then track 1:1.
- **Detect all plausible gestures in parallel from the first move**, then cancel
  the losers once intent is clear. Avoid recognizers that report only a final
  state (`swipeleft`-style events) — they discard the continuous tracking needed
  for feedback.
- **Minimize disambiguation delays.** Double-tap detection unavoidably delays
  single taps; pay that cost only where double-tap genuinely exists.

## 9. Non-pointer parity

A gesture is an accelerator, never the only path.

- Every drag, swipe, and reorder needs a keyboard equivalent — arrow keys to
  move, Enter or Space to pick up and drop, Escape to cancel and restore.
- Expose the current value or position when it carries meaning
  (`aria-valuenow` on a slider, a live status for a reorder).
- Keep visible focus above any decorative layer.
- Do not block unrelated page scroll outside the drag handle. Scope
  `touch-action` to the handle rather than the page.
- A non-focusable draggable element is not an acceptable final control.

## 10. Scroll and page-level behavior

- `overscroll-behavior: contain` on scrollable overlays so an inner scroll never
  chains to the page behind it.
- `scroll-snap-type` with `scroll-padding-inline` matching the container padding,
  so snap points land on content edges rather than the viewport edge.
- Set `-webkit-tap-highlight-color` deliberately rather than accepting the
  default gray flash.

## 11. Cleanup

Every gesture controller must release what it acquired:

- release pointer capture on `pointerup`, `pointercancel`, and unmount;
- cancel scheduled frames and pending springs;
- disconnect resize and intersection observers;
- restore body scroll locking and `inert` state;
- return to a known resting state after cancellation or error.

## 12. Verification

- slow drags and fast flicks, in both directions and on both axes;
- release while reversing, to confirm the velocity sign decides the outcome;
- grab mid-animation and confirm the element follows without a jump;
- over-drag past every boundary;
- touch, trackpad, mouse, pen, and keyboard paths;
- multi-touch: begin a drag, add a second finger, confirm no jump;
- interruption during entrance and during exit;
- reduced motion: gestures still work, momentum flourish is reduced;
- frame cost during the drag on representative low-power hardware, not only a
  desktop demo.

Gestures cannot be verified from source alone. State plainly when only source was
inspected.
