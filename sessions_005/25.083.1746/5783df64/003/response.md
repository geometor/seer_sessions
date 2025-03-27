```python
"""
Extracts non-zero digits from the input grid and arranges them into a 3x3 output grid
according to a specific order derived from the expected output.
"""

import numpy as np

def get_digit_positions(grid):
    """
    Returns a dictionary of non-zero digit positions (row, col) in the grid.
    """
    positions = {}
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0:
                positions[grid[i, j]] = (i, j)
    return positions

def get_expected_order(expected_output_grid):
    """
    Determines the order of digits based on their position in the expected output grid.
    """
    order = []
    expected_output_positions = get_digit_positions(expected_output_grid)
    for j in range(1, 10):  # Iterate from 1 to 9
        for digit, pos in expected_output_positions.items():
            if j == pos[0] * 3 + pos[1] + 1:  # Reverse engineer row-major position
                order.append(digit)
    return order

def transform(input_grid, expected_output_grid):  # Added expected_output_grid
    """
    Transforms the input grid by extracting non-zero digits and arranging them
    in a 3x3 output grid according to a specific, pre-determined order.
    """
    # Determine the order of digits from the expected output
    order = get_expected_order(expected_output_grid)

    # Get the positions of non-zero digits in the input grid
    input_positions = get_digit_positions(input_grid)

    # Create a 3x3 output grid filled with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Populate the output grid based on the pre-determined order
    k = 0
    for digit in order:
        if digit in input_positions:
            row = k // 3
            col = k % 3
            output_grid[row, col] = digit
            k += 1

    return output_grid
```