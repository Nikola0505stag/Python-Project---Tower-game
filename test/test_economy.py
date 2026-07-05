import unittest
from economy import Economy

class TestEconomy(unittest.TestCase):
    def setUp(self):
        self.eco = Economy()

    # starting values
    def test_starting_gold(self):
        self.assertEqual(self.eco.gold, 300)

    def test_starting_lives(self):
        self.assertEqual(self.eco.lives, 20)

    def test_starting_score(self):
        self.assertEqual(self.eco.score, 0)

    
    # can afford
    def test_can_afford_exact_amount(self):
        self.assertTrue(self.eco.can_afford(300))

    def test_can_afford_less_than_gold(self):
        self.assertTrue(self.eco.can_afford(100))

    def test_cannot_afford_more_than_gold(self):
        self.assertFalse(self.eco.can_afford(301))

    def test_cannot_afford_zero_gold(self):
        self.eco.spend(300)
        self.assertFalse(self.eco.can_afford(1))

    
    # spend
    def test_spend_deducts_gold(self):
        self.eco.spend(100)
        self.assertEqual(self.eco.gold, 200)

    def test_spend_returns_true_on_success(self):
        self.assertTrue(self.eco.spend(100))
    
    def test_spend_returns_false_when_too_poor(self):
        self.assertFalse(self.eco.spend(999))

    def test_spend_doest_not_deduct_when_too_poor(self):
        self.eco.spend(999)
        self.assertEqual(self.eco.gold, 300)

    def test_spend_exact_amout(self):
        self.eco.spend(300)
        self.assertEqual(self.eco.gold, 0)



if __name__ == '__main__':
    unittest.main()
