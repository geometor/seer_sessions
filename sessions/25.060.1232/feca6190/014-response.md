# feca6190 • 014 • refine_coder

---
```python
"""
1.  **Find Non-Zero Pixels:** Identify all pixels in the input grid that have a non-zero value (representing a color other than white). Note their colors and positions.

2.  **Determine Output Grid Size:** The output grid will be square. Its dimensions are equal to the maximum of the input grid's rows and columns.

3.  **Create Diagonal (if applicable):**
    *   If *both* the input grid's rows and columns are greater than 1, create a diagonal line of pixels in the output grid, starting from the top-left corner and extending to the bottom-right corner. All pixels on this diagonal should have the color of the first non-zero pixel found in the input.
    *  If only one dimension from input > 1:
        * if input is a row vector: creates a *column* vector, where the only non-zero value will be at the *top*.
        * if input is a column vector, then output becomes this vector.
    * if input dimensions are equal to 1: output = input.

4.  **Fill Remaining Pixels:** Set all remaining pixels in the output grid (those not part of the diagonal, in applicable cases) to white (0).
"""

import numpy as np

def find_nonzero_pixels(grid):
    """Finds all non-zero pixels in a grid."""
    non_zero_indices = np.where(grid != 0)
    rows = non_zero_indices[0]
    cols = non_zero_indices[1]
    values = grid[rows, cols]
    return list(zip(rows, cols, values))

def transform(input_grid):
    # Find non-zero pixels.
    non_zero_pixels = find_nonzero_pixels(input_grid)

    # Determine output grid size.
    input_rows, input_cols = input_grid.shape
    output_size = max(input_rows, input_cols)
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Create diagonal or handle row/column vectors.
    if input_rows > 1 and input_cols > 1:
        # Create diagonal from top-left to bottom-right.
        if non_zero_pixels:  # Check if the list is not empty
            value = non_zero_pixels[0][2]
            for i in range(output_size):
                output_grid[i, i] = value
    elif input_rows == 1 and input_cols == 1:
       if non_zero_pixels:
           output_grid[0,0] = non_zero_pixels[0][2]
    elif input_rows == 1:
        # Create a column vector.
        if non_zero_pixels:
            value = non_zero_pixels[0][2]
            output_grid = np.zeros((input_cols, 1), dtype=int)
            output_grid[0, 0] = value
    elif input_cols == 1:
        if non_zero_pixels:
           return input_grid


    return output_grid
```
