"""
Creates an output grid of the same dimensions as the input, initialized to white (0).
Finds the single red (2) pixel in the input grid.
Places four specific colors (green-3, magenta-6, azure-8, orange-7) in the output grid at positions diagonally adjacent to the original red pixel's location, but only if the target position is within the grid boundaries. The original red pixel location remains white in the output.
"""

import numpy as np

def find_pixel(grid, color_value):
  """Finds the first occurrence of a pixel with the specified color value."""
  height, width = grid.shape
  for r in range(height):
    for c in range(width):
      if grid[r, c] == color_value:
        return r, c
  return None # Should not happen based on task description

def transform(input_grid):
  """
  Applies the transformation rule based on the position of the red pixel.
  """
  input_grid_np = np.array(input_grid, dtype=int)
  height, width = input_grid_np.shape

  # Initialize output_grid with white (0)
  output_grid = np.zeros_like(input_grid_np)

  # Find the coordinates (r, c) of the red (2) pixel
  red_pos = find_pixel(input_grid_np, 2)
  if red_pos is None:
      # Handle case where red pixel isn't found, though constraints say it exists
      # For now, return the empty grid
      return output_grid.tolist()

  r, c = red_pos

  # Define the diagonal target positions and their corresponding colors
  # (relative_row, relative_col, color)
  diagonals = [
      (-1, -1, 3), # Up-Left: green (3)
      (-1, +1, 6), # Up-Right: magenta (6)
      (+1, -1, 8), # Down-Left: azure (8)
      (+1, +1, 7)  # Down-Right: orange (7)
  ]

  # Iterate through the diagonal definitions
  for dr, dc, color in diagonals:
    # Calculate the target coordinates
    target_r = r + dr
    target_c = c + dc

    # Check if target coordinates are within the grid boundaries
    is_valid_row = 0 <= target_r < height
    is_valid_col = 0 <= target_c < width

    # If within bounds, place the color in the output grid
    if is_valid_row and is_valid_col:
      output_grid[target_r, target_c] = color

  # Return the completed output grid as a list of lists
  return output_grid.tolist()