# a61f2674 • 008 • refine_coder

---
```python
"""
1.  **Identify the leftmost vertical line of grey pixels.** This line can be continuous or broken, but all pixels must be in the same column.
2.  **Transform the color of these grey pixels to blue.** Maintain their original positions.
3. **Identify the rightmost vertical line of white pixels.** This is similar to the grey line; the white pixels must be in the same, rightmost, column and can form a discontinuous line.
4. **Transform the color of the white pixels to red.** Maintain their original positions.
"""

import numpy as np

def find_leftmost_vertical_line(grid, color):
    """Finds the column index of the leftmost vertical line of a given color."""
    rows, cols = grid.shape
    for j in range(cols):
        pixels = []
        for i in range(rows):
            if grid[i, j] == color:
                pixels.append(i)
        if len(pixels) > 1:  # Consider it a line if there are at least two pixels
            return j, pixels
    return None, []

def find_rightmost_vertical_line(grid, color):
    """Finds the column index of the rightmost vertical line of a given color"""
    rows, cols = grid.shape
    for j in range(cols - 1, -1, -1):
        pixels = []
        for i in range(rows):
            if grid[i,j] == color:
                pixels.append(i)
        if len(pixels) > 1:
            return j, pixels
    return None, []
    

def transform(input_grid):
    # Initialize output grid with a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the leftmost vertical gray line
    col_index_gray, row_indices_gray = find_leftmost_vertical_line(input_grid, 5)
    if col_index_gray is not None:
        # Change the color of the gray pixels to blue
        for i in row_indices_gray:
            output_grid[i, col_index_gray] = 1

    # Find the rightmost vertical white line.
    col_index_white, row_indices_white = find_rightmost_vertical_line(input_grid, 0)
    if col_index_white is not None:
        # Change the color of the white pixels to red.
        for i in row_indices_white:
            output_grid[i, col_index_white] = 2

    return output_grid
```
