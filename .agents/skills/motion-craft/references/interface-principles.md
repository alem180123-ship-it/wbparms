# Interface principles

The decision framework that sits above every domain reference in this collection.
Start here, then load the reference that owns the rule you need.

## Rule ownership

Each rule lives in exactly one reference. When a concern crosses domains, keep it
with its owner and let the others name only the handoff. Report it once.

| Reference | Owns |
| --- | --- |
| `interface-principles.md` | Product job, hierarchy, restraint, working order, cross-domain arbitration |
| `accessibility-contract.md` | Semantics, keyboard and focus, names, forms, assistive technology, hit areas, zoom, and *whether* a requirement applies |
| `layout-structure.md` | Grouping, alignment, spacing, responsive structure, logical properties, spatial mirroring |
| `interface-copy.md` | Wording, terminology, voice, tone, labels, errors, empty states |
| `typography.md` | Text rendering, type scale, font behavior, wrapping mechanics, punctuation, bidi text |
| `color-and-contrast.md` | Color notation, palette construction, gamut, measuring a rendered pair, remediation |
| `surfaces-and-depth.md` | Radius, optical alignment, elevation, materials, gradients, icons, images |
| `motion-principles.md` | Whether to animate, easing, duration, choreography, interruptibility, motion performance |
| `gesture-physics.md` | Direct manipulation, velocity, momentum, boundaries, gesture recognition |
| `review-protocol.md` | Severity, evidence, consolidation, output format, verdict |
| `evidence-and-verification.md` | Evidence boundaries, verification environments, reproducibility |

Arbitrations that come up repeatedly:

- **Accessibility decides when contrast is required and how severe a failure is;
  color owns measuring the rendered pair and changing its values.**
- **Accessibility owns semantic heading structure; typography owns how heading
  levels render.**
- **Layout owns logical properties and spatial mirroring; typography owns
  language metadata, punctuation, and mixed-direction text.**
- **Typography owns truncation mechanics; layout owns whether the surrounding
  layout has room or an expansion affordance; copy owns the source string.**
- **Accessibility owns reduced-motion requirements; motion owns the recipe used
  when motion is appropriate.**

## Start with the product job

Before discussing anything visual, establish:

- who is using the surface;
- what they are trying to complete;
- what information or action is primary;
- what can fail, and what is irreversible;
- which states must exist — loading, empty, partial, error, success, disabled,
  offline, permission-limited;
- **how often the user encounters this surface.**

Frequency is not a footnote. It decides how much motion is allowed, how much
polish is justified, and how much of the user's attention any element may spend.
A control seen a hundred times a day and a control seen once are different design
problems even when they look identical.

If the product job is unclear, visual polish cannot make the interface correct.

## Restraint is the discipline

Adding is easy; the skill is deciding what not to build.

- **Every element earns its place.** If you cannot explain why something exists,
  that is the finding.
- **Simplicity is not minimalism.** Burying everything one level deeper looks
  minimal and is not simple. Sometimes *adding* context simplifies — a scrubber
  that shows time remaining is simpler than one that does not.
- **Show the common path first**, advanced options one level deeper.
- **Removal is a deliberate act**, not a side effect. Deleting requires thinking
  about the implications; adding does not, which is exactly why addition needs a
  gate.
- **Brief and precise beats prominent.** When in doubt, cut the duration or the
  ornament, not the clarity.

## Establish reading and action order

The visual hierarchy should match the user's likely sequence:

1. orient;
2. understand the current state;
3. identify the next action;
4. inspect supporting detail;
5. recover from uncertainty or error.

Use grouping, alignment, spacing, contrast, type scale, and progressive disclosure
to make that order legible. Avoid equally loud sections, arbitrary cards, and
decorative separation with no semantic grouping.

## Make relationships visible

- Keep labels close to the values or controls they describe.
- Place a control near what it affects, and arrange controls to mirror what they
  change. **If a label is needed to explain a control, the mapping is weak.**
- Align related content to shared edges or baselines.
- Use spacing as a system, not a collection of isolated numbers.
- Prefer fewer containers. Add a surface only when it communicates grouping,
  state, depth, or interaction.
- Keep the DOM reading order meaningful before changing visual order.
- Treat narrow and wide layouts as recomposed interfaces, not scaled screenshots.

## Make interaction legible

Every interactive element needs an understandable label, a visible affordance,
the applicable hover/focus/active/disabled/loading/error behavior, a sufficiently
large target, keyboard operation, state that does not rely on color alone, and
feedback proportional to the action.

**Never make a visual layer carry semantic responsibility.** Real links, buttons,
inputs, and controls live underneath or alongside any decorative effect.

**Feedback comes in four kinds** — status, completion, warning, and error.
Confirm meaningful actions, expose ongoing status, warn before a problem, and
validate inline rather than only on submit.

**Wayfinding.** Every screen answers: Where am I? Where can I go? What is there?
How do I get out? Never trap the user.

**Direct, specific labels beat safe generic ones.** Name navigation for its
contents ("Progress", "Library"), not vague umbrellas ("Home"). Specificity
creates predictability.

## Preserve user control

- Confirm destructive or costly actions when the consequence is not obvious — and
  only then. Overusing confirmation trains people to click through it.
- Back every irreversible action with forgiveness: an easy undo for slips.
- Keep escape routes and undo close to the affected action.
- Do not steal focus or unexpectedly move content.
- Make optimistic feedback distinguishable from confirmed completion.
- Preserve input and context across recoverable errors.
- Ensure animation can be interrupted without producing an invalid state.

## Build on familiarity

- Use metaphors that are neither too literal nor too abstract, and honor their
  physics.
- Things that look the same must behave the same and live in the same place.
- Break a familiar pattern only when you can show it is better — then test it
  rather than assume it.

## Design for the full range

- Adapt to the platform and to the situation, not just the viewport.
- Design inclusively across age, language, expertise, and ability.
- Where no single layout fits everyone, let people personalize — rearrange
  controls, hide what they do not use.

## Working order

Implement and review in this order. Later layers must not compensate for an
unresolved earlier one.

1. semantic structure and content;
2. state and data behavior;
3. layout and responsive recomposition;
4. typography, color roles, and controls;
5. focus, keyboard, announcements, and recovery;
6. motion and micro-interactions;
7. visual polish and atmosphere.

For a review, walk the same order — foundational failures are otherwise hidden by
polish.

## Prototype before committing

An interactive prototype is worth more than a large set of static designs. You
discover the interface by building it and playing with it, and a working prototype
sets a concrete bar that prevents a mediocre final implementation.

Design interaction and visuals together. Motion is not a layer added after the
pixels.

## Verify the actual experience

Review at minimum:

- initial, loading, empty, success, partial, and error states;
- keyboard-only operation;
- screen-reader structure where material;
- reduced-motion mode;
- representative narrow and wide viewports;
- slow network or delayed data where material;
- interruption and repeated interaction;
- real copy at realistic content lengths.

Separate source inspection, local runtime observation, and live-environment proof
in the final report.
