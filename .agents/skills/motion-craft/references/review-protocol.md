# Review protocol

The shared rules for any review this collection performs: severity, evidence,
consolidation, output format, restraint, and verdict. Domain rules stay in their
owning reference; this file owns how findings are produced and presented.

A review is **read-only by default**. Inspecting source, tests, assets,
screenshots, and an authorized local or live surface is allowed. Do not change
code, install packages, publish findings externally, or deploy a fix without a
separate request. When implementation is later authorized, the report becomes the
change scope and the relevant verification is re-run afterwards.

## 1. Resolve scope and mode first

State the resolved scope in the output.

| Mode | Coverage | Finding cap |
| --- | --- | --- |
| `quick` | Primary user path and highest-traffic states; report `HIGH` and `MEDIUM` only | 5 |
| `full` | Entire requested scope, including empty, loading, error, and narrow-width states | 15 |

Default to `full` unless the user asks for a quick review.

If the requested scope is too large to inspect credibly, narrow it to the
highest-traffic complete flow and **state the boundary**. Never imply that
uninspected surfaces were reviewed.

Also establish before judging: the intended user and product job; the environment
to inspect; any authenticated or destructive flow that must not be exercised;
target devices, browsers, themes, and locales; and whether the review is visual,
functional, or both.

## 2. Recon before judgment

Identify the framework, styling system, component library, design tokens,
supported viewports, and available preview or test commands. Follow the project's
established conventions. A rule violated in service of a documented, deliberate
project decision is not a finding — note it and move on.

## 3. Severity

One shared scale across every domain:

- **`HIGH`** — blocks a task, misleads the user, hides content or controls,
  creates data-loss risk, or is a repeated systemic failure.
- **`MEDIUM`** — meaningfully harms comprehension, efficiency, adaptability, or
  consistency.
- **`LOW`** — isolated polish with limited task impact. `full` mode only.

Within a severity, rank by **reach and leverage**. A token or shared-component fix
outranks the same symptom in one leaf component.

Motion-specific escalation: an animation on a keyboard-initiated or 100+/day
action, `ease-in` on UI, `scale(0)` entry, or a non-GPU animation with an easy GPU
fix are `HIGH` — they break feel on every trigger.

## 4. Evidence

Every finding cites `path/to/file:line` and shows the current implementation. If
the artifact has no source files, cite the exact screen and component.

Label every claim:

- **Observed** — directly seen in source, assets, metadata, frames, or a running
  interface.
- **Inferred** — a reasoned explanation that fits the evidence but is not proven.
- **Unknown** — unavailable, ambiguous, or outside the authorized scope.

Do not upgrade an inference into a fact through confident wording.

**Do not report a code-level finding from appearance alone, or a visual finding
from source alone, when runtime behavior decides the result.** Static source
inspection is not a visual pass.

## 5. Consolidate

One root cause is one finding. List every confirmed location in the same row
rather than emitting a row per occurrence.

Do not pad the report to reach the cap. A short review, or no findings at all, is
a valid result.

## 6. Make restraint visible

Record candidates considered and deliberately rejected — 1–3 in `quick`, 2–5 in
`full`. A candidate is rejected when the owning rule permits the current
implementation, the evidence is insufficient, the project convention is
intentional, or the change would add complexity without user benefit.

These must be real candidates encountered during the review, not invented filler.
If the scope genuinely contains fewer borderline candidates, include those that
exist and say so.

This section is what separates a review from a wishlist.

## 7. Verify what can be verified

Run the safe, relevant checks available in the project. Inspect the rendered
interface when runtime behavior or visual judgment decides the result. Report the
exact command or interaction and the observed result.

If a check cannot be run, label it **Not verified** and state what remains.
**Never convert a verification gap into a finding.**

When motion is in scope, the feel check in `references/motion-principles.md` §14
is part of verification, not optional.

## 8. Output format

### Findings

One table, ordered by severity, then reach and leverage. Never separate
"Before:" / "After:" lines.

| # | Severity | Domain | Location | Before | After | Why |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | HIGH | Accessibility | `src/Dialog.tsx:42` | `<button><XIcon /></button>` | Add `aria-label="Close"`; mark the icon `aria-hidden="true"` | The icon-only control has no accessible name |
| 2 | HIGH | Motion | `src/dropdown.css:14` | `transition: all 400ms ease-in` | `transition: transform 200ms var(--ease-out), opacity 200ms var(--ease-out)` | `ease-in` delays the moment the user is watching; `all` animates unintended properties off-GPU |

- **Before / After** show the current implementation and an actionable
  replacement, not a description of one.
- **Why** names the violated rule and its effect on the user.
- Omit the table entirely when there are no findings and say so plainly.

**Cite exact values.** When a finding needs a curve, a duration, a spring config,
a contrast threshold, or a target size, copy it from the owning reference — never
approximate from memory.

### Considered but rejected

| Location | Candidate | Rejected because |
| --- | --- | --- |
| `src/Card.tsx:28` | Increase the shadow | Existing depth matches the shared surface token; changing one card would reduce consistency |

### Coverage

State which domains and states were actually inspected. `Clear` means inspected
with no actionable finding; `Not reviewed` must explain why.

| Domain | Evidence inspected | Result |
| --- | --- | --- |
| Accessibility | `Dialog.tsx`, keyboard traversal, focus return | 1 finding |
| Motion | `dropdown.css`, 10%-speed replay | 1 finding |

### Verification

List each check or interaction, the exact command or steps, and the observed
result. Separate checks that passed from those marked **Not verified**.

### Verdict

End with exactly one:

- **`Block`** — one or more `HIGH` findings remain.
- **`Needs changes`** — only `MEDIUM` or `LOW` findings remain.
- **`Approve`** — no actionable findings remain and the claimed coverage was
  verified.

Approval is earned, not assumed. "Approve" with a pending actionable finding is
never correct.

## 9. Remedial preference

When proposing fixes, prefer earlier moves over later ones:

1. **Delete it** — no purpose, or too frequent to justify.
2. **Reduce it** — shorter, smaller, fewer properties, fewer elements.
3. **Correct the rule violation** — easing, origin, semantics, token, contrast.
4. **Make it interruptible** — transitions or springs instead of keyframes.
5. **Move it to the GPU** — layout properties → `transform`/`opacity`.
6. **Fix timing shape** — asymmetric where the interaction is asymmetric.
7. **Polish** — blur to mask a crossfade, stagger for groups, `@starting-style`.
8. **Accessibility and cohesion** — reduced motion, hover gating, personality
   match.

Prescribing a redesign when a smaller correction addresses the cause is itself a
review defect.

## 10. Handoff

A review does not authorize edits. End with a prioritized, self-contained
implementation plan the user can approve or hand to another agent.

Each plan item must stand alone: exact file paths, the current code verbatim, the
exact target values, the repo convention to follow with one exemplar, ordered
steps, explicit scope boundaries, and both mechanical and feel-check verification.
Never write "use the easing discussed above" — the executor has no context from
this conversation.
