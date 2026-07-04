from settings import STARTING_GOLD

class Economy:
    def __init__(self):
        self.gold = STARTING_GOLD

    def can_afford(self, amount):
        return self.gold >= amount

    def spend(self, amount):
        if self.can_afford(amount):
            self.gold -= amount
            return True
        return False

    def earn(self, amount):
        self.gold += amount
