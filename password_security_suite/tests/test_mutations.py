import unittest
from core.dictionary_gen import DictionaryGenerator

class TestMutations(unittest.TestCase):
    def setUp(self):
        self.gen = DictionaryGenerator()

    def test_leet_transformation(self):
        word = "ace"
        results = self.gen.apply_leet_speak(word)
        # We expect variations like "4ce", "4c3", "ac3"
        self.assertIn("4c3", results)
        self.assertIn("ace", results)

    def test_base_variations(self):
        base = self.gen.generate_base_list(["test"])
        # Should include 'TEST', 'test', 'Test'
        self.assertTrue(len(base) >= 3)
        self.assertIn("TEST", base)

    def test_mutation_appends(self):
        mutated = self.gen.apply_mutations(["admin"], include_numbers=True)
        # Check if common number patterns are appended
        self.assertTrue(any("admin1" in m for m in mutated))

if __name__ == "__main__":
    unittest.main()