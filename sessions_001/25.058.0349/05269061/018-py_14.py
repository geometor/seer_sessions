"""
The transformation identifies the smallest repeating rectangular pattern unit within the input grid and replicates this unit across the output grid, maintaining the same dimensions as the input.
"""

import numpy as np

def find_repeating_pattern(grid):
    """
    Finds the smallest repeating rectangular pattern unit in a grid.
    """
    rows, cols = grid.shape
    for height in range(1, rows + 1):
        for width in range(1, cols + 1):
            if rows % height == 0 and cols % width == 0:
                pattern = grid[:height, :width]
                valid_pattern = True
                for i in range(0, rows, height):
                    for j in range(0, cols, width):
                        if not np.array_equal(grid[i:i+height, j:j+width], pattern):
                            valid_pattern = False
                            break
                    if not valid_pattern:
                        break
                if valid_pattern:
                    return pattern
    return grid  # If no smaller pattern is found, return the whole grid

def transform(input_grid):
    # Identify the repeating pattern unit
    pattern = find_repeating_pattern(input_grid)

    # Get dimensions of the input grid and the pattern
    input_rows, input_cols = input_grid.shape
    pattern_rows, pattern_cols = pattern.shape

    # Initialize the output grid
    output_grid = np.zeros_like(input_grid)

    # Replicate the pattern across the output grid
    for i in range(input_rows):
        for j in range(input_cols):
            output_grid[i, j] = pattern[i % pattern_rows, j % pattern_cols]

    return output_grid