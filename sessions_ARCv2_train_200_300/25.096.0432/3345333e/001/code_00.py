"""
Identify the non-zero digit (color) that appears least frequently in the input grid.
Replace all instances of this least frequent digit with the background digit (0).
If there are fewer than two distinct non-zero digits, make no changes.
"""

import numpy as np
from collections import Counter

def find_unique_non_zero_values(grid: np.ndarray) -> list[int]:
    """Finds all unique non-zero integer values in the grid."""
    return np.unique(grid[grid != 0]).tolist()

def count_value_frequencies(grid: np.ndarray, values: list[int]) -> dict[int, int]:
    """Counts the frequency of specified values in the grid."""
    counts = Counter(grid.flatten())
    return {value: counts.get(value, 0) for value in values}

def find_min_frequency_value(frequencies: dict[int, int]) -> int | None:
    """Finds the value with the minimum frequency."""
    if not frequencies:
        return None
    # Find the minimum frequency
    min_freq = min(frequencies.values())
    # Find all values with that minimum frequency
    min_freq_values = [value for value, freq in frequencies.items() if freq == min_freq]
    # Return the numerically smallest value among those with the minimum frequency (handles ties)
    return min(min_freq_values)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Filters the input grid by removing the least frequent non-zero digit.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)

    # Find all unique non-zero digits (colors) in the grid
    unique_values = find_unique_non_zero_values(grid_np)

    # If there are less than two unique non-zero colors, no change is needed
    if len(unique_values) < 2:
        return input_grid # Return the original list of lists

    # Count the frequency of each unique non-zero color
    frequencies = count_value_frequencies(grid_np, unique_values)

    # Find the color with the minimum frequency
    value_to_remove = find_min_frequency_value(frequencies)

    # If for some reason no value is found (e.g., empty frequencies), return original
    if value_to_remove is None:
         return input_grid

    # Create the output grid by copying the input array
    output_grid_np = grid_np.copy()

    # Replace all occurrences of the least frequent color with 0 (background)
    output_grid_np[output_grid_np == value_to_remove] = 0

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid