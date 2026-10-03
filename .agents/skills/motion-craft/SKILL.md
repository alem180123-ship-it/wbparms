---
name: motion-craft
description: >-
  Find, specify, review, or improve motion in a web interface against exact
  rules for frequency, purpose, easing, duration, choreography, interruption,
  gesture physics, accessibility, and performance. Use when the main task is
  animation, transitions, or interaction motion. Supports brief, opportunities,
  review, and improve modes. Do not use for reverse engineering a reference
  video or building an animated logo identity. Triggers on animation, motion,
  transition, easing, cubic-bezier, spring, stagger, drag, swipe, gesture,
  interruptible, prefers-reduced-motion, "make it feel better", "the animation
  feels off", "should this animate".
license: MIT
---

# Motion Craft

Motion must clarify change, provide feedback, preserve continuity, or express a
deliberate product character. **Motion without a stated job is a candidate for
deletion, not tuning.** Default to flagging; approval is earned.

Most animation problems are not tuning problems. They are decisions that should
have been "no".

## Quick reference

| Need | Read |
| --- | --- |
| Frequency gate, easing, duration, springs, choreography, performance, reduced motion | `references/motion-principles.md` |
| Drag, swipe, sheets, velocity, momentum, boundaries, gesture recognition | `references/gesture-physics.md` |
| Severity, findings table, rejected candidates, verdict | `references/review-protocol.md` |
| Frequency's role in product hierarchy, restraint, working order | `references/interface-principles.md` |
| Evidence boundaries and feel-checking | `references/evidence-and-verification.md` |

**Never approximate a value that exists in a reference.** Copy the exact curve,
duration, spring config, or threshold.

## Select one mode

- **`brief`** — turn an idea into an exact motion specification.
- **`opportunities`** — find places that genuinely benefit from motion, and name
  what must stay static.
- **`review`** — assess existing motion without changing code.
- **`improve`** — produce prioritized, self-contained correction plans.
  Implement only after the user approves them.

Infer the mode only when the user's verb is unambiguous. Otherwise ask which
result they want.

## The ten non-negotiables

Every animation in scope is measured against these. A violation is a finding.

1. **Justified.** The purpose is one of: feedback, continuity, spatial
   consistency, state indication, preventing a jarring change, explanation, or
   delight. "It looks good" on a frequently-seen element is a block.
2. **Frequency-appropriate.** Keyboard-initiated and 100+/day actions get **no**
   animation. Tens/day gets ≤150ms opacity or color, or nothing. Occasional gets
   standard. Rare and first-run carry the delight budget.
3. **Responsive easing.** Entrances and exits use `ease-out` or a strong custom
   curve. **`ease-in` on UI is a block.** Built-in CSS easings are too weak for
   deliberate motion.
4. **Sub-300ms UI.** Anything slower on a UI element needs a stated reason.
   Per-element budgets are in `references/motion-principles.md` §4.
5. **Physical origin.** Trigger-anchored surfaces scale from their trigger, not
   center. Never `scale(0)` — enter from `scale(0.90–0.97)` with opacity.
   **Modals are exempt** and stay centered.
6. **Interruptible.** Rapidly triggered or gesture-driven motion retargets from
   its current value. Keyframes that restart from zero are a finding.
7. **GPU-only.** `transform` and `opacity` only. Layout properties,
   `transition: all`, and motion-library shorthand props under load are
   performance findings.
8. **Accessible.** `prefers-reduced-motion` honored — gentler, not zero. Hover
   motion gated behind `@media (hover: hover) and (pointer: fine)`. Motion is
   never the only feedback channel.
9. **Asymmetric where the interaction is.** Deliberate phases animate slower; the
   system's response snaps. Symmetric timing on press-and-release is a finding.
10. **Cohesive.** Motion matches the component's personality and the rest of the
    product. Curves and durations live as shared tokens, not five hand-typed
    near-matches.

## Flag on sight

- `transition: all`
- `scale(0)` entrances, or a pure fade with no initial transform
- `ease-in` on any UI interaction
- animation on a keyboard shortcut, command palette, or 100+/day action
- UI duration > 300ms with no stated reason
- `transform-origin: center` on a trigger-anchored popover, dropdown, or tooltip
- keyframes on toasts, toggles, or anything triggered rapidly
- animating `width`, `height`, `margin`, `padding`, `top`, or `left`
- motion-library `x`/`y`/`scale` shorthands on motion that runs while the page is
  busy
- a CSS variable on a parent driving a child's transform
- movement with no `prefers-reduced-motion` handling
- ungated `:hover` motion
- symmetric enter/exit timing on a press-and-release interaction
- an everything-at-once entrance where a stagger belongs
- drag dismissal on distance alone, with no velocity threshold
- a hard stop at a drag boundary instead of rising resistance

## Shared intake

Establish before any mode proceeds:

- the user task and the interface state change;
- trigger, **frequency tier**, and input method;
- target elements and their spatial relationship;
- desired motion character and the product's personality;
- framework, installed motion libraries, and existing easing/duration tokens;
- browser, device, and performance constraints;
- reduced-motion requirement;
- reference material, and whether it is directional or pixel-exact.

Inspect existing motion tokens and component conventions before proposing new
ones. **Plans extend the project's system; they never add a parallel one.**

## Purpose gate

Complete this for every candidate before anything else:

```text
Purpose:
Frequency tier:
User benefit:
Cost or risk:
Static / reduced-motion equivalent:
Decision: keep | reduce | remove | prototype
```

Reject motion that delays a frequent task, competes with content, makes position
ambiguous, repeats without value, or duplicates feedback already communicated
more clearly.

## Brief mode

Produce, in order:

1. before and after state;
2. trigger and completion condition;
3. element hierarchy;
4. choreography phases;
5. per-property timing and easing, with exact values;
6. transform origin and spatial path;
7. interruption and reversal behavior;
8. responsive and reduced-motion variants;
9. implementation strategy;
10. verification cases, including the feel check.

Name the perceived quality alongside the numbers. A spec that reads
`200ms ease-out` without saying "crisp, arrives immediately" cannot be judged.

## Opportunities mode

Inspect the actual journey. **Expect to reject most candidates** — an opportunity
finder that suggests motion everywhere produces exactly the over-animated
interfaces this skill exists to prevent.

Return three groups:

- **`high-value`** — motion measurably improves understanding or control;
- **`prototype`** — promising but needs comparison;
- **`keep static`** — motion would add cost, delay, noise, or accessibility risk.

Cap suggestions at 5–7 for a whole application, fewer for a single view, ordered
by leverage rather than by how enjoyable they would be to build.

Where to hunt: pressable elements with no `:active` state; content that swaps,
appears, or vanishes instantly; accordions that snap; panels and popovers with no
spatial connection to their trigger; surfaces that exit differently than they
entered; grids that pop in all at once; draggable elements that snap with no
physics; rare high-emotion moments rendered flat.

Useful sweeps: conditional renders with no transition, `onClick` handlers on
elements with no `:active` styling, `details`/accordion markup, drag handlers,
`.map(` renders of entering lists, empty-state and success components.

**A rejected-candidates section is required**, each with the gate question that
killed it. That section is what separates this from a wishlist.

## Review mode

Observe at normal speed, at 10% speed, under repeated input, with the keyboard,
and under reduced motion. Inspect the controller code separately from the visual
result.

Review purpose and frequency; duration, easing, delay, and stagger; continuity
and transform origin; gesture thresholds and velocity; interruption, reversal,
and cleanup; layout, paint, and compositing cost; hidden-tab, offscreen, hover,
and focus behavior; and reduced-motion behavior.

Report only proven findings, ordered by impact, using the table format in
`references/review-protocol.md`. Cite `file:line`.

## Improve mode

For every approved issue, write a plan that a model with **zero context and zero
taste** can execute:

```markdown
### NNN — <short imperative title>
- Severity / category:
- Current evidence: file:line plus the current code verbatim
- Desired behavior:
- Exact choreography: every value spelled out
- Files or components:
- Repo conventions to follow: one exemplar to imitate
- Steps: one concrete edit per step
- Boundaries: what must not be touched
- Accessibility:
- Performance:
- Mechanical verification: exact commands and expected outcome
- Feel check: what to watch for at 10% speed and under reduced motion
- Done when:
```

Never write "use the easing discussed above" — inline the exact cubic-bezier, the
exact duration, the exact path. Do not bundle unrelated animation changes into
one task.

## Implementation selection

Choose the smallest tool that fits:

| Situation | Tool |
| --- | --- |
| Bounded state motion, predetermined | CSS transitions |
| One-shot staged sequence | CSS keyframes |
| Entry without JavaScript | `@starting-style` |
| Programmatic control at CSS performance | Web Animations API |
| Stateful orchestration, layout continuity, exit presence | The project's existing motion library |
| Gestures, momentum, interruptible physics | Springs |
| Geometry-driven reveal or morph | SVG path, mask, or `clip-path` |
| A visual model DOM and SVG cannot express efficiently | Canvas or WebGL |

**Do not add a second animation library to solve a local effect** without an
explicit compatibility and maintenance justification. Check `package.json` and
match the import path already in use.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Tuning an animation that should be deleted | Run the frequency gate first |
| `transition: all` | Name the properties |
| `ease-in` on a dropdown or modal | `ease-out` or `var(--ease-out)` |
| `scale(0)` entrance | `scale(0.95)` + `opacity: 0` |
| Popover scaling from its own center | `transform-origin: var(--transform-origin)` |
| Reporting a centered modal as a wrong origin | Modals are exempt |
| Keyframes on a rapidly triggered element | CSS transitions, so it retargets |
| Motion-library `x`/`y` shorthand under load | Full transform string |
| Reduced motion implemented as zero motion | Keep opacity and color, drop movement |
| Drag dismissal on distance only | Add a velocity threshold (~0.11 px/ms) |
| Five near-identical cubic-beziers | Consolidate into tokens |
| Approximating a value from memory | Copy it from the reference |
| Judging feel from source alone | Replay at 10% speed, or say it was not verified |

## Output

Follow `references/review-protocol.md`: a findings table with
`Severity | Location | Before | After | Why`, a required rejected-candidates
section, coverage, verification, and exactly one verdict — `Block`,
`Needs changes`, or `Approve`.

**Block** on any feel-breaking regression: animation on a keyboard or
high-frequency action, `scale(0)` or `ease-in` on UI, or a non-GPU animation with
an easy GPU fix.

When feel cannot be judged from the available evidence, say so and put a feel
check in the plan rather than guessing.
