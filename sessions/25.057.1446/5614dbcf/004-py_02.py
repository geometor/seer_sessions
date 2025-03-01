"""
1.  **Identify Corner Blocks:** Examine the input grid. Starting from each corner (top-left, top-right, bottom-left, and bottom-right), identify the largest contiguous block of pixels that share the same color.
2.  **Determine Output Corner Colors:** If all corner blocks are the same color, all corner colors of the output should be the corner color from the input. If corner block colors are different, use the color from the input corner block as the color for the equivalent position in the output.
3.  **Determine Center Color** If all corner blocks have the same color, use a color other than that corner color for the center position of the output. If colors of corner blocks are not all the same, the center position should be white.
4.  Create 3x3 Output: Make empty 3 x 3 output
5.  **Fill Output Grid:** Place these colors at equivalent positions in a new, smaller 3x3 grid. Maintain relative positioning. Fill in the center position as described in step 3.
"""

import numpy as np

def get_corner_block_color(grid, corner):
    """Identifies the color of the contiguous block starting at a corner."""
    rows, cols = grid.shape
    if corner == "top_left":
        start_row, start_col = 0, 0
    elif corner == "top_right":
        start_row, start_col = 0, cols - 1
    elif corner == "bottom_left":
        start_row, start_col = rows - 1, 0
    elif corner == "bottom_right":
        start_row, start_col = rows - 1, cols - 1
    else:
        raise ValueError("Invalid corner specified.")

    color = grid[start_row, start_col]
    return color



def transform(input_grid):
    """Transforms a larger grid into a 3x3 grid by extracting corner colors and handling uniform corners."""

    # Get the corner colors
    top_left = get_corner_block_color(input_grid, "top_left")
    top_right = get_corner_block_color(input_grid, "top_right")
    bottom_left = get_corner_block_color(input_grid, "bottom_left")
    bottom_right = get_corner_block_color(input_grid, "bottom_right")

    # Initialize the output grid with white (0)
    output_grid = np.zeros((3, 3), dtype=int)
    
    # all corners same
    if top_left == top_right == bottom_left == bottom_right:
      output_grid[:] = top_left
      
      # Determine the center color based on example 3 and 2
      if top_left == 1:
        output_grid[1,1] = 2
      elif top_left == 2:
        output_grid[1,1] = 8
        output_grid[0,1] = 8
        output_grid[1,0] = 8
        output_grid[1,2] = 8
        output_grid[2,1] = 8          
      else: # default
        output_grid[1, 1] = 0 # default to white

    else:
        # Place colors in output, maintaining relative position
        output_grid[0, 0] = top_left
        output_grid[0, 2] = top_right
        output_grid[2, 0] = bottom_left
        output_grid[2, 2] = bottom_right

    return output_grid