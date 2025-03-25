```python
"""
1.  **Identify:** Find all non-zero digits within the 10x10 input grid.
2.  **Order**: Create an ordered list, add non-zero digits to the list, read input top to bottom, left to right.
3.  **Populate:** Create a 3x3 output grid. Fill the output, from left to right, top to bottom, using the ordered list, stopping once all list elements have been used.
4.  **Fill Remainder:** If any cells in the 3x3 grid remain empty, fill them with 0.
"""

import numpy as np

def get_nonzero_digits(grid):
    """
    Extracts non-zero digits from the input grid, preserving their original order.
    """
    nonzero_digits = []
    for row in grid:
        for element in row:
            if element != 0:
                nonzero_digits.append(element)
    return nonzero_digits

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # get non-zero digits in order
    nonzero_digits = get_nonzero_digits(input_grid)

    # populate output grid
    index = 0
    for i in range(3):
        for j in range(3):
            if index < len(nonzero_digits):
                output_grid[i, j] = nonzero_digits[index]
                index += 1
            else:
                break  # Stop if we run out of non-zero digits
        if index >= len(nonzero_digits):
          break
    return output_grid
```