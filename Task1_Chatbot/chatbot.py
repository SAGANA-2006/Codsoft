"""
chatbot.py

A simple rule-based chatbot built with core Python.
No external AI APIs are used — all responses are generated using
if-else logic, dictionaries, and basic string matching.

Author: <Your Name>
Project: CodSoft AI Internship - Task 1
"""

import random
import datetime


# ---------------------------------------------------------------------------
# STATIC DATA (jokes, quotes, tips, etc.)
# ---------------------------------------------------------------------------

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the computer go to therapy? It had too many unresolved issues.",
    "Why do Java developers wear glasses? Because they don't see sharp.",
    "How many programmers does it take to change a light bulb? "
    "None, that's a hardware problem.",
    "I told my computer I needed a break, and it froze.",
]

QUOTES = [
    "Success is not final, failure is not fatal: it is the courage to "
    "continue that counts. - Winston Churchill",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "It always seems impossible until it's done. - Nelson Mandela",
]

STUDY_TIPS = [
    "Break your study sessions into 25-minute focused blocks (Pomodoro "
    "Technique) followed by a 5-minute break.",
    "Teach a concept to someone else — it's one of the fastest ways to "
    "confirm you understand it.",
    "Revise your notes within 24 hours of a lecture to boost retention.",
    "Avoid multitasking while studying; it reduces focus and slows "
    "learning.",
    "Practice past question papers to get comfortable with exam patterns.",
]

PROGRAMMING_TIPS = [
    "Write small, testable functions instead of one giant block of code.",
    "Comment your code, but let clear naming do most of the explaining.",
    "Use version control (Git) from day one, even for small projects.",
    "Read error messages carefully — they usually tell you exactly what "
    "went wrong.",
    "Practice consistently; coding is a skill built through repetition.",
]

# Keywords mapped to simple response categories.
GREETING_KEYWORDS = ("hi", "hello", "hey", "hola", "greetings")
WELLBEING_KEYWORDS = ("how are you", "how're you", "how you doing")
EXIT_KEYWORDS = ("bye", "exit", "quit", "goodbye")
HELP_KEYWORDS = ("help", "what can you do", "commands")
ABOUT_KEYWORDS = ("about", "who are you", "what are you")
JOKE_KEYWORDS = ("joke", "make me laugh", "funny")
QUOTE_KEYWORDS = ("quote", "motivate", "motivation", "inspire")
TIME_KEYWORDS = ("time", "what time is it", "current time")
DATE_KEYWORDS = ("date", "what day is it", "today's date")
STUDY_KEYWORDS = ("study tip", "study tips", "how to study")
PROGRAMMING_KEYWORDS = ("programming tip", "coding tip", "code tip")


# ---------------------------------------------------------------------------
# CORE HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def print_welcome() -> None:
    """Display a welcome banner when the chatbot starts."""
    print("=" * 55)
    print("        WELCOME TO PYBOT - YOUR TERMINAL ASSISTANT")
    print("=" * 55)
    print("Type 'help' to see what I can do, or 'bye' to exit.\n")


def get_user_name() -> str:
    """
    Ask the user for their name and return it.

    Keeps asking until a non-empty response is provided.
    """
    name = ""
    while not name.strip():
        name = input("PyBot: Before we start, what's your name? \nYou: ")
        if not name.strip():
            print("PyBot: I didn't quite catch that. Please tell me your "
                  "name.")
    return name.strip().title()


def contains_any(user_input: str, keywords: tuple) -> bool:
    """
    Check whether the user's input contains any of the given keywords.

    Args:
        user_input: The lowercased user message.
        keywords: A tuple of keyword strings to look for.

    Returns:
        True if any keyword is found in the input, else False.
    """
    return any(keyword in user_input for keyword in keywords)


def get_current_time() -> str:
    """Return the current system time as a formatted string."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")


def get_current_date() -> str:
    """Return the current system date as a formatted string."""
    today = datetime.datetime.now()
    return today.strftime("%A, %d %B %Y")


def tell_joke() -> str:
    """Return a random joke from the JOKES list."""
    return random.choice(JOKES)


def tell_quote() -> str:
    """Return a random motivational quote from the QUOTES list."""
    return random.choice(QUOTES)


def give_study_tip() -> str:
    """Return a random college study tip."""
    return random.choice(STUDY_TIPS)


def give_programming_tip() -> str:
    """Return a random programming tip."""
    return random.choice(PROGRAMMING_TIPS)


def show_help() -> str:
    """Return a formatted string listing available chatbot commands."""
    return (
        "Here's what I can help you with:\n"
        "  - Say hi/hello to greet me\n"
        "  - Ask 'how are you?'\n"
        "  - Ask for the 'time' or 'date'\n"
        "  - Ask for a 'joke'\n"
        "  - Ask for a 'quote'\n"
        "  - Ask for 'study tips' or 'programming tips'\n"
        "  - Give me a math expression, e.g. '12 * 4' or '15 / 3'\n"
        "  - Type 'about' to learn about me\n"
        "  - Type 'bye' to end our chat"
    )


def show_about() -> str:
    """Return a short description of the chatbot."""
    return (
        "I'm PyBot, a rule-based chatbot built with pure Python for the "
        "CodSoft AI Internship (Task 1). I don't use any external AI "
        "APIs — just good old if-else logic and string matching!"
    )


def is_math_expression(user_input: str) -> bool:
    """
    Roughly determine if the input looks like a math expression.

    A valid expression should contain only digits, spaces, decimal
    points, and one of the supported operators (+, -, *, /).
    """
    operators = ("+", "-", "*", "/")
    if not any(op in user_input for op in operators):
        return False
    allowed_chars = set("0123456789+-*/. ")
    return all(char in allowed_chars for char in user_input)


def calculate(expression: str) -> str:
    """
    Safely evaluate a simple two-operand math expression.

    Supports +, -, *, / between two numbers only (no chained
    expressions), to keep parsing simple and avoid using eval().

    Args:
        expression: A string like "12 * 4".

    Returns:
        A human-readable result string, or an error message if the
        expression could not be parsed or evaluated.
    """
    operators = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }

    for symbol, operation in operators.items():
        if symbol in expression:
            parts = expression.split(symbol)
            if len(parts) != 2:
                # More than one operator found; not supported.
                continue
            try:
                num1 = float(parts[0].strip())
                num2 = float(parts[1].strip())
            except ValueError:
                return ("I couldn't read that as numbers. Try something "
                        "like '10 + 5'.")

            if symbol == "/" and num2 == 0:
                return "I can't divide by zero — that breaks the universe!"

            result = operation(num1, num2)
            # Show whole numbers without a trailing .0
            if result == int(result):
                result = int(result)
            return f"The answer is {result}"

    return "I couldn't understand that calculation. Try '8 * 3' style input."


# ---------------------------------------------------------------------------
# RESPONSE ROUTER
# ---------------------------------------------------------------------------

def generate_response(user_input: str, user_name: str) -> str:
    """
    Decide which reply to give based on keywords found in user_input.

    This is the central rule-based decision function. It checks the
    cleaned user input against known keyword groups in a fixed order
    and returns the matching response.

    Args:
        user_input: Raw text typed by the user.
        user_name: The name the user gave earlier, used for personalization.

    Returns:
        The chatbot's reply as a string.
    """
    text = user_input.lower().strip()

    if not text:
        return "Please type something so I can help you."

    if contains_any(text, EXIT_KEYWORDS):
        return f"Goodbye, {user_name}! It was great chatting with you. 👋"

    if contains_any(text, HELP_KEYWORDS):
        return show_help()

    if contains_any(text, ABOUT_KEYWORDS):
        return show_about()

    if contains_any(text, WELLBEING_KEYWORDS):
        return "I'm just a bunch of if-else statements, but I'm doing " \
               "great! How about you?"

    if contains_any(text, GREETING_KEYWORDS):
        return f"Hello again, {user_name}! How can I help you today?"

    if contains_any(text, TIME_KEYWORDS):
        return f"The current time is {get_current_time()}."

    if contains_any(text, DATE_KEYWORDS):
        return f"Today's date is {get_current_date()}."

    if contains_any(text, JOKE_KEYWORDS):
        return tell_joke()

    if contains_any(text, QUOTE_KEYWORDS):
        return tell_quote()

    if contains_any(text, STUDY_KEYWORDS):
        return give_study_tip()

    if contains_any(text, PROGRAMMING_KEYWORDS):
        return give_programming_tip()

    if is_math_expression(text):
        return calculate(text)

    return ("I'm not sure I understand. Type 'help' to see what I can "
            "do, " + user_name + ".")


# ---------------------------------------------------------------------------
# MAIN PROGRAM LOOP
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the chatbot's main conversation loop."""
    print_welcome()

    try:
        user_name = get_user_name()
    except (KeyboardInterrupt, EOFError):
        print("\nPyBot: Session interrupted. Goodbye!")
        return

    print(f"\nPyBot: Nice to meet you, {user_name}! Let's chat.\n")

    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nPyBot: Session interrupted. Goodbye!")
            break

        response = generate_response(user_input, user_name)
        print(f"PyBot: {response}\n")

        if contains_any(user_input.lower().strip(), EXIT_KEYWORDS):
            break


if __name__ == "__main__":
    main()
