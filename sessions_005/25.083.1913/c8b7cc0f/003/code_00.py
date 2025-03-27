"""
1.  **Identify Top-Left Object:** Find the top-leftmost non-zero pixel in the input grid.  This pixel belongs to the "primary object."
2.  **Determine the Object Color:** Note the color of the primary object.
3.  **Outline:** Determine the outline of the shape defined by the primary object by looking for 3 adjacent pixels of the same color.
4.  **Create 3x3 Output:** Create a 3x3 output grid filled entirely with black (0) pixels.
5.  **Fill Outline:** Fill the outline defined by the primary color, in the output. If the outline is incomplete, extend to the bounds of the 3x3 grid.
6.  **Background:** All other pixels in the output should be black (0).
"""

import numpy as np

def find_top_left_non_zero_pixel(grid):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return r, c
    return None, None

def get_color(grid, row, col):
    if 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]:
        return grid[row, col]
    return 0

def transform(input_grid):
    # Create a 3x3 output grid filled with black (0)
    output_grid = np.zeros((3, 3), dtype=int)

    input_grid = np.array(input_grid)

    # Find the top-leftmost non-zero pixel
    start_row, start_col = find_top_left_non_zero_pixel(input_grid)

    # if no non-zero pixel, return the all black grid
    if start_row is None:
        return output_grid

    # Get the color of the primary object
    primary_color = get_color(input_grid, start_row, start_col)

    # Fill the outline in the output grid
    output_grid[0,0] = primary_color

    # check right
    if get_color(input_grid, start_row, start_col + 1) == primary_color:
        output_grid[0,1] = primary_color
        if get_color(input_grid, start_row, start_col + 2) == primary_color:
            output_grid[0,2] = primary_color
    # check down
    if get_color(input_grid, start_row+1, start_col) == primary_color:
        output_grid[1,0] = primary_color
        if get_color(input_grid, start_row+2, start_col) == primary_color:
            output_grid[2,0] = primary_color

        # check diagonal
        if get_color(input_grid, start_row + 1, start_col + 1) == primary_color:
            output_grid[1,1] = primary_color

    return output_grid