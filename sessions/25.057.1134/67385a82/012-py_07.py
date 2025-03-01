"""
Identifies horizontal, contiguous sequences of green pixels. If a sequence has a length greater than 1, replaces all green pixels in that sequence with azure pixels.
Leaves all other pixels unchanged.
"""

import numpy as np

def get_horizontal_sequences(grid, color):
    """
    Finds all horizontal, contiguous sequences of the specified color.

    Args:
        grid: A 2D numpy array representing the input grid.
        color: The color to search for.

    Returns:
        A list of tuples, where each tuple represents a sequence and contains:
            - row index
            - start column index
            - end column index (exclusive)
    """
    sequences = []
    rows, cols = grid.shape
    for r in range(rows):
        start_col = None
        for c in range(cols):
            if grid[r, c] == color:
                if start_col is None:
                    start_col = c
            elif start_col is not None:
                sequences.append((r, start_col, c))
                start_col = None
        if start_col is not None:  # Handle sequences that extend to the end of the row
            sequences.append((r, start_col, cols))
    return sequences

def transform(input_grid):
    """
    Transforms the input grid by replacing certain green pixels with azure pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all horizontal sequences of green (3) pixels.
    green_sequences = get_horizontal_sequences(input_grid, 3)

    # Iterate through the sequences and replace if length > 1
    for row, start_col, end_col in green_sequences:
        if end_col - start_col > 1:
            for c in range(start_col, end_col):
                output_grid[row, c] = 8

    return output_grid