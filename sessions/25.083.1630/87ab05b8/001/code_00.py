"""
Locate the bottom-right pixel of a color other than 6. Then change a 2x2 area
including, and up and to the left of, the pixel found. All other pixels stay
the same.
"""

import numpy as np

def find_bottom_right_non_background(grid, background_color=6):
    """Finds the bottom-right pixel that is not the background color."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] != background_color:
                return r, c, grid[r, c]
    return None  # Should not reach here if there is at least one non-background pixel.


def transform(input_grid):
    """Transforms the input grid according to the rule."""
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the bottom-right non-background pixel
    target_row, target_col, target_color = find_bottom_right_non_background(output_grid)

    # Determine the top-left coordinates of the 2x2 block
    top_left_row = target_row - 1
    top_left_col = target_col - 1


    # Modify the 2x2 block in the output grid
    if 0 <= top_left_row < rows and 0 <= top_left_col < cols:
      output_grid[top_left_row:top_left_row + 2, top_left_col:top_left_col + 2] = target_color

    return output_grid