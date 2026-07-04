from settings import STARTING_GOLD, STARTING_LIVES

class Economy:
    def __init__(self):
        self.gold = STARTING_GOLD
        self.lives = STARTING_LIVES
        self.score = 0

    def can_afford(self, amount):
        return self.gold >= amount

    def spend(self, amount):
        if self.can_afford(amount):
            self.gold -= amount
            return True
        return False

    def earn(self, amount):
        self.gold += amount
        self.score += amount

    def lose_life(self, count=1):
        self.lives -= count

    def is_game_ofer(self):
        return self.lives <= 0
