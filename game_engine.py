import random

class GameEngine:
    def __init__(self, word_list_path: str = "words.txt"):
        with open(word_list_path, "r") as f:
            self.word_list = [line.strip().lower() for line in f if len(line.strip()) == 5]
        self.answer = ""
        self.guesses = []
        self.results = []
        self.is_won = False
        self.is_lost = False
        self.max_guesses = 6

    def start_game(self, answer: str = None):
        self.answer = answer if answer else random.choice(self.word_list)
        self.guesses = []
        self.results = []
        self.is_won = False
        self.is_lost = False

    def is_valid_word(self, word: str) -> bool:
        return word in self.word_list

    def score_guess(self, guess: str) -> list[str]:
        result = ["gray"] * 5
        answer_chars = list(self.answer)
        
        # Pass 1: Green
        for i in range(5):
            if guess[i] == answer_chars[i]:
                result[i] = "green"
                answer_chars[i] = None

        # Pass 2: Yellow
        for i in range(5):
            if result[i] != "green" and guess[i] in answer_chars:
                result[i] = "yellow"
                answer_chars[answer_chars.index(guess[i])] = None

        return result

    def make_guess(self, guess: str) -> dict:
        if self.is_won or self.is_lost:
            raise ValueError("Game is already finished")
        if len(guess) != 5 or not self.is_valid_word(guess):
            raise ValueError("Invalid word")

        result = self.score_guess(guess)
        self.guesses.append(guess)
        self.results.append(result)

        if guess == self.answer:
            self.is_won = True
        elif len(self.guesses) >= self.max_guesses:
            self.is_lost = True

        return {
            "guess": guess,
            "result": result,
            "is_won": self.is_won,
            "is_lost": self.is_lost,
            "guesses_remaining": self.max_guesses - len(self.guesses)
        }