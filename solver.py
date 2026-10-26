import math
from collections import defaultdict

def compute_pattern(guess: str, answer: str) -> tuple:
    result = ["gray"] * 5
    ans_chars = list(answer)
    for i in range(5):
        if guess[i] == ans_chars[i]:
            result[i] = "green"
            ans_chars[i] = None
    for i in range(5):
        if result[i] != "green" and guess[i] in ans_chars:
            result[i] = "yellow"
            ans_chars[ans_chars.index(guess[i])] = None
    return tuple(result)

class Solver:
    def __init__(self, word_list: list[str]):
        self.word_list = word_list
        self.possible_words = list(word_list)

    def filter_words(self, guess: str, result: list[str]):
        result_tuple = tuple(result)
        self.possible_words = [
            w for w in self.possible_words 
            if compute_pattern(guess, w) == result_tuple
        ]

    def calculate_entropy(self, guess: str) -> float:
        pattern_counts = defaultdict(int)
        for target in self.possible_words:
            pattern = compute_pattern(guess, target)
            pattern_counts[pattern] += 1
        
        entropy = 0.0
        total_words = len(self.possible_words)
        for count in pattern_counts.values():
            prob = count / total_words
            entropy -= prob * math.log2(prob)
        return entropy

    def get_suggestions(self, top_n: int = 5) -> list[dict]:
        if len(self.possible_words) == 0:
            return []
        if len(self.possible_words) == 1:
            return [{"word": self.possible_words[0], "entropy": 0.0}]

        suggestions = []
        for word in self.possible_words:
            suggestions.append({
                "word": word,
                "entropy": self.calculate_entropy(word)
            })
        
        suggestions.sort(key=lambda x: x["entropy"], reverse=True)
        return suggestions[:top_n]