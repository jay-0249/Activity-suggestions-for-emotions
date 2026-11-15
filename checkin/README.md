# Reflective check-in

The drawing is a way into reflection, not a measurement. The vision model acts as a mirror. The person's own answer, a few taps, decides whether and what to suggest.

> Drawing is how you express it, a one-tap check is how we measure it, and the AI is a mirror, not a diagnostician. (`data/safety.json`)

## Why this framing

| Finding | What it means for the flow | Source |
|---|---|---|
| No study validates reading current mood from a photo of a short scribble; the best pen-tablet dataset (EMOTHAW) catches about 4 in 10 anxious or stressed people and 1 in 8 depressed people | The drawing cannot be the measurement | `research_notes/Drawing AI brief review/brief_verification.md` |
| Drawing an emotion you were asked to depict decodes above chance (about 51% vs 17%); free scribbles have no such evidence | Ask "draw how you feel", not "draw random lines" | Damiano et al. 2023; Çiftçi et al. 2025 (KIDO) |
| In KIDO, children's own words predicted the emotion far better than their drawing (97% vs F1 79%) | Ask one question and let the person answer | Çiftçi et al. 2025 |
| Naming a feeling is itself a small regulation step ("affect labeling") | The check-in is useful on its own, even with no activity | Lieberman et al. 2007; Torre & Lieberman 2018 |
| Dwelling on a feeling makes it worse (d = −0.26); venting drawings do worse than distracting ones | Keep reflection short; move to an option quickly; never prompt venting | Webb, Miles & Sheeran 2012; Drake & Winner 2012 |
| A Gemini Flash baseline made unsupported claims about drawings about 46% of the time | Constrain the model to visible features and allow "can't tell" | ArtCognition (arXiv 2601.04297) |

## The flow

**1. Invite (about 5 s).** "Take 10–30 seconds. Draw how you feel right now: lines, shapes, colours, a word, anything. There's no right way." On-screen drawing is better than a paper photo because the app can also log stroke timing for later research; a paper photo works for the demo.

**2. Mirror (vision model, turn 1).** The model uses `system_prompt.md` and returns JSON matching `reflection.schema.json`. The app shows only the `reflection` text and the `question`. It describes what is visible, may offer at most 2 tentative guesses, and says "can't tell" for ordinary scribbles. Never show decimal scores.

**3. Name it (the person, about 5 s).** Show the 12 feeling chips with an intensity tap for each (a little / quite / very), plus "not sure" and "I'm really struggling".
- Model guesses appear pre-selected but faded (`prefillChips`), and count only once tapped.
- An optional text box answers the model's question. If the person writes, send the text back to the model (turn 2) to suggest chips; the person still confirms them.

**4. Respond (engine).** `decide()` in `engine.mjs` runs on the confirmed chips only.

| Mode | When | What the app does |
|---|---|---|
| `support_safety` | "I'm really struggling", the model's `safety_concern`, or a self-harm cue in the person's words | No activities. Supportive message, prompt to contact someone, localised crisis resources |
| `ask` | No chips confirmed | Ask again gently; never guess on their behalf |
| `neutral` | Only "neutral" | "Steady is good." No suggestions |
| `positive` | Only calm / content / energetic | Up to 2 optional ideas to savour or share it; "no need to do anything" |
| `mixed` | Some negative, but positive load ≥ negative load | One gentle option; keep the good part (rule R38) |
| `support` | Negative load > positive load | 3 options from different categories, from the most specific evidence available: triple, then pair, then single-emotion rankings; contraindicated activities removed for every confirmed feeling |

Load is the sum of intensity scores (a little = 0.45, quite = 0.65, very = 0.85), which are uncalibrated defaults. "Very" on a tension feeling puts a low-effort calming option first (rule R01).

**5. Close the loop.** After an activity: "Did that help?" (yes / a bit / no). Pass the answers back as `history`, so what helped rises and what didn't drops (rule R29). Plot self-reported feelings over time for the trend graph, never the model's guesses.

## Personalisation

`preferences.likes` / `dislikes` use the activity tags (creative, physical, social, solo, indoor, outdoor, mindful, cognitive, musical, verbal, hands-on, low-effort, high-energy). They reorder options inside the evidence-allowed set and never bring back an avoided activity. `preferences.context` (`otherPersonAvailable`, `canGoOutside`) removes options the person can't do right now.

## What not to do

- Don't say "you are anxious", "we detected stress" or any clinical word. Use "It might look like…" and always offer "That's not right".
- Don't suggest anything from the model's reading alone.
- Don't show scores, percentages or a "mood score" derived from the drawing.
- Don't treat fast or messy lines as negative. The prompt tells the model they are normal for this task.

## Before the demo: two quick checks

1. **Bias check.** Have 5 teammates scribble when calm and when stressed. Count how often the model guesses a negative feeling for the calm drawings. If it is often, tighten the prompt.
2. **Consistency check.** Send the same photo 5 times, and to 2 models. If the guesses change, show only the reflection and the chips, with no pre-fill.

## Files

| File | What it is |
|---|---|
| `system_prompt.md` | Vision-model system prompt for turns 1 and 2 |
| `reflection.schema.json` | JSON schema for the model's output (use it for structured output) |
| `engine.mjs` | Reference decision engine over `../data` (Node 18+; port to Dart for Flutter) |
| `engine.test.mjs` | 13 scenario tests: `node --test checkin/engine.test.mjs` |

## Example outputs from the engine

| Confirmed feelings | Mode | Suggestions | Evidence used |
|---|---|---|---|
| stressed (quite) + tired (quite) | support | progressive muscle relaxation, sitting in nature, calming music | pair rule, direct combination evidence |
| angry (very) | support | slow breathing, drawing to distract, forest bathing | single emotion; venting and vigorous exercise excluded |
| sad + lonely | support | yoga, brief friendly chat, gardening | pair rule, same-sample evidence |
| bored | support | challenge-matched game, positive reminiscence, mastery challenge | single emotion (thin evidence) |
| content | positive | best-possible-self writing, act of kindness | single emotion |
