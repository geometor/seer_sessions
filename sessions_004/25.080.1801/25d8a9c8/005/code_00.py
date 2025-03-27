"""
Transforms an input grid by replacing the most frequent color in each row with 5 and all other colors with 0,
but only if the most frequent color occupies more than 50% of the row. Otherwise, the entire row is set to 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid based on the most frequent color in each row and its proportion.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.zeros_like(input_grid)

    for i, row in enumerate(input_grid):
        unique_colors, counts = np.unique(row, return_counts=True)
        most_frequent_color = unique_colors[np.argmax(counts)]
        most_frequent_count = np.max(counts)
        proportion = most_frequent_count / len(row)

        if proportion > 0.5:
            for j, color in enumerate(row):
                if color == most_frequent_color:
                    output_grid[i, j] = 5
                else:
                    output_grid[i, j] = 0  # Explicitly set other colors to 0
        else:
            output_grid[i, :] = 0  # Set the entire row to 0

    return output_grid