# 794b24be • 048 • refine_coder

---
```python
"""
1.  **Identify the Solid Horizontal Line:** Find the single row in the input grid that contains a contiguous horizontal line of pixels that are a single non-white color. The row can be determined because all pixels that are not white have the same color.
2.  **Get Line Attributes**: Note the row index and the non-white color of this line.
3.  **Reconstruct:** Create an output grid of the same dimensions as the input grid, filled entirely with white (color 0).
4.  **Draw Line:** In the output grid, color all pixels in the identified row with the identified color.
5. All other pixels in the output grid remain white.
"""

import numpy as np

def find_horizontal_line(grid):
    """Finds the row index and color of a solid horizontal line."""
    rows, cols = grid.shape
    for r in range(rows):
        row_colors = []
        for c in range(cols):
            if grid[r, c] != 0:  # Not white
                row_colors.append(grid[r, c])
        if len(row_colors) > 0 and all(x == row_colors[0] for x in row_colors): # all the same color
            return r, row_colors[0]
    return None, None  # No line found


def transform(input_grid):
    """Transforms the input grid by drawing a single horizontal line."""
    # Initialize output_grid as all white (0) with the same dimensions as the input_grid
    output_grid = np.zeros_like(input_grid)

    # Find the horizontal line's row and color
    row_index, color = find_horizontal_line(input_grid)

    # If a line is found, draw it on the output grid
    if row_index is not None:
        rows, cols = output_grid.shape
        for c in range(cols):
            output_grid[row_index, c] = color

    return output_grid
```
