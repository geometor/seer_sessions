"""
1. **Find Anchor:** Search for the top-leftmost yellow (color value 4) pixel within the input grid. This pixel will be the anchor point. If no yellow pixel is found, return an empty (0x0) grid.

2. **Determine Subgrid Dimensions:** If a yellow pixel is found, determine the largest possible rectangular subgrid that can be formed, with the top-left corner at the anchor pixel.

3. **Extract Subgrid:** Extract this subgrid from the input grid.

4. **Return the subgrid.**
"""

import numpy as np

def find_top_leftmost_color(grid, color):
    # Iterate through the grid to find the top-leftmost occurrence of the specified color.
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color:
                return (r_idx, c_idx)
    return None  # Return None if the color is not found.

def transform(input_grid):
    # Convert input_grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the top-leftmost yellow pixel (color 4).
    top_left_corner = find_top_leftmost_color(input_grid, 4)

    # If no yellow pixel is found, return an empty grid.
    if top_left_corner is None:
        return np.zeros((0, 0), dtype=int)

    # Determine subgrid dimensions.
    start_row, start_col = top_left_corner
    end_row = input_grid.shape[0]  # Maximum possible size
    end_col = input_grid.shape[1]  # Maximum possible size

    # Extract and return the subgrid.
    output_grid = input_grid[start_row:end_row, start_col:end_col]
    return output_grid.tolist()