"""
Connects a red pixel and a green pixel in the input grid with a path of azure pixels. The path extends either vertically or horizontally first to align on an axis, then in the other axis to connect, ensuring the correct endpoint.
"""

import numpy as np

def find_pixel_by_color(grid, color_value):
    """Finds the coordinates of the first pixel with the specified color value."""
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color_value:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid by connecting a red and green pixel with an azure path."""
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the red and green pixels
    red_pos = find_pixel_by_color(input_grid, 2)
    green_pos = find_pixel_by_color(input_grid, 3)

    if red_pos is None or green_pos is None:
        return output_grid  # Return original grid if pixels are not found

    # Determine which axis to extend first
    row_diff = green_pos[0] - red_pos[0]
    col_diff = green_pos[1] - red_pos[1]
    
    if row_diff != 0:
      # Create the first vertical segment
      for row in range(red_pos[0] + (1 if row_diff > 0 else -1), green_pos[0], (1 if row_diff > 0 else -1)):
          output_grid[row, red_pos[1]] = 8
      # Create the second horizontal segment
      for col in range(red_pos[1] + (1 if col_diff > 0 else -1), green_pos[1] + (1 if col_diff > 0 else 0) , (1 if col_diff > 0 else -1) ):
        output_grid[green_pos[0], col] = 8
    elif col_diff != 0:
      # Create the first horizontal segment
      for col in range(red_pos[1] + (1 if col_diff > 0 else -1), green_pos[1], (1 if col_diff > 0 else -1) ):
        output_grid[red_pos[0], col] = 8

      # Create the second veritical segment
      for row in range(red_pos[0] + (1 if row_diff > 0 else -1), green_pos[0] + (1 if row_diff > 0 else 0), (1 if row_diff > 0 else -1)):
          output_grid[row, green_pos[1]] = 8
    

    return output_grid