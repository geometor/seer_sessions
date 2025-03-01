# 91714a58 • 004 • example_1 • investigate_coder

---
```python
"""
Extracts the largest rectangular region of red pixels (color code 2) from the input grid and creates an output grid where only this rectangle is preserved, with all other pixels set to white (color code 0).
"""

import numpy as np

def find_largest_red_rectangle(grid):
    """
    Finds the largest rectangle of red pixels within the grid.

    Returns:
        A tuple (start_row, start_col, end_row, end_col) defining the rectangle,
        or None if no red pixels are found.
    """
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
        return None

    max_area = 0
    best_rectangle = None

    for start_row, start_col in red_pixels:
        for end_row, end_col in red_pixels:
            if end_row >= start_row and end_col >= start_col:
                # Check if the rectangle is all red
                sub_grid = grid[start_row:end_row+1, start_col:end_col+1]
                if np.all(sub_grid == 2):
                    area = (end_row - start_row + 1) * (end_col - start_col + 1)
                    if area > max_area:
                        max_area = area
                        best_rectangle = (start_row, start_col, end_row, end_col)
    return best_rectangle
    

def transform(input_grid):
    """
    Transforms the input grid by isolating the largest red rectangle.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the largest red rectangle
    rectangle = find_largest_red_rectangle(input_grid)

    # Initialize output grid as all white
    output_grid = np.zeros_like(input_grid)

    # If a red rectangle was found, preserve it in the output grid
    if rectangle:
        start_row, start_col, end_row, end_col = rectangle
        output_grid[start_row:end_row+1, start_col:end_col+1] = 2

    return output_grid.tolist()
```
