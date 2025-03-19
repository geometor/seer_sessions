# 1190e5a7 • 012 • refine_coder

---
```python
"""
The transformation rule identifies the first occurrence of the number '8' within the input grid. The output grid is a cropped section of the input grid.  If '8' appears as a vertical dividing line, the section *before* (to the left of) the first '8' is taken as the output.  If '8' appears as a horizontal dividing line, the section *before* (above) the first '8' is taken.
"""

import numpy as np

def find_first_occurrence(grid, value):
    """Finds the first row and column index where the given value appears."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == value:
                return r, c
    return rows, cols  # Return grid size if value not found

def is_horizontal_line(grid, row, value):
    """Checks if a given row is filled with the specified value."""
    return all(grid[row, c] == value for c in range(grid.shape[1]))

def is_vertical_line(grid, col, value):
    """Checks if a given column is filled with the specified value."""
    return all(grid[r, col] == value for r in range(grid.shape[0]))

def transform(input_grid):
    """
    Extracts a sub-grid from the input, stopping before the first 8, considering horizontal and vertical lines.
    """
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Find the first occurrence of 8
    first_8_row, first_8_col = find_first_occurrence(input_grid, 8)

    # Check if the first 8 is part of a horizontal or vertical line
    if is_horizontal_line(input_grid, first_8_row, 8):
        # Crop above the horizontal line
        output_grid = input_grid[:first_8_row, :]
    elif is_vertical_line(input_grid, first_8_col, 8):
        # Crop to the left of the vertical line
        output_grid = input_grid[:, :first_8_col]
    else:
        # Default case (if no clear horizontal/vertical line) - crop based on first occurrence.
        output_grid = input_grid[:first_8_row, :first_8_col]

    return output_grid.tolist()
```

