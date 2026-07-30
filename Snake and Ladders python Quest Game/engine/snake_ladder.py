import random

class GameEngine:
    # head: tail
    SNAKES = {16: 7, 60: 19, 63: 18, 67: 30, 87: 24, 93: 69, 95: 75, 98: 77}
    # bottom: top
    LADDERS = {8: 27, 23: 37, 25: 54, 28: 50, 56: 64, 68: 88, 76: 97, 81: 100}

    @staticmethod
    def roll_dice():
        return random.randint(1, 6)

    @classmethod
    def calculate_move(cls, current_pos, roll):
        new_pos = current_pos + roll
        
        if new_pos > 100:
            return current_pos, "stay", 0 # Can't move past 100
        
        event = "none"
        final_pos = new_pos
        
        if new_pos in cls.SNAKES:
            final_pos = cls.SNAKES[new_pos]
            event = "snake"
        elif new_pos in cls.LADDERS:
            final_pos = cls.LADDERS[new_pos]
            event = "ladder"
            
        return final_pos, event, new_pos # final, event_type, intermediate_pos
