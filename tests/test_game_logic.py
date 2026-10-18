from logic_utils import check_guess, parse_guess


def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_three_digit_guess_vs_two_digit_secret():
    # Regression: as text, "120" < "40", which caused flipped hints
    outcome, _ = check_guess(120, 40)
    assert outcome == "Too High"


def test_parse_rejects_out_of_range():
    ok, _, err = parse_guess("110", 1, 100)
    assert not ok
    assert err is not None and "between" in err


def test_parse_rejects_text():
    ok, _, _ = parse_guess("abc", 1, 100)
    assert not ok


def test_parse_accepts_valid_guess():
    assert parse_guess("42", 1, 100) == (True, 42, None)