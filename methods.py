"""Algorithms for ordering files to minimize average completion time."""

from collections.abc import Sequence
from itertools import permutations


def _average_completion_time(order: Sequence[float]) -> float:
    """Return the average cumulative processing time for an order."""
    if not order:
        return 0.0

    current_time = 0
    total_completion_time = 0
    for file_size in order:
        # Add this file's processing time to the queue.
        current_time += file_size
        # Record when this file finishes processing.
        total_completion_time += current_time

    return total_completion_time / len(order)


def ProcessFilesBaseline(file_sizes: Sequence[float]) -> tuple[list[float], float]:
    """Find the optimal order by checking every permutation.

    This baseline is factorial-time and is intended for correctness checks and
    small inputs.
    """
    if not file_sizes:
        return [], 0.0

    best_order = list(file_sizes)
    best_average = float("inf")

    # Check every possible file order.
    for order in permutations(file_sizes):
        average = _average_completion_time(order)
        # Keep the order with the smallest average wait time.
        if average < best_average:
            best_order = list(order)
            best_average = average

    return best_order, best_average


def ProcessFilesGreedy(file_sizes: Sequence[float]) -> tuple[list[float], float]:
    """Process files from smallest to largest for an optimal order."""
    # Shorter files should be processed first.
    order = sorted(file_sizes)
    return order, _average_completion_time(order)
