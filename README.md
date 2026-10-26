# Wordle Lab

A full-featured local web application for playing Wordle, complete with an information-theory based solver and a modern, polished user interface.

## Features

* **Authentic UI:** Dark mode aesthetic, responsive on-screen keyboard with color tracking, 3D tile flip animations, and toast notifications.
* **Smart Solver:** Calculates the entropy of remaining possible words to suggest the mathematically optimal next guess.
* **Dynamic Word Validation:** Uses your local `words.txt` for the game's answers, but transparently falls back to the Datamuse API to validate and allow any real English 5-letter word you type.
* **Robust Backend:** Built with Python 3.12, FastAPI, and the `requests` library.

## Setup Instructions (Local)

1. Ensure you have `uv` installed.
2. Ensure you have Python 3.12 installed.
3. Make sure your `words.txt` file is populated with a list of valid 5-letter words (one per line, lowercase).
4. Install dependencies and run the server:
   ```bash
   uv venv --python 3.12
   source .venv/bin/activate
   uv pip install -e .
   uvicorn app:app --reload
   ```
5. Open `http://localhost:8000` in your web browser.

## Setup Instructions (Docker)

If you are running via Docker (or GitHub Codespaces), you can build and run the container directly without installing local Python dependencies:

1. Build the image:
   ```bash
   docker build -t wordle-lab .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 wordle-lab
   ```
3. Open `http://localhost:8000` in your web browser.