import unittest
from economy import Economy

class TestEconomy(unittest.TestCase):
    def setUp(self):
        self.eco = Economy()

    def test_starting_gold(self):
        self.assertEqual(self.eco.gold, 300)

    def test_starting_lives(self):
        self.assertEqual(self.eco.lives, 20)

    def test_starting_score(self):
        self.assertEqual(self.eco.score, 0)
