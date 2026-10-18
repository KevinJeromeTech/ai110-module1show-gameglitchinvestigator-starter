# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it looked normal: a Streamlit page with a guess box, Submit and New Game buttons, and a sidebar for difficulty. Once I started playing, the hints didn't make sense. The secret was 40, but guesses of 110 and 115 both told me to go higher, and then 120 told me to go lower, so the direction kept flipping instead of being consistently wrong. The game also accepted 110 even though Normal mode is supposed to be 1 to 100. After the game ended and revealed the secret, I clicked New Game and nothing happened. The game stayed stuck on the game-over screen.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|-------|-------------------|-----------------|------------------------|-------------------------|
| Secret 40, guess 110 | "Go LOWER" | "Go HIGHER" | none | `app.py`, `check_guess`: the hint messages for Too High and Too Low are swapped |
| Secret 40, guesses 115 then 120 | "Go LOWER" both times | "Go HIGHER" then "Go LOWER"; direction flips between guesses | none | `app.py`, `if submit:` block: secret is converted to a string on even attempts, so `check_guess` falls into its `except TypeError` branch and compares text (`"120" < "40"`) |
| Click "New Game" after game over | New secret, attempts reset, game playable again | Nothing happens; still shows game over | none | `app.py`, `if new_game:` block: resets attempts and secret but never sets `status` back to `"playing"`, so `st.stop()` blocks the game |
| Guess 110 on Normal (range 1–100) | Rejected as out of range | Accepted and uses an attempt | none | `app.py`, `parse_guess`: no range check |
