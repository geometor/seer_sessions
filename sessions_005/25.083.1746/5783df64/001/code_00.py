"""
Extracts non-zero digits from the input grid in top-to-bottom, left-to-right order,
and arranges them into a 3x3 output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting non-zero digits and arranging them in a 3x3 output grid.
    """
    # Initialize an empty list to hold the non-zero digits
    non_zero_digits = []

    # Iterate through the input grid, extracting non-zero digits
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] != 0:
                non_zero_digits.append(input_grid[i, j])

    # Create a 3x3 output grid filled with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Populate the output grid with the non-zero digits
    k = 0
    for i in range(3):
        for j in range(3):
            if k < len(non_zero_digits):
                output_grid[i, j] = non_zero_digits[k]
                k += 1

    return output_grid