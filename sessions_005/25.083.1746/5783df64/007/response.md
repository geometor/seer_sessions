```python
"""
Extracts all non-zero digits from the input grid and arranges them into a 3x3 output grid.
The digits are placed in the output grid in the order they appear in the input grid (row-major order).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting all non-zero digits
    and arranging them in a 3x3 output grid in row-major order.
    """
    # Create a 3x3 output grid filled with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Extract non-zero digits and their positions (row-major)
    non_zero_digits = []
    for row in input_grid:
        for cell in row:
            if cell != 0:
                non_zero_digits.append(cell)

    # Populate the output grid with the non-zero digits
    k = 0
    for i in range(3):
        for j in range(3):
            if k < len(non_zero_digits):
                output_grid[i, j] = non_zero_digits[k]
                k += 1

    return output_grid
```