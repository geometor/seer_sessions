import numpy as np

def find_boundary_row_index(grid_np):
  """
  Finds the index of the first row consisting entirely of the digit 4.
  
  Args:
    grid_np: A NumPy array representing the input grid.
  
  Returns:
    The index of the boundary row, or -1 if not found.
  """
  num_rows = grid_np.shape[0]
  for r_idx in range(num_rows):
    # Check if all elements in the current row are equal to 4
    if np.all(grid_np[r_idx, :] == 4):
      return r_idx
  return -1 # Indicate boundary row not found

def transform(input_grid):
  """
  Transforms the input grid by identifying a boundary row composed entirely of the digit 4. 
  All rows from the input grid up to and including this boundary row are kept. 
  All rows below the boundary row are replaced with rows filled entirely with 0s.
  """
  
  # Convert input to a NumPy array for efficient processing
  input_np = np.array(input_grid)

  # Check for empty grid edge case
  if input_np.size == 0:
      return []
      
  # Get grid dimensions
  num_rows, num_cols = input_np.shape
  
  # Find the index of the first row containing only 4s
  boundary_index = find_boundary_row_index(input_np)

  # Initialize the output grid - start with a copy of the input
  # This handles rows above and including the boundary automatically
  output_np = np.copy(input_np)

  # If a boundary row was found
  if boundary_index != -1:
    # Iterate through rows below the boundary index
    for r_idx in range(boundary_index + 1, num_rows):
      # Replace the row with zeros
      output_np[r_idx, :] = 0
  # Else: if no boundary row is found, the original grid copy is returned

  # Convert back to list of lists format if required by the environment
  return output_np.tolist()