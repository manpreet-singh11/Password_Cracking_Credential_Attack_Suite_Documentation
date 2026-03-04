import unittest
from core.analyzer import PasswordAnalyzer

class TestEntropy(unittest.TestCase):
    def setUp(self):
        self.analyzer = PasswordAnalyzer()

    def test_empty_password(self):
        self.assertEqual(self.analyzer.calculate_entropy(""), 0)

    def test_entropy_growth(self):
        low_entropy = self.analyzer.calculate_entropy("abc")
        high_entropy = self.analyzer.calculate_entropy("aB1#")
        # Even though "abc" is shorter, "aB1#" uses 4 different pools
        self.assertGreater(high_entropy, low_entropy)

    def test_strength_rating(self):
        res = self.analyzer.analyze("123456")
        self.assertEqual(res['rating'], "Very Weak")

if __name__ == "__main__":
    unittest.main()