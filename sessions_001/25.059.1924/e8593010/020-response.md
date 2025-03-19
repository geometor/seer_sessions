# e8593010 • 020 • refine_coder

---
```python
"""
1.  Preserve Gray: All gray pixels in the input grid remain unchanged in the output grid.
2.  Background Fill: If the input has a solid filled shape in the center composed of white pixels, replace all the white pixels with blue.
3.  Checkerboard Pattern: If the input has checkerboard pattern of white and grey pixels, replace the white pixels by a series of rotating colors - red, blue and green - starting from the top left.
"""

import numpy as np

def is_solid_fill(grid, color):
    """Checks if the grid has a solid filled shape of the given color."""
    rows, cols = grid.shape
    # Find bounding box of the color
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return False
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)

    # Check if the shape is solid within the bounding box
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if grid[r, c] != color:
                return False
    return True

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check for solid fill of white
    if is_solid_fill(input_grid, 0):
        # change output pixels - Background Fill
        for r in range(rows):
            for c in range(cols):
                if input_grid[r][c] == 0:
                    output_grid[r][c] = 1  # Blue
    else: # Checkerboard Pattern
        color_sequence = [2, 1, 3]  # Red, Blue, Green
        color_index = 0
        for r in range(rows):
            for c in range(cols):
                if input_grid[r][c] == 0:
                    output_grid[r][c] = color_sequence[color_index % 3]
                    color_index += 1


    return output_grid
```
