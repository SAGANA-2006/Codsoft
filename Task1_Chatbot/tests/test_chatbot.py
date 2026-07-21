"""
test_chatbot.py

Unit tests for PyBot's rule-based response logic.

Run with:
    pytest
or:
    python -m pytest tests/
"""

import os
import sys

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, _PROJECT_ROOT)

import chatbot  # noqa: E402


# ---------------------------------------------------------------------------
# contains_any
# ---------------------------------------------------------------------------

def test_contains_any_matches_keyword():
    assert chatbot.contains_any("hi there", chatbot.GREETING_KEYWORDS)


def test_contains_any_matches_multi_word_phrase():
    assert chatbot.contains_any(
        "how are you today", chatbot.WELLBEING_KEYWORDS
    )


def test_contains_any_no_match_returns_false():
    assert not chatbot.contains_any("random text", chatbot.JOKE_KEYWORDS)


# ---------------------------------------------------------------------------
# is_math_expression / calculate
# ---------------------------------------------------------------------------

def test_is_math_expression_true_for_valid_expression():
    assert chatbot.is_math_expression("12 * 4")
    assert chatbot.is_math_expression("3.5 + 2")


def test_is_math_expression_false_for_non_math_text():
    assert not chatbot.is_math_expression("hello there")


def test_calculate_addition():
    assert chatbot.calculate("2 + 3") == "The answer is 5"


def test_calculate_subtraction():
    assert chatbot.calculate("5 - 2") == "The answer is 3"


def test_calculate_division():
    assert chatbot.calculate("10 / 4") == "The answer is 2.5"


def test_calculate_division_returns_int_when_whole():
    assert chatbot.calculate("10 / 2") == "The answer is 5"


def test_calculate_division_by_zero():
    result = chatbot.calculate("5 / 0")
    assert "divide by zero" in result.lower()


def test_calculate_invalid_expression():
    result = chatbot.calculate("not math")
    assert "couldn't understand" in result.lower()


def test_calculate_non_numeric_operands():
    result = chatbot.calculate("a + b")
    assert "couldn't read that as numbers" in result.lower()


# ---------------------------------------------------------------------------
# generate_response (routing)
# ---------------------------------------------------------------------------

def test_generate_response_greeting():
    reply = chatbot.generate_response("hello", "Sam")
    assert "Sam" in reply


def test_generate_response_exit():
    reply = chatbot.generate_response("bye", "Sam")
    assert "Goodbye" in reply
    assert "Sam" in reply


def test_generate_response_empty_input():
    reply = chatbot.generate_response("   ", "Sam")
    assert "type something" in reply.lower()


def test_generate_response_math_expression():
    reply = chatbot.generate_response("6 * 7", "Sam")
    assert reply == "The answer is 42"


def test_generate_response_help():
    reply = chatbot.generate_response("help", "Sam")
    assert "here's what i can help" in reply.lower()


def test_generate_response_fallback():
    reply = chatbot.generate_response("asdlkjasldkj", "Sam")
    assert "not sure i understand" in reply.lower()


def test_generate_response_joke_returns_known_joke():
    reply = chatbot.generate_response("tell me a joke", "Sam")
    assert reply in chatbot.JOKES


def test_generate_response_quote_returns_known_quote():
    reply = chatbot.generate_response("give me a quote", "Sam")
    assert reply in chatbot.QUOTES
