# e6721834 • 012 • refine_coder

---
```python
"""
The transformation rule is as follows:

1.  **Divide:** Divide the input grid into two rectangular regions (left and right) based on a vertical boundary at column 10.
2.  **Recolor Left:** Recolor the entire left region to blue (color 1).
3. **Condense Right, Preserve Colors:** Consider the right region. Identify all pixels that *do not* match the background color of the right region (which is consistently blue (1) in these examples).
4.  **Maintain Relative Positioning in condensation:** Condense these non-background pixels into a smaller rectangular area on the right, maintaining their original colors and relative positions *within* the right region. The condensed area will have the same height as the grid. The condensed area will always start at column 10.
"""

import numpy as np

def get_right_background_color(grid, boundary_col):
    """Gets the background color of the right region."""
    return grid[0, boundary_col]

def condense_right_side(grid, boundary_col):
    """Condenses the right side of the grid, preserving non-background colors."""
    right_background = get_right_background_color(grid, boundary_col)
    right_side = grid[:, boundary_col:]
    height = grid.shape[0]
    width = grid.shape[1] // 2
    condensed_grid = np.full((height, width), right_background)  # Initialize with background

    non_background_pixels = []
    for row_index, row in enumerate(right_side):
        for col_index, pixel in enumerate(row):
            if pixel != right_background:
                non_background_pixels.append((row_index, col_index, pixel))

    for row, col, color in non_background_pixels:
        condensed_grid[row, col] = color #keep col relative

    return condensed_grid

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Divide the grid at column 10.
    boundary_col = 10
    height = input_grid.shape[0]
    width = input_grid.shape[1]

    # 2. Recolor the left region to blue (1).
    output_grid = np.full((height, width), 1)


    # 3. & 4. Condense the right side, preserving colors.
    condensed_right = condense_right_side(input_grid, boundary_col)

    #combine
    output_grid[:, boundary_col:] = condensed_right


    return output_grid.tolist()
```
