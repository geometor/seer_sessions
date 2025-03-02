"""
The program analyzes an input grid, counts the occurrences of each color (excluding 0), and outputs a 1x1 grid containing the most frequent color.
"""

import numpy as np
from collections import Counter

def get_most_common_color(counts):
    """Return most frequent color ignoring 0"""
    filtered_counts = {k:v for (k,v) in counts.items() if k != 0}
    if not filtered_counts:
        return 0
    most_common = Counter(filtered_counts).most_common(1)
    if most_common:
        return most_common[0][0]
    return 0

def transform(input_grid):
    """
    Transforms the input grid to a 1x1 output grid with the most frequent color (excluding 0).
    """
    # Count the occurrences of each color in the input grid.
    color_counts = Counter(input_grid.flatten())

    # Find the most frequent color, excluding 0.
    most_frequent_color = get_most_common_color(color_counts)

    # Create a 1x1 output grid.
    output_grid = np.zeros((1, 1), dtype=int)

    # Set the output grid's pixel to the most frequent color.
    output_grid[0, 0] = most_frequent_color

    return output_grid