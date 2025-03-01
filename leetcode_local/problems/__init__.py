from enum import Enum

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class Problem:
    def __init__(self, id, title, description, examples, constraints, difficulty, category, function_name):
        self.id = id
        self.title = title
        self.description = description
        self.examples = examples
        self.constraints = constraints
        self.difficulty = difficulty
        self.category = category
        self.function_name = function_name
        
    def __str__(self):
        return f"Problem {self.id}: {self.title} ({self.difficulty.name})"