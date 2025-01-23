import unittest

def increment_dict_values(d, increment):
    return {k: v + increment for k, v in d.items()}

class TestIncrementDict(unittest.TestCase):
    def test_increment_dict_values(self):
        self.assertEqual(
            increment_dict_values({"a": 1, "b": 2}, 1), {"a": 2, "b": 3}
        )
        self.assertEqual(
            increment_dict_values({"x": 0, "y": -1}, 5), {"x": 5, "y": 4}
        )

# Run all the test cases
if __name__ == "__main__":
    unittest.main()