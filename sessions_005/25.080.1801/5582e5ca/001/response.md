```python
"""
1.  **Examine** the input grid, which is a 3x3 matrix of digits.
2.  **Identify** last number on the main diagonal (from top-left to bottom-right) of the input grid.
3.  **Create** a new 3x3 grid.
4.  **Fill** all cells of the new grid with the identified digit.
5. The new filled grid is the **output**.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the digit on the main diagonal
    selected_digit = input_grid[2][2]

    # Fill the output grid with the selected digit.
    output_grid[:] = selected_digit

    return output_grid
```