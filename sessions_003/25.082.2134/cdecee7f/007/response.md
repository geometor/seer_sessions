```python
"""
1.  **Extract Non-Zero Digits:** Identify all non-zero digits within the input grid, recording their original row and column indices.
2.  **Sort Digits:** Sort the extracted digits based on their original position in the input grid. The sorting prioritizes columns. Within each column, sort the digits from the smallest row index to the largest (reading down the columns).
3.  **Create Output Grid:** Create a 3x3 output grid initialized with zeros.
4.  **Populate Output Grid:** Fill the 3x3 output grid with the sorted digits. Fill the grid from left to right and top to bottom.
5. **Fill Remainder:** The output will be pre-filled with zeros. If there are more cells than digits the remaining cells will stay zero.
"""

import numpy as np

def get_sorted_nonzero_digits(grid):
    """
    Extracts non-zero digits from the input grid and sorts them
    based on their original column and then row (column-major order).
    """
    nonzero_digits = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_digits.append({
                    'value': grid[r, c],
                    'row': r,
                    'col': c
                })

    # sort by column, then row
    sorted_digits = sorted(nonzero_digits, key=lambda x: (x['col'], x['row']))
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
                output_grid[i, j] = sorted_nonzero_digits[index]['value']
                index += 1
            else:
                break  # Stop if we run out of non-zero digits
        if index >= len(sorted_nonzero_digits):
          break

    return output_grid
```