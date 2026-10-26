import requests
import urllib3
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from game_engine import GameEngine
from solver import Solver

# Suppress the warning that appears when we bypass SSL verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()
game = GameEngine()

class GuessRequest(BaseModel):
    word: str

def is_valid_dictionary_word(word: str) -> bool:
    try:
        # Datamuse API rarely blocks cloud datacenter IPs
        response = requests.get(
            f"https://api.datamuse.com/words?sp={word}&max=1",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            # Confirm the API returned an exact match for the word
            if data and data[0].get("word") == word:
                return True
        else:
            print(f"API rejected request with status: {response.status_code}")
        return False
    except requests.RequestException as e:
        print(f"Datamuse API Connection Error: {e}")
        return False

@app.post("/api/start")
def start_game():
    game.start_game()
    return {"message": "Game started", "word_length": 5, "max_guesses": 6}

@app.post("/api/guess")
def submit_guess(request: GuessRequest):
    word = request.word.strip().lower()
    
    if len(word) != 5:
        raise HTTPException(status_code=400, detail="Word must be exactly 5 letters")

    # Check against local list first, fallback to external API
    if not game.is_valid_word(word):
        if is_valid_dictionary_word(word):
            # Temporarily add it to the local word list so the game engine accepts it
            game.word_list.append(word)
        else:
            raise HTTPException(status_code=400, detail="Invalid word")

    try:
        status = game.make_guess(word)
        return status
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/hint")
def get_hint():
    if game.is_won or game.is_lost:
        raise HTTPException(status_code=400, detail="Game over")
        
    solver = Solver(game.word_list)
    for guess, result in zip(game.guesses, game.results):
        solver.filter_words(guess, result)
        
    return {
        "words_remaining": len(solver.possible_words),
        "suggestions": solver.get_suggestions(top_n=5)
    }

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")