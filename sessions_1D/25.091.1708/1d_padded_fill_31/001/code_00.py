import numpy as np

def find_non_white_color(grid):
  """Finds the first non-white color (value != 0) in the grid."""
  for pixel in grid:
    if pixel != 0:
      return pixel
  return None # Should not happen based on task description

def find_color_indices(grid, color):
  """Finds all indices of a given color in the grid."""
  return np.where(grid == color)[0]

def transform(input_grid):
  """
  Transforms the input grid by filling the segment between the first and 
  last occurrence of the non-white color with that same color.

  Args:
    input_grid: A 1D numpy array representing the input row.

  Returns:
    A 1D numpy array representing the transformed output row.
  """
  # Ensure input is a NumPy array
  input_grid_np = np.array(input_grid)

  # 1. Identify the single non-white color (fill_color)
  fill_color = find_non_white_color(input_grid_np)
  if fill_color is None:
      # Handle case with no non-white color (return input as is)
      return input_grid_np.copy() 

  # 2. Find the indices of all occurrences of the fill_color
  indices = find_color_indices(input_grid_np, fill_color)
  
  # Handle case with zero or one occurrence (no filling needed)
  if len(indices) < 2:
    return input_grid_np.copy()

  # 3. Get the first (start_index) and last (end_index) index
  start_index = indices[0]
  end_index = indices[-1]

  # 4. Initialize the output grid as a copy of the input grid
  output_grid = input_grid_np.copy()

  # 5 & 6. Iterate through the indices strictly between start_index and end_index 
  #        and set the color to fill_color.
  #        Using numpy slicing for efficiency: output_grid[start+1:end]
  if start_index + 1 < end_index: # Check if there's actually space between
      output_grid[start_index + 1 : end_index] = fill_color
  
  # 7. Return the modified output grid
  return output_grid