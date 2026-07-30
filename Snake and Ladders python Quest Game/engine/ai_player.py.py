import random

class AIPlayer:
    @staticmethod
    def get_decision(difficulty):
        # Probability of AI answering correctly based on difficulty
        thresholds = {"Beginner": 0.75, "Intermediate": 0.60, "Advanced": 0.45}
        accuracy = thresholds.get(difficulty, 0.5)
        return random.random() < accuracy