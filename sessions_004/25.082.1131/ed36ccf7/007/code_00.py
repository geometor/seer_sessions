"""
The transformation operates on each column independently.  Within each column:

1.  **Identify the most frequent color.** If there's a tie, prioritize the color that appears *first* in the input column, reading from top to bottom.
2. **Replace all other colors in that column with the most frequent color.**

This process is applied to every column in the input grid to produce the output grid.
"""

import numpy as np

def _get_most_frequent_color(column):
    """Finds the most frequent color in a column, prioritizing the first in case of a tie."""
    counts = np.bincount(column)
    max_count = np.max(counts)
    most_frequent_colors = np.where(counts == max_count)[0]
    if len(most_frequent_colors) > 1:
        # Tiebreaker: Return the first color encountered
        for val in column:
          if val in most_frequent_colors:
            return val
    return most_frequent_colors[0]

def transform(input_grid):
    """
    Transforms the input grid by replacing each column with its most frequent color.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Start with a copy of the input

    # Iterate through each column
    for j in range(cols):
        column = input_grid[:, j]
        most_frequent = _get_most_frequent_color(column)

        # Replace all colors in the column with the most frequent color
        output_grid[:, j] = most_frequent

    return output_grid.tolist()