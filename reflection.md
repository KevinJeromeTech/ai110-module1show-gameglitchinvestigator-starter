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


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude Code inside VS Code to do the refactor, and Claude in chat to trace bugs back to specific lines and review changes. One correct suggestion: Claude Code moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` from `app.py` into `logic_utils.py`, swapped the hint messages so "Too High" says "Go LOWER", and removed the code that turned the secret into a string on even attempts. I verified it with pytest (`test_guess_too_high_says_go_lower` and `test_three_digit_guess_vs_two_digit_secret`) and by replaying the game with a secret of 40 and guesses above it, which now said LOWER every time. One suggestion I didn't accept as written: Claude Code moved `parse_guess` over unchanged, so out-of-range guesses like 110 were still accepted and decimals like 4.9 were silently cut down to 4. I changed it to take the difficulty's range and reject both cases with a clear error message, and I confirmed it with `test_parse_rejects_out_of_range` and by typing 110 into the live game. I also caught Claude's chat miscounting expected results twice (how many lines git should report and how many matches grep should find), which reminded me to check the actual output instead of trusting the prediction.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---I treated a bug as fixed only when both a pytest case and the live game agreed. The most useful test was `test_three_digit_guess_vs_two_digit_secret`, which checks that 120 against a secret of 40 returns "Too High"; it targets the string-comparison bug, where "120" sorted before "40" as text. For New Game, I lost a game on purpose, clicked New Game, and confirmed the game restarted with a fresh secret, zero attempts, and an empty history. The starter test file also couldn't run at first because plain `pytest` couldn't find `logic_utils`, and every function was a stub; running `python -m pytest` fixed the path issue. AI helped me design tests by turning each row of my bug log into a specific input and expected output, so each test maps directly to a bug I actually saw.

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire Python script from top to bottom every time you interact with the page: clicking a button, typing in a box, or changing a dropdown. That means normal variables reset on every click, so anything the game needs to remember, like the secret number, attempts, score, and whether the game is over, has to live in `st.session_state`, which survives between reruns. I compare it to a whiteboard that stays up while the rest of the room gets reset after every move. This explained the New Game bug: the button reset the secret and attempts in session state but left `status` as "lost", so on the next rerun the script hit `st.stop()` and the game never restarted. Whatever you don't explicitly reset in session state carries over, even when you meant to start fresh.

---

## 5. Looking ahead: your developer habits

One habit I'm keeping is running `git remote -v` before my first commit in any project. During this project I found out my home folder had been turned into a git repo connected to one of my client projects, so my first commits went to the wrong repository. The push was rejected and nothing was lost, but it showed me that "it committed" doesn't mean "it went where I think it went." Next time I work with AI on code, I want to give it one bug at a time with the exact input and output, instead of describing everything at once. This project showed me that AI-generated code can look clean and still be wrong in ways you only catch by actually running it, like a hint that alternates between two different bugs depending on whether the attempt number is even or odd.
