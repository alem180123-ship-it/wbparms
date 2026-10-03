# Interface copy

Clear beats clever, consistency beats variety, and the best error message is the
interaction redesigned so the error cannot happen.

How copy *renders* — capitalization via `text-transform`, truncation, smart
punctuation — belongs to `references/typography.md`. Error markup and
announcements belong to `references/accessibility-contract.md`. Room for
translated strings belongs to `references/layout-structure.md`. This file owns
the words.

## Recon the existing voice first

Before writing or reviewing, inspect nearby interface copy, the product's
terminology, its localization conventions, and any content style guide.

**Preserve intentional brand character when it stays clear and appropriate to the
stakes.** Treat a difference from generic plain language as a finding only when
it creates inconsistency, ambiguity, translation risk, or a tone mismatched to
the consequence.

## One voice, flexible tone

The product has one voice, established by its existing system rather than
invented during a local edit. Keep terms consistent: if it is "Archive" in the
menu, it is not "Move to storage" in the toast.

Tone flexes with the stakes:

| Context | Tone |
| --- | --- |
| Success, onboarding, empty states | Warm, may be light |
| Routine actions, settings | Neutral, minimal |
| Errors, destructive confirmations | Calm, plain, zero playfulness |
| Data loss, security, billing | Serious and explicit |

## Address the reader directly

Use "you", not "the user", in instructional copy. Avoid "we" in errors where it
obscures responsibility or recovery — "Unable to load content" beats "We're
having trouble loading this content". Preserve an established first-person brand
voice in low-stakes contexts where it stays clear.

Use possessives sparingly — "Favorites" over "Your Favorites" — and never switch
perspective mid-flow.

## Plain words

Choose easily understood words and delete every word that is not needed.

- No idioms, colloquialisms, or humor that will not translate.
- Skip unnecessary gender: "Subscribers can post recipes", not "each subscriber
  can post his or her recipes".
- Match the input device: "tap" on touch, "click" with a pointer, "select" when
  both are possible.
- **Never build a sentence by concatenating fragments around a variable.**
  `"You have " + n + " new messages"` breaks in every language whose word order
  differs. Use full templated strings with proper pluralization.

## Verb-first buttons

Button labels start with a verb naming the specific action: "Send", "Save draft",
"Delete project".

Never "OK!", "Let's go!", or a bare "Yes"/"No" on a consequential action.
**Confirmation buttons repeat the consequence** so the dialog is answerable
without reading the body: "Delete this project?" offers `Delete project` and
`Cancel`, not `Yes` and `No`.

Multi-step flows use one vocabulary throughout: "Get started" to enter,
"Continue" *or* "Next" (pick one) to advance, "Done" to finish. Alternating
synonyms across steps makes users wonder whether the buttons differ.

## Links describe their destination

Link text must make sense out of context — screen-reader users navigate by a list
of the page's links. "Read the billing docs", never "Click here" (which also
fails the device-verb rule on touch), and never a bare "Learn more" when several
appear on one page. Suffix each: "Learn more about exports".

## One capitalization policy

Pick title case or sentence case **per element type** — all buttons, all
headings — and apply it consistently. Sentence case is the safer default: calmer,
no per-word rules, localizes cleanly. "Save Changes" beside "Discard changes"
reads as sloppiness.

## Settings describe the ON state

Label a toggle for what happens when it is on: "Send read receipts". Users infer
the off state. Labelling the negative — "Don't send read receipts" — turns the
toggle into a double negative.

Link directly to a referenced setting rather than describing the path to it: a
"Notification settings" link, not "Go to Settings > Notifications > Email".

## Errors say how to fix, next to where it broke

An error is an instruction, placed adjacent to the failing field.

| Instead of | Write |
| --- | --- |
| "That password is too short" | "Choose a password with at least 8 characters" |
| "Invalid name" | "Use only letters for your name" |
| "Oops! Something went wrong." | "Unable to save. Check your connection and try again." |
| "We couldn't process your request" | "Unable to save. Check your connection and try again." |

No blame, no "oops", no exclamation marks. Phrase hints positively — "Use only
letters", not "Don't use numbers or symbols" — and show them *before* the mistake
rather than after.

**If the same error fires for many users, redesign the interaction instead of
rewording it.**

## Empty states point forward

An empty state says what this place is and how to fill it, with one clear next
action.

```html
<!-- A shrug -->
<p>No results.</p>

<!-- Orientation plus a next step -->
<p class="font-medium">No projects yet</p>
<p class="text-sm text-muted">Projects keep your tasks and files together.</p>
<button class="mt-4">Create a project</button>
```

Search and filter empty states name the query and offer an exit: "No results for
'quarterly'. Clear filters."

**Never park crucial persistent information in an empty state** — it disappears
the moment content exists.

## Placeholders are examples, not labels

Placeholders show the expected format (`name@example.com`, `DD/MM/YYYY`). A
placeholder is never a field's only label: it vanishes on input, and every field
keeps a visible label.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Local rewrite ignores established terminology | Inspect nearby copy and the style guide first |
| "The user" in instructional copy | Address the reader as "you" |
| "We're having trouble…" obscures recovery | Direct status plus next step |
| `OK` / `Yes` on a destructive dialog | Repeat the consequence: "Delete project" |
| "Continue" on step 2, "Next" on step 3 | One flow vocabulary throughout |
| "Click here" or a bare "Learn more" | Describe the destination |
| "Save Changes" beside "Discard changes" | One capitalization policy per element type |
| "Don't send read receipts" toggle | Label the ON state |
| "Oops! Something went wrong." | Say what to do, next to the failing field |
| "No results." as the whole empty state | Orient, then point forward |
| Placeholder doing the label's job | Visible label; placeholder shows the format |
| `"You have " + n + " messages"` | Templated string with pluralization |
| Describing a settings path in prose | Link directly to the setting |

## Verification

- Read the complete flow in order, not isolated strings.
- Check every variable interpolation and plural form, including zero and one.
- Check the longest realistic value at the narrowest supported width.
- Confirm the same concept uses the same term everywhere it appears.
- Confirm every destructive confirmation is answerable from its buttons alone.
