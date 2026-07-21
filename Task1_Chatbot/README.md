# 🤖 PyBot — Rule-Based Terminal Chatbot

**CodSoft Artificial Intelligence Internship — Task 1**

PyBot is a beginner-to-intermediate level chatbot built entirely with core
Python. It uses **if-else logic, dictionaries, and string keyword
matching** to hold a conversation — no external AI APIs (OpenAI, Gemini,
Claude, etc.) are used anywhere in this project.

---

## ✨ Features

| Feature | Description |
|---|---|
| Welcome message | Greets the user when the program starts |
| Name memory | Asks for the user's name and uses it throughout the chat |
| Greetings | Responds to "hi", "hello", "hey", etc. |
| Wellbeing check | Responds to "how are you?" |
| Current date | Tells today's date |
| Current time | Tells the current system time |
| Jokes | Tells one of 5 programming jokes at random |
| Motivational quotes | Shares a random motivational quote |
| Calculator | Performs `+`, `-`, `*`, `/` on two numbers |
| Study tips | Shares college study tips |
| Programming tips | Shares coding best practices |
| Help menu | Lists all available commands |
| About | Explains what PyBot is |
| Exit | Responds to "bye" and ends the session politely |
| Fallback handling | Gracefully handles unrecognized input |

---

## 📁 Project Structure

```
Task1_Chatbot/
│
├── chatbot.py          # Main chatbot application
├── README.md            # Project documentation (this file)
├── requirements.txt     # Python dependencies (none required)
├── LICENSE               # MIT License
├── .gitignore            # Files/folders excluded from Git
├── screenshots/          # Demo screenshots for GitHub
└── output/               # Sample output logs
```

---

## 🚀 How to Run

1. **Install Python 3** (3.8 or higher recommended).
   Check your version:
   ```bash
   python3 --version
   ```

2. **Clone or download** this project folder.

3. **Navigate into the project folder:**
   ```bash
   cd Task1_Chatbot
   ```

4. **Run the chatbot:**
   ```bash
   python3 chatbot.py
   ```

5. Start chatting! Type `help` at any time to see available commands,
   and `bye` to exit.

No external libraries are required — the project only uses Python's
built-in `random` and `datetime` modules.

---

## 🧩 Function Overview

| Function | Purpose |
|---|---|
| `print_welcome()` | Displays the startup banner |
| `get_user_name()` | Prompts for and validates the user's name |
| `contains_any()` | Checks if input contains any keyword from a group |
| `get_current_time()` / `get_current_date()` | Return formatted date/time |
| `tell_joke()` / `tell_quote()` | Return a random joke/quote |
| `give_study_tip()` / `give_programming_tip()` | Return a random tip |
| `show_help()` / `show_about()` | Return static informational text |
| `is_math_expression()` | Detects whether input looks like a calculation |
| `calculate()` | Safely evaluates a two-number expression without `eval()` |
| `generate_response()` | Central router that matches input to the right reply |
| `main()` | Runs the welcome flow and the conversation loop |

The chatbot deliberately avoids Python's built-in `eval()` for
calculations, parsing the expression manually instead — this is safer
and demonstrates a better understanding of string handling.

---

## 📸 Suggested Screenshots for GitHub

Save these in the `screenshots/` folder and reference them in your
README or LinkedIn post:

1. Startup screen showing the welcome message and name prompt.
2. A greeting exchange ("hi" → chatbot's reply).
3. The chatbot telling a joke and a motivational quote.
4. A calculation example (e.g. `12 * 4`).
5. The `help` command output.
6. The exit message when typing `bye`.

---

## 🔮 Future Improvements

- Add **NLP-based intent matching** (e.g. using `nltk` or `spaCy`) instead
  of plain keyword matching.
- Support **multi-operand math expressions** (e.g. `2 + 3 * 4`).
- Add a **GUI** using Tkinter or a web interface using Flask/Streamlit.
- Store conversation history in a file for later review.
- Add **voice input/output** using `speech_recognition` and `pyttsx3`.
- Let users customize the joke/quote lists via an external JSON file.
- Add unit tests (`pytest`) for the response logic.

---

## 📝 License

This project is licensed under the MIT License — see [LICENSE](LICENSE)
for details.

---

## 🙌 Acknowledgements

Built as part of the **CodSoft Artificial Intelligence Internship**
(Task 1 — Rule-Based Chatbot).

`#codsoft` `#internship` `#artificialintelligence` `#python`
