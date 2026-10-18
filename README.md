# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!


## 📝 Document Your Experience

- [x] **Game purpose:** A Streamlit number-guessing game. The player picks a difficulty, guesses a secret number within that range, and gets "Go HIGHER" / "Go LOWER" hints until they win or run out of attempts.
- [x] **Bugs found:**
  1. The hint messages were swapped: guessing above the secret said "Go HIGHER."
  2. On even-numbered attempts the secret was converted to a string, so guesses were compared as text (`"120" < "40"`), making hints flip between guesses.
  3. New Game didn't reset `status`, so after a win or loss `st.stop()` blocked the game and the button did nothing.
  4. Out-of-range guesses (like 110 on a 1–100 game) were accepted and used up an attempt.
- [x] **Fixes applied:**
  1. Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` into `logic_utils.py` (refactored with Claude Code).
  2. Fixed `check_guess` to return the correct hint and removed the string-comparison fallback.
  3. `app.py` now always compares against the integer secret.
  4. New Game now resets status, attempts, score, and history, and picks a secret from the current difficulty's range.
  5. `parse_guess` rejects out-of-range and non-whole-number input without using an attempt.
  6. Added pytest cases covering each fix.


## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start the game on Normal difficulty (range 1–100, 8 attempts).
2. User enters 110. The game rejects it: "Guess must be between 1 and 100." No attempt is used.
3. User enters 50. The game shows "📉 Go LOWER!" and attempts left drops to 7.
4. User enters 25. The game shows "📈 Go HIGHER!"
5. User enters 37. The game shows "📉 Go LOWER!" Hints stay consistent on every attempt now.
6. User enters the secret number. Balloons appear and the final score is shown.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
