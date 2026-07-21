# 🎬 Task 4 — Movie Recommendation System

**CodSoft Artificial Intelligence Internship — Task 4**

A **content-based movie recommendation system** built in Python. The user
types the name of a movie they like, and the system recommends the **Top 5
most similar movies**, complete with genre and similarity score — all
displayed in a clean, colorful terminal interface. It even understands
**spelling mistakes**, so "Interstellarr" or "Dark Knigt" still works.

---

## 📌 Table of Contents

- [Demo](#-demo)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Understanding TF-IDF](#-understanding-tf-idf)
- [Understanding Cosine Similarity](#-understanding-cosine-similarity)
- [Function-by-Function Explanation](#-function-by-function-explanation)
- [Installation & Usage](#-installation--usage)
- [Sample Run](#-sample-run)
- [Dataset](#-dataset)
- [Future Improvements](#-future-improvements)
- [Screenshot Suggestions (for GitHub)](#-screenshot-suggestions-for-github)
- [License](#-license)

---

## 🎥 Demo

```
Enter a movie name (or type 'exit' to quit): Interstellarr

Did you mean: 'Interstellar'? Showing results for the closest match.
------------------------------------------------------------------
Top 5 Movies Similar to 'Interstellar':

#  Title                                        Genre          Similarity
-------------------------------------------------------------------------
1  Back to the Future                           Sci-Fi             51.29%
2  Alien                                        Sci-Fi             47.04%
3  Gravity                                      Sci-Fi             45.36%
4  Aliens                                       Sci-Fi             44.21%
5  The Martian                                  Sci-Fi             43.66%
```

---

## ✨ Features

| Feature                          | Description                                                                 |
|-----------------------------------|-------------------------------------------------------------------------------|
| 🔎 Free-text movie search         | Just type a movie name — no need for exact IDs.                              |
| ✍️ Spelling-mistake tolerant       | Uses fuzzy matching (`difflib`) to correct typos automatically.              |
| 🎯 Top 5 similar movies           | Returns the 5 most content-similar movies using Cosine Similarity.           |
| 🏷️ Genre display                  | Every recommendation shows its genre.                                       |
| 📊 Similarity score                | Every recommendation shows a % similarity score.                            |
| 🎨 Nice terminal UI               | Colored, table-style, easy-to-read output.                                  |
| 💾 Save results                   | Optionally saves recommendations to a text file in `output/`.               |
| 📦 100+ movie dataset             | A hand-curated dataset spanning 18 genres.                                  |
| 🧩 Clean, modular, OOP code       | Beginner-friendly, fully commented, interview-ready.                        |

---

## 📁 Project Structure

```
Task4_RecommendationSystem/
│
├── recommendation.py     # Main source code (recommendation engine + CLI)
├── movies.csv             # Sample dataset of 149 movies (title, genre, tags)
├── README.md               # Project documentation (this file)
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
├── .gitignore               # Files/folders excluded from Git
├── screenshots/            # Store terminal screenshots here for GitHub
└── output/                 # Saved recommendation results (.txt) get written here
```

---

## ⚙️ How It Works

The system follows a classic **content-based filtering** pipeline:

```
movies.csv
    │
    ▼
Combine "genre" + "tags" into one text column ("content")
    │
    ▼
TF-IDF Vectorizer  ── converts text → numeric vectors
    │
    ▼
Cosine Similarity  ── compares every movie vector to every other movie vector
    │
    ▼
User types a movie name
    │
    ▼
Fuzzy match (difflib) corrects typos → exact title found
    │
    ▼
Look up that movie's similarity row → sort → return Top 5
    │
    ▼
Nicely formatted terminal output (title, genre, similarity %)
```

Because this is **content-based filtering** (as opposed to collaborative
filtering), the system doesn't need any user ratings or history — it only
needs the *content/description* of each movie, which makes it perfect for a
small, self-contained dataset like this one.

---

## 🧠 Understanding TF-IDF

**TF-IDF** stands for **Term Frequency – Inverse Document Frequency**. It is
a way of converting text into numbers so that a machine learning algorithm
can understand and compare them mathematically.

It's made of two parts multiplied together:

1. **Term Frequency (TF)** — How often does a word appear in *this*
   document (movie)?
   ```
   TF(word, doc) = (Number of times word appears in doc) / (Total words in doc)
   ```

2. **Inverse Document Frequency (IDF)** — How rare is this word across
   *all* documents (movies)? Common words like "action" or "drama" that
   appear in many movies get a **low** IDF score (they carry little
   distinguishing power). Rare, specific words like "wormhole" or
   "holocaust" get a **high** IDF score (they carry a lot of distinguishing
   power).
   ```
   IDF(word) = log( Total number of documents / Number of documents containing word )
   ```

3. **TF-IDF score** = `TF × IDF`

**Why use it here?** If we just counted word frequency (Bag-of-Words),
generic words that appear everywhere (like "drama" or "action") would
dominate the comparison and make *every* movie look similar. TF-IDF
automatically down-weights those generic words and up-weights the words that
actually make a movie unique — giving us far more meaningful similarity
scores.

In this project, `TfidfVectorizer` from scikit-learn is applied to a
combined `genre + tags` string for every movie, producing a matrix where:
- Each **row** = one movie
- Each **column** = one unique word from the entire vocabulary
- Each **cell** = the TF-IDF weight of that word for that movie

---

## 📐 Understanding Cosine Similarity

Once every movie is represented as a **vector** of TF-IDF numbers, we need a
way to measure how "close" two movies are to each other. **Cosine
Similarity** does exactly that by measuring the **angle** between two
vectors, rather than their raw distance.

```
                A · B
cos(θ)  =  ─────────────
             ||A|| ||B||
```

Where:
- `A · B` is the dot product of vectors A and B
- `||A||` and `||B||` are the magnitudes (lengths) of each vector

The result is always a number between **0 and 1**:
- **1.0** → the two movies point in exactly the same direction (i.e., they
  use very similar words/genres — extremely similar content)
- **0.0** → the two movies share no common terms at all (completely
  unrelated content)

**Why cosine similarity instead of Euclidean distance?** Movie description
vectors can vary a lot in length (some movies have longer tag lists than
others). Cosine similarity ignores magnitude and only cares about
*direction* — i.e., whether the same words show up in similar proportions —
which makes it much more robust for text-based comparisons than raw
distance metrics.

In this project, `cosine_similarity()` from scikit-learn is applied to the
entire TF-IDF matrix at once, producing an **N × N similarity matrix**
where cell `[i, j]` holds the similarity score between movie `i` and movie
`j`.

---

## 🧩 Function-by-Function Explanation

### `class Colors`
A small utility class holding ANSI escape codes so terminal text can be
printed in color (green for success, yellow for warnings, red for errors,
etc.), making the CLI experience much nicer.

### `print_banner()`
Prints an eye-catching welcome banner when the program starts.

### `print_divider()`
Prints a horizontal line to visually separate sections of output.

### `class MovieRecommender`
The heart of the project — encapsulates all data loading, model building,
and recommendation logic in one clean, reusable object.

- **`__init__(self, data_path)`**
  Constructor. Stores the dataset path and immediately calls
  `_load_data()` and `_build_model()` so the recommender is fully ready to
  use as soon as it's created.

- **`_load_data(self)`**
  Reads `movies.csv` into a pandas DataFrame, fills any missing genre/tag
  values with empty strings (so nothing crashes), and creates a combined
  `content` column (`genre + tags`) — this combined text is what the model
  will actually "read" to understand each movie.

- **`_build_model(self)`**
  Creates a `TfidfVectorizer` (ignoring common English stop-words like
  "the", "a", "is"), fits it on the `content` column to build the TF-IDF
  matrix, then computes the full pairwise `cosine_similarity` matrix
  between every movie. This is the "training" step — it only needs to run
  once when the program starts.

- **`find_closest_title(self, user_input)`**
  Handles **spelling mistakes**. Uses Python's built-in
  `difflib.get_close_matches()` to compare the user's (possibly misspelled)
  input against every movie title in the dataset and returns the closest
  match, if any exists above a similarity cutoff of 0.5 (50%).

- **`recommend(self, movie_name, top_n=5)`**
  The main recommendation function. It:
  1. Corrects typos via `find_closest_title()`.
  2. Finds that movie's row index in the DataFrame.
  3. Pulls its precomputed similarity scores against every other movie.
  4. Sorts those scores from highest to lowest.
  5. Skips the movie itself (since its similarity to itself is always 1.0)
     and returns the next `top_n` movies as a list of dictionaries
     (`title`, `genre`, `similarity_score`).

### `display_recommendations(original_input, matched_title, recommendations)`
Formats and prints the final results as a clean table in the terminal,
including a friendly "Did you mean...?" message if the user's spelling was
corrected.

### `save_recommendations_to_file(original_input, matched_title, recommendations, output_dir)`
Optionally writes the recommendation results to a `.txt` file inside the
`output/` folder, so the user has a saved record of past searches.

### `list_sample_titles(recommender, count=10)`
Displays a handful of random example movie titles at startup so the user
knows what kind of movies they can search for.

### `main()`
The entry point that ties everything together: prints the banner, loads
the dataset, builds the model, shows sample titles, and then loops
indefinitely — accepting movie names, generating recommendations, and
optionally saving results — until the user types `exit`.

---

## 🚀 Installation & Usage

### 1. Clone or download this folder
```bash
git clone <your-repo-url>
cd Task4_RecommendationSystem
```

### 2. (Optional but recommended) Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the program
```bash
python recommendation.py
```

### 5. Try it out
```
Enter a movie name (or type 'exit' to quit): The Dark Knigt
```
Even with the typo, it will correctly detect **"The Dark Knight"** and
recommend 5 similar action movies.

---

## 🖥️ Sample Run

```
==================================================================
       CODSOFT AI INTERNSHIP - TASK 4
       MOVIE RECOMMENDATION SYSTEM (Content-Based Filtering)
       Powered by TF-IDF + Cosine Similarity
==================================================================

Dataset loaded successfully! (149 movies available)

Sample movies you can try:
   - Guardians of the Galaxy
   - The Imitation Game
   - The Departed
   ...

------------------------------------------------------------------
Enter a movie name (or type 'exit' to quit): Interstellarr
------------------------------------------------------------------
Did you mean: 'Interstellar'? Showing results for the closest match.
------------------------------------------------------------------
Top 5 Movies Similar to 'Interstellar':

#  Title                                        Genre          Similarity
-------------------------------------------------------------------------
1  Back to the Future                           Sci-Fi             51.29%
2  Alien                                        Sci-Fi             47.04%
3  Gravity                                      Sci-Fi             45.36%
4  Aliens                                       Sci-Fi             44.21%
5  The Martian                                  Sci-Fi             43.66%
------------------------------------------------------------------
Save these results to a file? (y/n): n
```

---

## 🎞️ Dataset

`movies.csv` contains **149 well-known movies** spanning **18 genres**
(Action, Drama, Sci-Fi, Crime, Thriller, Fantasy, Animation, Horror,
Romance, Musical, Biography, Sports, Adventure, War, Mystery, Western,
Family, Comedy). Each row has:

| Column | Description                                              |
|--------|-----------------------------------------------------------|
| `title` | The movie's name                                          |
| `genre` | The primary genre                                          |
| `tags`  | Space-separated keywords describing plot, theme, and mood — this is the "content" used by TF-IDF |

You can freely **add your own movies** to `movies.csv` — just follow the
same 3-column format, and the model will automatically pick them up the
next time the script runs (no code changes required).

---

## 🔮 Future Improvements

- 🌐 **Web interface** — wrap this in a Flask/Streamlit app for a
  point-and-click UI instead of the terminal.
- 🤝 **Hybrid recommendations** — combine this content-based approach with
  collaborative filtering (based on user ratings) for even better results.
- 🎭 **Multi-genre support** — allow movies to belong to multiple genres
  instead of just one primary genre.
- 🧠 **Better NLP features** — use word embeddings (Word2Vec, GloVe, or
  Sentence-BERT) instead of TF-IDF to capture deeper semantic meaning
  (e.g. understanding that "murder" and "homicide" are related).
- 🎬 **Real-world dataset integration** — connect to a live dataset such as
  TMDB or MovieLens for thousands of real movies with posters and plot
  summaries.
- 🖼️ **Poster previews** — fetch and display movie posters using a public
  movie API alongside each recommendation.
- 📈 **Evaluation metrics** — add precision/recall style evaluation against
  known "similar movie" ground truth data.
- 🗣️ **Voice input** — allow users to speak the movie name instead of
  typing it.
- 🧵 **Caching** — persist the TF-IDF/similarity matrix to disk so it
  doesn't need to be recomputed every time the script restarts.

---

## 📸 Screenshot Suggestions (for GitHub)

Save these into the `screenshots/` folder and embed them in your GitHub
repo's README for a polished presentation:

1. **`startup_banner.png`** — the colorful welcome banner and sample movie
   list shown right when the program starts.
2. **`spelling_correction.png`** — a search with an intentional typo (e.g.
   "Interstellarr") showing the "Did you mean...?" message.
3. **`recommendations_table.png`** — the formatted Top-5 output table with
   genres and similarity percentages clearly visible.
4. **`save_to_file.png`** — the terminal after choosing "y" to save
   results, showing the confirmation message and file path.
5. **`output_file_contents.png`** — the contents of a generated
   `output/recommendations_*.txt` file opened in a text editor.
6. **`code_structure.png`** — a screenshot of the project folder structure
   in VS Code's file explorer, showing all the required files.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE)
file for details.

---

### 🙌 Acknowledgements

Built as part of the **CodSoft Artificial Intelligence Internship**,
Task 4: *Movie Recommendation System*.
