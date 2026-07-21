"""
================================================================================
 CodSoft AI Internship - Task 4: Movie Recommendation System
================================================================================
Author : (Your Name Here)
Description:
    A content-based movie recommendation system that suggests movies similar
    to a movie entered by the user. It uses TF-IDF (Term Frequency - Inverse
    Document Frequency) to convert movie text data (genre + tags) into
    numerical vectors, and Cosine Similarity to measure how similar movies
    are to each other.

    The system is fault-tolerant: if a user makes a spelling mistake while
    typing a movie name, it uses fuzzy string matching (difflib) to find the
    closest matching title in the dataset before generating recommendations.

Libraries used:
    - pandas        -> loading & handling the movie dataset
    - numpy         -> numerical operations on similarity scores
    - scikit-learn  -> TF-IDF Vectorizer & Cosine Similarity
    - difflib       -> built-in Python library for fuzzy text matching
================================================================================
"""

import os
import sys
import difflib

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movies.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
TOP_N_RECOMMENDATIONS = 5


# --------------------------------------------------------------------------
# TERMINAL UI HELPERS (for a "nice terminal output")
# --------------------------------------------------------------------------
class Colors:
    """ANSI escape codes to add color to terminal output."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def print_banner():
    """Prints a nice welcome banner for the application."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
==================================================================
       CODSOFT AI INTERNSHIP - TASK 4
       MOVIE RECOMMENDATION SYSTEM (Content-Based Filtering)
       Powered by TF-IDF + Cosine Similarity
==================================================================
{Colors.END}"""
    print(banner)


def print_divider():
    """Prints a simple horizontal divider line."""
    print(f"{Colors.BLUE}{'-' * 66}{Colors.END}")


# --------------------------------------------------------------------------
# CORE RECOMMENDATION ENGINE CLASS
# --------------------------------------------------------------------------
class MovieRecommender:
    """
    A content-based movie recommendation engine.

    The engine works in 3 conceptual steps:
        1. Text Vectorization : Convert each movie's genre + tags into a
           numerical TF-IDF vector.
        2. Similarity Computation : Compute Cosine Similarity between every
           pair of movie vectors to build a similarity matrix.
        3. Lookup & Ranking : Given a movie name (even a misspelled one),
           find the closest matching title, then look up its row in the
           similarity matrix and return the top-N most similar movies.
    """

    def __init__(self, data_path: str):
        """
        Initializes the recommender by loading data and preparing the model.

        Parameters
        ----------
        data_path : str
            Path to the movies.csv dataset file.
        """
        self.data_path = data_path
        self.df = None                 # Will hold the movie dataset (DataFrame)
        self.tfidf_matrix = None       # Will hold the TF-IDF vectors for all movies
        self.similarity_matrix = None  # Will hold pairwise cosine similarity scores
        self.titles = None             # Quick-access list of all movie titles

        self._load_data()
        self._build_model()

    # ----------------------------------------------------------------
    def _load_data(self):
        """
        Loads the movie dataset from a CSV file into a pandas DataFrame.

        The CSV is expected to have 3 columns:
            - title : Name of the movie
            - genre : Primary genre of the movie
            - tags  : Space separated keywords describing the movie
                      (used as the "content" for TF-IDF)

        Any missing values in 'genre' or 'tags' are replaced with an empty
        string so that the vectorizer does not crash on NaN values.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at: {self.data_path}")

        self.df = pd.read_csv(self.data_path)

        # Basic data cleaning: fill missing text fields with empty strings
        self.df["genre"] = self.df["genre"].fillna("")
        self.df["tags"] = self.df["tags"].fillna("")

        # Combine genre + tags into a single "content" column.
        # This combined text is what TF-IDF will actually analyze, since it
        # represents everything we know about the movie's theme/content.
        self.df["content"] = self.df["genre"] + " " + self.df["tags"]

        # Reset index to make sure row numbers are clean (0, 1, 2, ...)
        self.df.reset_index(drop=True, inplace=True)

        # Store a lowercase list of titles for fast fuzzy matching later
        self.titles = self.df["title"].tolist()

    # ----------------------------------------------------------------
    def _build_model(self):
        """
        Builds the TF-IDF matrix and the Cosine Similarity matrix.

        TF-IDF (Term Frequency - Inverse Document Frequency):
            Converts text into numbers by scoring each word in a document
            based on:
              - How often it appears in that document (Term Frequency)
              - How rare it is across all documents (Inverse Document
                Frequency)
            Common words that appear in almost every movie (like "the",
            "movie", "drama") get a LOW score, while distinctive words that
            help differentiate one movie from another get a HIGH score.
            The result is a matrix where each row is a movie, and each
            column is a unique word, with TF-IDF weight values as entries.

        Cosine Similarity:
            Once every movie is represented as a vector of numbers (its
            TF-IDF row), we measure how "similar" two movies are by
            calculating the cosine of the angle between their vectors.
            A cosine similarity of 1.0 means the movies are identical in
            content, while 0.0 means they share no common terms at all.
        """
        # stop_words='english' removes common English filler words
        # (the, is, and, a, ...) that add noise but no useful meaning.
        vectorizer = TfidfVectorizer(stop_words="english")

        # fit_transform learns the vocabulary from all movies AND converts
        # every movie's content into a TF-IDF vector, all in one step.
        self.tfidf_matrix = vectorizer.fit_transform(self.df["content"])

        # cosine_similarity computes pairwise similarity between every row
        # (movie) in the TF-IDF matrix, producing an N x N matrix where
        # cell [i, j] = similarity score between movie i and movie j.
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    # ----------------------------------------------------------------
    def find_closest_title(self, user_input: str):
        """
        Handles spelling mistakes by finding the closest matching movie
        title to whatever the user typed.

        Uses Python's built-in `difflib.get_close_matches`, which compares
        the user's input against every title in the dataset and returns
        the ones that are most similar (based on character sequence
        matching), even if the user mistyped a few letters.

        Parameters
        ----------
        user_input : str
            The (possibly misspelled) movie title typed by the user.

        Returns
        -------
        str or None
            The best-matching movie title from the dataset, or None if no
            reasonably close match was found.
        """
        user_input_clean = user_input.strip().lower()
        titles_lower = [t.lower() for t in self.titles]

        # cutoff=0.5 means only accept matches that are at least 50%
        # similar to the user's input; n=1 means we only want the single
        # best match.
        close_matches = difflib.get_close_matches(
            user_input_clean, titles_lower, n=1, cutoff=0.5
        )

        if not close_matches:
            return None

        # Map the lowercase match back to its original-case title
        matched_index = titles_lower.index(close_matches[0])
        return self.titles[matched_index]

    # ----------------------------------------------------------------
    def recommend(self, movie_name: str, top_n: int = TOP_N_RECOMMENDATIONS):
        """
        Generates the top-N most similar movies to a given movie name.

        Steps performed:
            1. Correct any spelling mistakes using find_closest_title().
            2. Locate that movie's row/index in the DataFrame.
            3. Pull that movie's similarity scores against every other
               movie from the precomputed similarity_matrix.
            4. Sort all movies by similarity score (highest first).
            5. Skip the movie itself (since it is always 100% similar to
               itself) and return the next `top_n` movies.

        Parameters
        ----------
        movie_name : str
            The movie title entered by the user (may contain typos).
        top_n : int
            Number of recommendations to return (default 5).

        Returns
        -------
        tuple (matched_title, recommendations)
            matched_title : str or None
                The corrected/matched title used for the search.
            recommendations : list of dict or None
                Each dict has keys: title, genre, similarity_score.
                Returns None if no match was found at all.
        """
        matched_title = self.find_closest_title(movie_name)

        if matched_title is None:
            return None, None

        # Find the row index of the matched movie in the DataFrame
        movie_index = self.df[self.df["title"] == matched_title].index[0]

        # Get similarity scores of this movie against all other movies.
        # enumerate() pairs each score with its movie index: (index, score)
        similarity_scores = list(enumerate(self.similarity_matrix[movie_index]))

        # Sort movies by similarity score in descending order (most similar first)
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        recommendations = []
        for idx, score in similarity_scores:
            # Skip the movie itself (it will always have similarity == 1.0)
            if idx == movie_index:
                continue
            if len(recommendations) >= top_n:
                break

            recommendations.append({
                "title": self.df.iloc[idx]["title"],
                "genre": self.df.iloc[idx]["genre"],
                "similarity_score": round(float(score), 4),
            })

        return matched_title, recommendations


# --------------------------------------------------------------------------
# OUTPUT / DISPLAY HELPERS
# --------------------------------------------------------------------------
def display_recommendations(original_input: str, matched_title: str, recommendations: list):
    """
    Neatly prints the recommendation results to the terminal in a
    formatted, easy-to-read table-like layout.

    Parameters
    ----------
    original_input : str
        The raw text the user typed in.
    matched_title : str
        The closest matching title found in the dataset.
    recommendations : list of dict
        The list of recommended movies with genre and similarity score.
    """
    print_divider()

    if matched_title.lower() != original_input.strip().lower():
        print(f"{Colors.YELLOW}Did you mean: '{matched_title}'? "
              f"Showing results for the closest match.{Colors.END}")
    else:
        print(f"{Colors.GREEN}Movie found: '{matched_title}'{Colors.END}")

    print_divider()
    print(f"{Colors.BOLD}Top {len(recommendations)} Movies Similar to "
          f"'{matched_title}':{Colors.END}\n")

    header = f"{'#':<3}{'Title':<45}{'Genre':<15}{'Similarity':>10}"
    print(f"{Colors.CYAN}{Colors.BOLD}{header}{Colors.END}")
    print(f"{Colors.CYAN}{'-' * len(header)}{Colors.END}")

    for i, movie in enumerate(recommendations, start=1):
        score_percent = f"{movie['similarity_score'] * 100:.2f}%"
        row = (f"{i:<3}{movie['title'][:43]:<45}{movie['genre']:<15}"
               f"{score_percent:>10}")
        print(row)

    print_divider()


def save_recommendations_to_file(original_input: str, matched_title: str,
                                  recommendations: list, output_dir: str):
    """
    Saves the recommendation results to a text file inside the output/
    folder, so users have a persistent record of past searches.

    Parameters
    ----------
    original_input : str
        The raw text the user typed in.
    matched_title : str
        The closest matching title found in the dataset.
    recommendations : list of dict
        The list of recommended movies with genre and similarity score.
    output_dir : str
        Folder path where the result file should be saved.
    """
    os.makedirs(output_dir, exist_ok=True)
    safe_name = "".join(c if c.isalnum() else "_" for c in matched_title)
    file_path = os.path.join(output_dir, f"recommendations_{safe_name}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Search Input     : {original_input}\n")
        f.write(f"Matched Movie    : {matched_title}\n")
        f.write(f"Top {len(recommendations)} Recommendations:\n")
        f.write("-" * 60 + "\n")
        for i, movie in enumerate(recommendations, start=1):
            f.write(f"{i}. {movie['title']} | Genre: {movie['genre']} | "
                    f"Similarity: {movie['similarity_score']}\n")

    print(f"{Colors.GREEN}Saved results to: {file_path}{Colors.END}")


def list_sample_titles(recommender: MovieRecommender, count: int = 10):
    """
    Prints a small sample of available movie titles, useful for helping
    the user know what kind of movies exist in the dataset.

    Parameters
    ----------
    recommender : MovieRecommender
        The initialized recommender object (holds the movie dataset).
    count : int
        Number of sample titles to display.
    """
    print(f"{Colors.YELLOW}Sample movies you can try:{Colors.END}")
    sample = recommender.df["title"].sample(min(count, len(recommender.df)), random_state=None)
    for title in sample:
        print(f"   - {title}")
    print()


# --------------------------------------------------------------------------
# MAIN PROGRAM LOOP
# --------------------------------------------------------------------------
def main():
    """
    Main entry point of the application.

    Loads the dataset, builds the recommendation model once, and then
    repeatedly prompts the user for a movie name until they choose to exit.
    """
    print_banner()

    try:
        recommender = MovieRecommender(DATA_PATH)
    except FileNotFoundError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        sys.exit(1)

    print(f"{Colors.GREEN}Dataset loaded successfully! "
          f"({len(recommender.df)} movies available){Colors.END}\n")

    list_sample_titles(recommender)

    while True:
        print_divider()
        user_input = input(
            f"{Colors.BOLD}Enter a movie name (or type 'exit' to quit): {Colors.END}"
        ).strip()

        if user_input.lower() in ("exit", "quit", "q"):
            print(f"\n{Colors.CYAN}Thank you for using the Movie "
                  f"Recommendation System. Goodbye!{Colors.END}\n")
            break

        if not user_input:
            print(f"{Colors.RED}Please enter a valid movie name.{Colors.END}")
            continue

        matched_title, recommendations = recommender.recommend(
            user_input, top_n=TOP_N_RECOMMENDATIONS
        )

        if matched_title is None:
            print(f"{Colors.RED}Sorry, no close match was found for "
                  f"'{user_input}'. Please check the spelling and try "
                  f"again.{Colors.END}")
            continue

        display_recommendations(user_input, matched_title, recommendations)

        save_choice = input(
            f"{Colors.BOLD}Save these results to a file? (y/n): {Colors.END}"
        ).strip().lower()
        if save_choice == "y":
            save_recommendations_to_file(
                user_input, matched_title, recommendations, OUTPUT_DIR
            )


if __name__ == "__main__":
    main()
