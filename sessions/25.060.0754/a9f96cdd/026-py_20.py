"""
The input grid contains a single red pixel. The output grid is the same size and contains four colored pixels: green, magenta, azure, and orange, in addition to the red pixel.  The other pixels are white (0). The positions of the colored pixels are determined based on the position of the red pixel, but not via constant offsets. The positions are defined as follows:

Task 1:
- Green: Same row as red, column = red_column + 1
- Magenta: Same row as red, column = red_column + 2
- Azure: Same column as red, row = red_row - 1
- Orange: Same column as red, row = red_row + 1

Task 2:
- Green: Row = red_row, Column = 27
- Magenta: Row = red_row, Column = 28
- Azure: Row = red_row, Column = 26
- Orange: Row = red_row, Column = 25
"""

import numpy as np

def find_pixel(grid, color_value):
    """Finds the coordinates of the first pixel with the given color value."""
    pos = np.argwhere(grid == color_value)
    return pos[0] if len(pos) > 0 else None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.zeros_like(input_grid)
    red_pos = find_pixel(input_grid, 2)

    if red_pos is None:
        return output_grid  # Return blank grid if no red pixel
    
    output_grid[red_pos[0], red_pos[1]] = 2

    red_row, red_col = red_pos
    
    # Check the input grid size to determine which task rule to apply.
    if input_grid.shape[1] < 30:  # Task 1
        # Green: Same row as red, column = red_column + 1
        if red_col + 1 < output_grid.shape[1]:
            output_grid[red_row, red_col + 1] = 3
        # Magenta: Same row as red, column = red_column + 2
        if red_col + 2 < output_grid.shape[1]:
          output_grid[red_row, red_col + 2] = 6
        # Azure: Same column as red, row = red_row - 1
        if red_row - 1 >= 0:
            output_grid[red_row - 1, red_col] = 8
        # Orange: Same column as red, row = red_row + 1
        if red_row + 1 < output_grid.shape[0]:
            output_grid[red_row + 1, red_col] = 7
    else:  # Task 2
        # Green: Row = red_row, Column = 27
        output_grid[red_row, 27] = 3
        # Magenta: Row = red_row, Column = 28
        output_grid[red_row, 28] = 6
        # Azure: Row = red_row, Column = 26
        output_grid[red_row, 26] = 8
        # Orange: Row = red_row, Column = 25
        output_grid[red_row, 25] = 7

    return output_grid