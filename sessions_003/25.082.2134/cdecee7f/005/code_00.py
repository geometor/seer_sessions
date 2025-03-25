"""
1.  **Extract Digits:** Identify all non-zero digits within the 10x10 input grid.
2.  **Order Digits:** Sort the extracted digits in ascending order based on their *value*.
3.  **Create Output Grid:** Create a 3x3 output grid initialized with zeros.
4.  **Populate Output Grid:** Fill the 3x3 output grid with the sorted digits. Fill the grid from left to right and top to bottom.
5. **Fill Remainder:** The output grid will be pre-filled with zeros. If there are more cells then digits, the remaining will stay 0.
"""

import numpy as np

def get_sorted_nonzero_digits(grid):
    """
    Extracts non-zero digits from the input grid and sorts them
    based on their value (ascending).
    """
    nonzero_digits = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_digits.append(grid[r, c])

    # sort by digit value
    sorted_digits = sorted(nonzero_digits)
    return sorted_digits

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # get non-zero digits in order
    sorted_nonzero_digits = get_sorted_nonzero_digits(input_grid)

    # populate output grid
    index = 0
    for i in range(3):
        for j in range(3):
            if index < len(sorted_nonzero_digits):
                output_grid[i, j] = sorted_nonzero_digits[index]
                index += 1
            else:
                break  # Stop if we run out of non-zero digits
        if index >= len(sorted_nonzero_digits):
          break

    return output_grid