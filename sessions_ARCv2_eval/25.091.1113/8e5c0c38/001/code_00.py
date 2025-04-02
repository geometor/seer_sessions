import numpy as np
from collections import Counter

def find_background_color(grid):
  """Finds the most frequent color in the grid, assumed to be the background."""
  counts = Counter(grid.flatten())
  # Find the color with the highest count
  background_color = counts.most_common(1)[0][0]
  return background_color

def count_same_color_neighbors(grid, r, c, color):
  """Counts the number of adjacent (up, down, left, right) neighbors with the same color."""
  count = 0
  height, width = grid.shape
  neighbors = [
      (r - 1, c),  # Up
      (r + 1, c),  # Down
      (r, c - 1),  # Left
      (r, c + 1)   # Right
  ]
  for nr, nc in neighbors:
    # Check bounds
    if 0 <= nr < height and 0 <= nc < width:
      # Check color
      if grid[nr, nc] == color:
        count += 1
  return count

def transform(input_grid):
  """
  Transforms the input grid by removing pixels from non-background objects
  that have fewer than two adjacent neighbors of the same color. Adjacent neighbors
  are considered only horizontally and vertically. The removed pixels are replaced
  with the background color.
  """
  # Convert input to numpy array for easier manipulation
  input_np = np.array(input_grid, dtype=int)
  height, width = input_np.shape

  # Initialize output_grid as a copy of the input
  output_grid = np.copy(input_np)

  # Determine the background color (most frequent color)
  background_color = find_background_color(input_np)

  # Iterate through each pixel of the input grid
  for r in range(height):
    for c in range(width):
      pixel_color = input_np[r, c]

      # Check if the pixel is part of a non-background object
      if pixel_color != background_color:
        # Count adjacent neighbors with the same color
        neighbor_count = count_same_color_neighbors(input_np, r, c, pixel_color)

        # If the count is less than 2, change the pixel in the output grid to the background color
        if neighbor_count < 2:
          output_grid[r, c] = background_color

  # Convert the result back to a list of lists if necessary (often numpy arrays are acceptable)
  return output_grid.tolist()