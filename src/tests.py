"""Test cases for the file processing algorithms."""

import unittest
from itertools import product

try:
    from .methods import (
        ProcessFilesBaseline,
        ProcessFilesGreedy,
        _average_completion_time,
    )
except ImportError:
    from methods import (
        ProcessFilesBaseline,
        ProcessFilesGreedy,
        _average_completion_time,
    )


class AverageCompletionTimeTests(unittest.TestCase):
    def test_empty_order(self):
        self.assertEqual(_average_completion_time([]), 0.0)

    def test_single_file(self):
        self.assertEqual(_average_completion_time([7]), 7.0)

    def test_cumulative_completion_times(self):
        # Files finish at 8, 11, 17, and 19, respectively.
        self.assertAlmostEqual(_average_completion_time([8, 3, 6, 2]), 13.75)

    def test_order_affects_average(self):
        self.assertAlmostEqual(_average_completion_time([1, 4]), 3.0)
        self.assertAlmostEqual(_average_completion_time([4, 1]), 4.5)


class FileOrderingTests(unittest.TestCase):
    algorithms = (ProcessFilesBaseline, ProcessFilesGreedy)

    def test_known_results(self):
        cases = [
            ("empty", [], [], 0.0),
            ("single", [7], [7], 7.0),
            # The example from planning.md: completion times 2, 5, 11, 19.
            ("planning example", [8, 3, 6, 2], [2, 3, 6, 8], 9.25),
            ("sorted", [1, 2, 3, 4], [1, 2, 3, 4], 5.0),
            ("reverse sorted", [4, 3, 2, 1], [1, 2, 3, 4], 5.0),
            ("duplicates", [3, 1, 3, 1], [1, 1, 3, 3], 4.0),
            ("all equal", [5, 5, 5], [5, 5, 5], 10.0),
            ("all zero", [0, 0, 0], [0, 0, 0], 0.0),
            ("mixed zero", [4, 0, 2], [0, 2, 4], 8 / 3),
            ("fractional", [1.5, 0.5, 1.0], [0.5, 1.0, 1.5], 5 / 3),
            ("large sizes", [10**12, 1], [1, 10**12], (10**12 + 2) / 2),
        ]
        for algorithm in self.algorithms:
            for name, sizes, expected_order, expected_average in cases:
                with self.subTest(algorithm=algorithm.__name__, case=name):
                    order, average = algorithm(sizes)
                    self.assertIsInstance(order, list)
                    self.assertEqual(order, expected_order)
                    self.assertAlmostEqual(average, expected_average)

    def test_input_is_preserved_and_output_is_a_new_list(self):
        for algorithm in self.algorithms:
            for sizes in ([], [1, 2, 3], [8, 3, 6, 2]):
                with self.subTest(algorithm=algorithm.__name__, sizes=sizes):
                    original = sizes.copy()
                    order, _ = algorithm(sizes)
                    self.assertEqual(sizes, original)
                    self.assertIsNot(order, sizes)
                    order.append(99)
                    self.assertEqual(sizes, original)

    def test_tuple_input(self):
        for algorithm in self.algorithms:
            with self.subTest(algorithm=algorithm.__name__):
                order, average = algorithm((3, 1, 2))
                self.assertEqual(order, [1, 2, 3])
                self.assertAlmostEqual(average, 10 / 3)

    def test_greedy_matches_exhaustive_baseline_on_small_inputs(self):
        # Bound the input length because the baseline examines n! orders.
        for size in range(5):
            for sizes in product((0, 1, 3), repeat=size):
                with self.subTest(sizes=sizes):
                    baseline_order, baseline_average = ProcessFilesBaseline(sizes)
                    greedy_order, greedy_average = ProcessFilesGreedy(sizes)
                    self.assertCountEqual(greedy_order, sizes)
                    self.assertEqual(greedy_order, baseline_order)
                    self.assertAlmostEqual(greedy_average, baseline_average)

    def test_greedy_handles_large_input(self):
        size = 10_000
        order, average = ProcessFilesGreedy(list(range(size, 0, -1)))
        self.assertEqual(order, list(range(1, size + 1)))
        # For 1 through n, the mean of the cumulative sums is (n+1)(n+2)/6.
        self.assertAlmostEqual(average, (size + 1) * (size + 2) / 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
