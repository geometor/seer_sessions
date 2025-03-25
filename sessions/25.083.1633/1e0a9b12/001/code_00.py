"""
Take all the non-zero numbers from the input and "stack" them at the bottom of the output grid, while filling the rest with zeros, without changing the input order.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by stacking non-zero digits at the bottom.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    non_zero_digits = []

    # 1. Identify and Order: Extract non-zero digits while preserving order.
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_digits.append(input_grid[r, c])

    # 2. Stack: Place non-zero digits at the bottom, filling upwards.
    current_row = rows - 1
    col_index = 0
    for digit in non_zero_digits:
        while output_grid[current_row, col_index] != 0:
            col_index +=1
            if col_index >= cols:
               col_index = 0
               current_row -=1

        output_grid[current_row, col_index] = digit
        col_index += 1
        if col_index >= cols:
            col_index = 0
            current_row -= 1
            
    # 3. Fill (Implicitly handled by initializing output_grid with zeros).

    return output_grid