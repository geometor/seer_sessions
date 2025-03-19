# 045e512c • 008 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all distinct objects within the input grid. An object is defined as a contiguous block of pixels of the same color. Focus on red, green and azure objects.
2.  **Red Object Transformation:**
    *   Check if the red object's height is smaller than the grid's height.
    *   If the red object's height is smaller than the grid height, extend the red object vertically to match the grid's height. Replicate the red object's internal pattern during extension.
    * If the red object fills the grid vertically, then do not modify it.
3.  **Preserve Other Objects:** Ensure that all other objects (green and azure) retain their original shapes, positions, and colors in the output grid.
"""

import numpy as np

def find_object(grid, color):
    """
    Finds the top-left corner and dimensions of a contiguous block of the given color.
    Returns None if no such object is found.
    """
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None

    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return (min_row, min_col), height, width

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid)
    grid_height = output_grid.shape[0]

    # Find objects
    red_obj = find_object(input_grid, 2)
    green_obj = find_object(input_grid, 3)
    azure_obj = find_object(input_grid, 8)

    # Red Object Transformation
    if red_obj:
        red_pos, red_height, red_width = red_obj
        if red_height < grid_height:
            # Extend red object vertically, preserving pattern
            for row in range(grid_height):
                for col_offset in range(red_width):
                    output_grid[row, red_pos[1] + col_offset] = input_grid[(red_pos[0] + (row % red_height)), red_pos[1] + col_offset]

    # Preserve green and azure - these are already in place by copying input to output
    return output_grid
```
