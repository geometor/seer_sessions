import numpy as np

def find_marker(grid, marker_value):
  """Finds the row and column index of the first occurrence of marker_value."""
  for r_idx, row in enumerate(grid):
    for c_idx, value in enumerate(row):
      if value == marker_value:
        return r_idx, c_idx
  return None # Should not happen based on problem description

def transform(input_grid):
  """
  Transforms the input grid by creating a new grid of the same dimensions,
  filled with 0s, and then drawing a 3x3 square of 4s centered at the
  location where the value 7 was found in the input grid.
  """
  # Convert input to numpy array for easier manipulation
  input_array = np.array(input_grid, dtype=int)
  rows, cols = input_array.shape
  
  # Initialize output_grid with the same dimensions as the input, filled with 0
  output_grid = np.zeros_like(input_array)

  # Find the coordinates (row, column) of the marker value (7)
  marker_row, marker_col = find_marker(input_array, 7)

  # If marker is found (which it always should be according to the rules)
  if marker_row is not None and marker_col is not None:
      # Determine the top-left corner coordinates for the 3x3 square
      start_row = marker_row - 1
      start_col = marker_col - 1
      
      # Iterate through the 3x3 area centered at the marker
      for r in range(start_row, start_row + 3):
          for c in range(start_col, start_col + 3):
              # Check if the current coordinates (r, c) are within the grid bounds
              if 0 <= r < rows and 0 <= c < cols:
                  # Set the value in the output grid to 4
                  output_grid[r, c] = 4
                  
  # Return the completed output grid (converted back to list of lists if necessary, 
  # but numpy array is often preferred)
  return output_grid.tolist()
