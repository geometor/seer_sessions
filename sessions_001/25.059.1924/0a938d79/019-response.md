# 0a938d79 • 019 • refine_coder

---
```python
"""
1.  **Locate Key Rows:** Find the row indices of the first occurrences of color 2 (red) and color 3 (green) within the input grid.
2.  **Transform Starting Row**: Transform the row where color 2 first appears by filling it entirely with color 2 (red).
3.  **Alternate Upwards:** Starting from the row immediately *above* the transformed row, fill the entire row with color 3. Continue filling rows upwards, alternating between color 3 and 2 for each subsequent row.
4.  **Alternate Downwards:** Starting from the row immediately *below* the transformed row, fill it entirely with color 3. Continue filling rows downwards, alternating between colors 3 and 2 for each subsequent row.
5. Stop when reaching the top and bottom boundaries of the grid.
"""

import numpy as np

def find_first_color_row(grid, color):
    """Finds the row index of the first occurrence of a given color."""
    for i, row in enumerate(grid):
        if color in row:
            return i
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the row index of the first occurrence of color 2.
    red_row = find_first_color_row(input_grid, 2)

    if red_row is None:
        return output_grid # Return blank grid if color 2 isn't present.

    # Replace the entire row containing color 2 with color 2.
    output_grid[red_row, :] = 2

    # Alternate colors 2 and 3 for rows above.
    current_color = 3
    for r in range(red_row - 1, -1, -1):
        output_grid[r, :] = current_color
        current_color = 3 if current_color == 2 else 2

    # Alternate colors 3 and 2 for rows below
    current_color = 3
    for r in range(red_row + 1, output_grid.shape[0]):
        output_grid[r, :] = current_color
        current_color = 3 if current_color == 2 else 2


    return output_grid
```
