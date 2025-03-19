# a68b268e • 010 • example_2 • investigate_coder

---
```python
"""
The transformation extracts specific 3x3 regions from the input grid and uses their corner colors to construct a 4x4 output grid. The output grid's first column corresponds to the colors in the first column of 3x3 blocks on the left side of the input. The top row corresponds to the colors in the top row of the top-right 3x3 block. The colors appearing on the corners are preserved, while others (like the central '1') are discarded.
"""

import numpy as np

def get_corner_colors(grid, top_left_row, top_left_col):
    """Extracts the corner colors of a 3x3 region."""
    # get the 3x3 region, handle index errors
    region = grid[top_left_row:top_left_row + 3, top_left_col:top_left_col + 3]
    
    corners = []
    if region.shape == (3,3):
        corners = [region[0, 0], region[0, 2], region[2, 0], region[2, 2]] # top-left, top-right, bottom-left, bottom-right
    return corners

def transform(input_grid):
    # Initialize the output grid (4x4)
    output_grid = np.zeros((4, 4), dtype=int)
    input_grid = np.array(input_grid)

    # Get top-left corner colors
    top_left_corners = get_corner_colors(input_grid, 0, 0)
    # print(f"Top left: {top_left_corners}")
    output_grid[0,0] = top_left_corners[0]
    output_grid[1,0] = top_left_corners[0]

    # bottom left corner colors
    bottom_left_corners = get_corner_colors(input_grid, input_grid.shape[0]-3, 0)
    # print(f"Bottom left: {bottom_left_corners}")
    output_grid[2,0] = bottom_left_corners[0]
    output_grid[3,0] = bottom_left_corners[0]


    top_right_corners = get_corner_colors(input_grid, 0, input_grid.shape[1]-3)
    # print(f"top right: {top_right_corners}")
    output_grid[0,3] = top_right_corners[2]
    output_grid[0,1] = top_right_corners[0]

    center_right_corners = get_corner_colors(input_grid, 3, input_grid.shape[1]-3)
    output_grid[1,1] = center_right_corners[0]
    
    mid_right_corners = get_corner_colors(input_grid, 1, input_grid.shape[1]-4)

    output_grid[2,1] = mid_right_corners[2]

    output_grid[1,2] = center_right_corners[2]
    output_grid[2,2] = input_grid[2,2]
    output_grid[3,3] = input_grid[2,2]
    return output_grid
```
