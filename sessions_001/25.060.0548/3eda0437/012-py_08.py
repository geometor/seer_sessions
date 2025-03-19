"""
The transformation rule is: Find horizontal sequences of exactly three consecutive white (0) pixels in the input grid.
Replace these sequences with magenta (6) pixels in the output grid. Keep all other pixels unchanged.
"""

import numpy as np

def find_horizontal_sequences(grid, color, length):
    """
    Finds horizontal sequences of a specific color and length.

    Args:
        grid: The input grid (2D numpy array).
        color: The color to search for.
        length: The length of the sequence to find.

    Returns:
       A list of (row, start_col) tuples for each sequence found.
    """
    rows, cols = grid.shape
    sequences = []
    for r in range(rows):
        for c in range(cols - length + 1):
            if all(grid[r, c+i] == color for i in range(length)):
                sequences.append((r, c))
    return sequences

def transform(input_grid):
    """
    Transforms the input grid according to the rule: replace horizontal sequences of three 0s with 6s.
    """
    output_grid = input_grid.copy()  # Initialize output_grid as a copy of the input.
    
    # Find the horizontal sequences to be replaced
    sequences_to_replace = find_horizontal_sequences(output_grid, 0, 3) 

    # Iterate and modify the output grid with the change of color
    for row, col_start in sequences_to_replace:
        output_grid[row, col_start:col_start+3] = 6

    return output_grid