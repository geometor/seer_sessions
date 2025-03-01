# a87f7484 • 002 • example_4 • investigate_coder

---
```python
"""
1.  **Identify the Target Color:** Scan the input grid to find the bottom-most, non-zero color.
2.  **Extract Central Region:** If this color is present, center a 3x3 window around instances of the last most occurrence of that color, taking boundary into account.
3. **Form output grid** Return the 3x3 sub-grid derived in the last step, using the 3x3 subgrid content as the output.
"""

import numpy as np

def get_bottom_most_color(input_grid):
    """Finds the bottom-most, non-zero color in the grid."""
    rows, cols = input_grid.shape
    bottom_most_color = 0
    for r in range(rows - 1, -1, -1):
        for c in range(cols):
            if input_grid[r, c] != 0:
                bottom_most_color = input_grid[r, c]
                return bottom_most_color, r, c
    return bottom_most_color, -1, -1

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Identify the target (bottom-most, non-zero) color and its position
    target_color, target_row, target_col = get_bottom_most_color(input_grid)

    if target_color == 0:
        return output_grid

    # Extract the 3x3 region centered around the target color
    start_row = max(0, target_row - 1)
    end_row = min(rows, target_row + 2)
    start_col = max(0, target_col - 1)
    end_col = min(cols, target_col + 2)

    # Extract 3x3 sub_grid. Handle boundaries of input grid
    subgrid_height = end_row - start_row
    subgrid_width = end_col - start_col
    sub_grid = input_grid[start_row:end_row, start_col:end_col]

    # Center sub_grid onto output
    out_start_row = max(0, 1 - (target_row - start_row))  # Adjust for top boundary
    out_start_col = max(0, 1 - (target_col - start_col)) # Adjust for left boundary

    output_grid[out_start_row:out_start_row + subgrid_height,
                out_start_col:out_start_col + subgrid_width] = sub_grid

    return output_grid
```
