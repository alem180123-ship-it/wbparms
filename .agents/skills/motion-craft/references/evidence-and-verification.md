# Evidence and verification

Use this reference for reviews, reverse engineering, implementation, and final
handoffs.

## Label the evidence boundary

Keep three categories separate:

- **Observed:** directly seen in source, assets, metadata, screenshots, frames, or
  a running interface.
- **Inferred:** a reasoned explanation that fits the evidence but is not directly
  proven.
- **Unknown:** information not available, ambiguous, or outside the authorized
  scope.

Do not upgrade an inference into a fact through confident wording.

## Distinguish verification environments

- Source inspection proves what the inspected files contain.
- Static validation proves syntax, structure, or declared relationships.
- A local run proves behavior in that exact local environment.
- Automated tests prove only the asserted cases.
- A deployed preview proves that deployment.
- Live verification proves the observed production behavior at that time.

A local implementation is not a deployment, and a deployment is not independent
proof that every user flow works.

## Capture reproducible evidence

Record:

- exact input paths or URLs;
- relevant revision, branch, or snapshot date;
- viewport, theme, motion preference, and input method;
- video dimensions, duration, frame rate, and extraction strategy;
- commands or tools used;
- generated artifact paths;
- limitations, missing states, and uncertainty.

Use unique output directories for analyses. Never silently overwrite the source
or a previous evidence run.

## Review findings

A useful finding includes:

1. the observed behavior;
2. where it occurs, as `path/to/file:line`;
3. why it matters to the user or system;
4. the smallest credible correction, with exact values;
5. severity and confidence;
6. how the correction should be verified.

Do not invent issues to fill a category. Explicitly say when no material finding
was established.

Severity, consolidation, the findings table, the required rejected-candidates
section, and the verdict are defined in `references/review-protocol.md`. Use that
format rather than improvising one.

## Feel-checking

Some qualities cannot be established by reading code, running a test, or taking a
single screenshot. Motion, gesture response, crossfades, and spring character are
in that category. A mechanically correct implementation can still be wrong.

When the quality in question is felt rather than measured:

- **Replay at 10% speed** in the browser's animation inspector, or temporarily
  multiply durations by 2–5×.
- **Step frame by frame** to expose timing drift between coordinated properties.
- **Drive gestures on real hardware.** A trackpad does not produce the velocities
  a thumb does.
- **Return with fresh eyes.** Imperfections invisible during development surface
  the next day.

If a feel check was not performed, say so and name it as the outstanding
verification. Never present a source-only inspection as evidence about how
something feels.

## Visual comparison

Compare the full interaction, not a single attractive frame:

- start and exact rest states;
- anticipation and initial direction;
- acceleration and peak velocity;
- handoff or morph;
- follow-through and settle;
- dwell;
- interruption;
- responsive variants;
- reduced-motion behavior.

Contact sheets reveal composition. Frame deltas reveal activity. Source code
reveals intended timings. None alone proves the complete experience.

## Stop conditions

Stop and ask for direction when:

- material product intent remains ambiguous;
- multiple visual directions have different product consequences;
- the required asset or reference is missing;
- rights or provenance block reuse;
- the next step would publish, deploy, install, buy, or mutate external state;
- verification requires credentials or authority not provided.

Report the blocker with the evidence already gathered and the smallest decision
needed to proceed.
