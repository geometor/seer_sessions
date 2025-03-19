"""
Identify the location of the azure (8) pixel and the red (2) pixel. Draw a vertical line of yellow (4) pixels downwards from the azure pixel, stopping at the row of the red pixel. Draw a horizontal line of yellow (4) pixels from the end of the vertical line to the red pixel. Preserve the azure and red pixels.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first pixel of a given color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    azure_pos = find_pixel(input_grid, 8)
    red_pos = find_pixel(input_grid, 2)

    if azure_pos is None or red_pos is None:
        return output_grid

    # Draw vertical line
    if azure_pos[0] < red_pos[0]:
      for r in range(azure_pos[0] + 1, red_pos[0]):
          output_grid[r, azure_pos[1]] = 4
    else:
      for r in range(red_pos[0] + 1, azure_pos[0] ):
          output_grid[r, azure_pos[1]] = 4        

    # Draw horizontal line
    if(azure_pos[1] < red_pos[1]):
      for c in range(azure_pos[1] + 1, red_pos[1] ):
          output_grid[red_pos[0], c] = 4
    else:
      for c in range(red_pos[1] + 1, azure_pos[1]):
          output_grid[red_pos[0], c] = 4        

    return output_grid