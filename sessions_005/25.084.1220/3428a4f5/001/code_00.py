import numpy as np

def find_separator_row(grid_np):
  """Finds the index of the first row containing only yellow (4) pixels."""
  for r in range(grid_np.shape[0]):
    if np.all(grid_np[r, :] == 4):
      return r
  return -1 # Should not happen based on examples

def apply_combination_rule(upper_pixel, lower_pixel):
  """Applies the pixel combination rule to determine the output pixel value."""
  # Rule:
  # white(0) + white(0) -> white(0)
  # red(2)   + white(0) -> green(3)
  # white(0) + red(2)   -> green(3)
  # red(2)   + red(2)   -> white(0)
  if upper_pixel == 2 and lower_pixel == 2:
    return 0
  elif upper_pixel == 0 and lower_pixel == 0:
    return 0
  elif upper_pixel == 2 or lower_pixel == 2: # Exactly one is red (2), the other is white (0)
    return 3
  else:
    # This case should technically not occur if inputs are only 0 and 2
    # but defaulting to white for safety.
    return 0

def transform(input_grid):
  """
  Transforms the input grid based on a combination rule applied to two subgrids separated by a yellow line.

  1. Finds the horizontal line of yellow (4) pixels.
  2. Extracts the grid above (UpperGrid) and below (LowerGrid) the yellow line.
  3. Creates an output grid with the dimensions of the UpperGrid.
  4. For each cell (r, c), combines the corresponding pixels from UpperGrid and LowerGrid:
     - If both are red (2) or both are white (0), the output is white (0).
     - If one is red (2) and the other is white (0), the output is green (3).
  """
  # Convert input list of lists to a NumPy array for easier processing
  input_np = np.array(input_grid, dtype=int)

  # Find the row index of the yellow separator line
  separator_row_index = find_separator_row(input_np)

  if separator_row_index == -1:
      # Handle cases where the separator might be missing, though not expected
      # based on training data. Returning an empty grid or raising an error
      # might be appropriate. For now, return input shape just as a placeholder.
      print("Warning: Separator row not found.")
      return [[]] * input_np.shape[0]


  # Extract the upper and lower grids
  upper_grid = input_np[0:separator_row_index, :]
  lower_grid = input_np[separator_row_index + 1:, :]

  # Ensure upper and lower grids have the same dimensions
  if upper_grid.shape != lower_grid.shape:
      # Handle inconsistent grid sizes if necessary
      print("Warning: Upper and lower grids have different shapes.")
      # Potentially return an error or default grid
      return [[]] * upper_grid.shape[0] # Default to upper grid shape


  # Get the dimensions for the output grid
  output_height, output_width = upper_grid.shape

  # Initialize the output grid (e.g., with zeros)
  output_np = np.zeros((output_height, output_width), dtype=int)

  # Iterate through each cell of the upper/lower grids
  for r in range(output_height):
    for c in range(output_width):
      # Get the pixel values from the upper and lower grids
      upper_pixel = upper_grid[r, c]
      lower_pixel = lower_grid[r, c]

      # Apply the combination rule and set the output pixel
      output_np[r, c] = apply_combination_rule(upper_pixel, lower_pixel)

  # Convert the output NumPy array back to a list of lists
  output_grid = output_np.tolist()

  return output_grid