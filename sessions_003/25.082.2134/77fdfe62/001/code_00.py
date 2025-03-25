"""
Transforms an input grid into an output grid by selecting specific corner pixels from regions above and below a horizontal blue line, and arranging them in a specific pattern.
"""

import numpy as np

def find_blue_line(grid):
    """Finds the row index of the horizontal blue line."""
    for i, row in enumerate(grid):
        if all(pixel == 1 for pixel in row):
            return i
    return None

def get_corner_pixels(grid, blue_line_row):
    """Gets the top-left, top-right, bottom-left, and bottom-right corner pixels, excluding the blue line."""
    height, width = grid.shape
    top_left = grid[0, 0] if blue_line_row > 0 else 0
    top_right = grid[0, width - 1] if blue_line_row > 0 else 0
    bottom_left = grid[height - 1, 0] if blue_line_row < height -1 else 0
    bottom_right = grid[height - 1, width - 1] if blue_line_row < height-1 else 0

    return top_left, top_right, bottom_left, bottom_right

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    blue_line_row = find_blue_line(input_grid)

    top_left, top_right, bottom_left, bottom_right = get_corner_pixels(input_grid, blue_line_row)
    
    # Build the output grid
    if blue_line_row is not None:
      output_grid_top = np.array([[top_left, top_right], [top_left, top_right]]) if (top_left !=0 or top_right !=0) else np.array([[0,0],[0,0]])
      output_grid_bottom = np.array([[bottom_left, bottom_right], [bottom_left, bottom_right]]) if (bottom_left != 0 or bottom_right != 0) else np.array([[0, 0], [0, 0]])

      # Ensure consistent dimensions before concatenation
      if output_grid_top.size == 0:
          output_grid = output_grid_bottom
      elif output_grid_bottom.size == 0:
            output_grid = output_grid_top
      else:
        if output_grid_top.shape[1] < output_grid_bottom.shape[1]:
          output_grid_top = np.pad(output_grid_top, ((0,0),(0,output_grid_bottom.shape[1]-output_grid_top.shape[1])), 'constant')
        elif output_grid_top.shape[1] > output_grid_bottom.shape[1]:
          output_grid_bottom = np.pad(output_grid_bottom, ((0,0),(0, output_grid_top.shape[1]-output_grid_bottom.shape[1])), 'constant')
        output_grid = np.vstack([output_grid_top, output_grid_bottom])
    else:  # Handle cases where there's no blue line.
      output_grid = np.zeros((2,2), dtype=int)


    return output_grid.tolist()