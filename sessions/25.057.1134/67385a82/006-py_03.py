"""
Identifies single-pixel color transformations between input and output grids.
The primary confirmed rule is changing green (3) to azure (8).
This code also attempts to identify other single-pixel color transformations.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Apply the confirmed green-to-azure rule
    for i in range(rows):
        for j in range(cols):
            if output_grid[i, j] == 3:
                output_grid[i, j] = 8

    # Attempt to identify other color transformations
    input_counts = count_colors(input_grid)
    output_counts = count_colors(output_grid)

    for color in range(10):
        diff = input_counts[color] - output_counts[color]
        if diff > 0:  # Potential source color
            for other_color in range(10):
                if input_counts[other_color] - output_counts[other_color] == -diff: #potential target color
                    # Apply the identified transformation
                    for i in range(rows):
                        for j in range(cols):
                            if input_grid[i,j] == color:
                                output_grid[i,j] = other_color
                    break #only one target per source color
    return output_grid

def count_colors(grid):
    """Counts the occurrences of each color (0-9) in the grid."""
    counts = [0] * 10
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            counts[grid[i, j]] += 1
    return counts