# Changelog

All notable changes to PyBot will be documented in this file.

## [1.0.0] - Initial Release

### Added
- Rule-based response engine (`generate_response`) using keyword matching.
- Greeting, wellbeing, help, about, and exit intents.
- Time and date lookup.
- Random jokes and motivational quotes.
- Study tips and programming tips.
- Two-operand calculator (`+`, `-`, `*`, `/`) without `eval()`.
- Personalized responses using the user's name.
- Unit tests covering keyword matching, the calculator, and response
  routing (`tests/test_chatbot.py`).
- GitHub Actions workflow to run tests automatically on push/PR.
