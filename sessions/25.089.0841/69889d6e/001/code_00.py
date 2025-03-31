import numpy as np

def find_pixels(grid, color):
  """Finds all coordinates (row, col) of pixels with a specific color."""
  coords = np.argwhere(grid == color)
  # Convert numpy array N x 2 to list of tuples [(r1, c1), (r2, c2), ...]
  return [tuple(coord) for coord in coords]

def transform(input_grid):
  """
    Transforms the input grid based on the following rule:
    1. Initialize the output grid as a copy of the input grid.
    2. Find all red pixels (color 2) in the original input grid.
    3. For each original red pixel at location (r, c):
       a. Iterate diagonally upwards and rightwards, tracking the iteration step with 'i' starting from 0.
       b. Calculate the top-left corner of a potential 2x2 block for this step: (dr, dc) = (r - i, c + i).
       c. If the row 'dr' goes above the top edge of the grid (dr < 0), stop the diagonal iteration for this starting red pixel.
       d. Define the four cells relative to the top-left corner (dr, dc): (dr, dc), (dr, dc+1), (dr+1, dc), (dr+1, dc+1).
       e. For each of these four potential cell coordinates (nr, nc):
          i. Check if the coordinates (nr, nc) are within the grid boundaries (0 <= nr < height, 0 <= nc < width).
          ii. If the cell is within bounds AND the corresponding cell in the current output grid is white (color 0), change its color to red (color 2). Other colors (including the original red pixel or blue pixels) are not overwritten.
    4. Return the final modified output grid.
  """
  # Convert input list of lists to numpy array for easier manipulation
  input_np = np.array(input_grid, dtype=int)
  # Initialize output grid as a copy of the input
  output_grid = np.copy(input_np)
  height, width = input_np.shape

  # Find coordinates of all red (2) pixels in the *original* input grid
  # These are the starting points for the diagonal patterns
  initial_red_pixels_coords = find_pixels(input_np, 2)

  # Process each starting red pixel
  for r, c in initial_red_pixels_coords:
      i = 0
      # Loop infinitely until a break condition is met (pattern goes off-grid)
      while True:
          # Calculate the top-left corner (dr, dc) for the 2x2 block
          # Pattern moves diagonally: up (row decreases) and right (column increases)
          dr, dc = r - i, c + i

          # If the row 'dr' is less than 0, the pattern has moved off the top edge
          # Stop processing this diagonal path for the current starting red pixel
          if dr < 0:
              break

          # Define the coordinates of the four cells in the 2x2 block
          # relative to the calculated top-left corner (dr, dc)
          cells_to_paint = [
              (dr, dc),      # Top-left
              (dr, dc + 1),  # Top-right
              (dr + 1, dc),  # Bottom-left
              (dr + 1, dc + 1) # Bottom-right
          ]

          # Iterate through the four cells of the potential 2x2 block
          for nr, nc in cells_to_paint:
              # Check if the cell coordinates (nr, nc) are within the grid boundaries
              if 0 <= nr < height and 0 <= nc < width:
                  # Check if the target cell in the output grid is currently white (0)
                  if output_grid[nr, nc] == 0:
                      # If it's white, paint it red (2)
                      output_grid[nr, nc] = 2
                  # If the cell is not white (e.g., already red, blue, etc.), do nothing

          # Increment the step counter for the next diagonal position
          i += 1

  # Convert the final numpy array back to a list of lists for the expected output format
  return output_grid.tolist()