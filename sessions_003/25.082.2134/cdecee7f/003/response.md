```python
"""
1.  **Identify and Sort:** Find all non-zero digits within the 10x10 input grid, and record the row and column position for each. Sort the digits, considering the input grid read top to bottom and left to right. The order is determined by reading the positions where digits are placed.
2.  **Populate Output:** Create a 3x3 output grid. Fill the output grid with the ordered list of non-zero digits. Fill the grid from left to right and top to bottom.
3.  **Fill Remainder:** If any cells in the 3x3 output grid remain empty after placing all identified digits, fill them with 0.
"""

import numpy as np

def get_sorted_nonzero_digits(grid):
    """
    Extracts non-zero digits from the input grid and sorts them
    based on their position (top-to-bottom, left-to-right).
    """
    nonzero_digits = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_digits.append( ((r, c), grid[r, c]) )

    # sort by row, then by column
    sorted_digits = sorted(nonzero_digits, key=lambda item: (item[0][0], item[0][1]))
    return [digit for _, digit in sorted_digits]

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
```