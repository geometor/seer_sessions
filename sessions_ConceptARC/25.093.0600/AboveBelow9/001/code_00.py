import copy

def find_boundary_row_index(grid):
  """
  Finds the index of the first row consisting entirely of the digit 4.
  
  Args:
    grid: A list of lists representing the input grid.
  
  Returns:
    The index of the boundary row, or -1 if not found.
  """
  for r_idx, row in enumerate(grid):
    is_boundary = True
    if not row: # Handle empty rows if necessary, though not expected
        is_boundary = False
        continue
    for cell in row:
      if cell != 4:
        is_boundary = False
        break
    if is_boundary:
      return r_idx
  return -1 # Indicate boundary row not found


def transform(input_grid):
  """
  Transforms the input grid based on a boundary row of 4s.

  Identifies the first row consisting entirely of the digit 4. 
  Keeps all rows from the input grid up to and including this boundary row.
  Replaces all rows below the boundary row with rows filled entirely with 0s.
  """
  
  # Get dimensions
  if not input_grid:
      return []
  num_rows = len(input_grid)
  num_cols = len(input_grid[0]) if num_rows > 0 else 0

  # Find the boundary row (first row full of 4s)
  boundary_index = find_boundary_row_index(input_grid)

  # If no boundary row is found, perhaps return the original grid or handle error
  # Based on examples, we assume it always exists.
  if boundary_index == -1:
      # Or raise ValueError("Boundary row of 4s not found.")
      return copy.deepcopy(input_grid) 

  # Initialize the output grid
  output_grid = []

  # Copy rows up to and including the boundary row
  for r_idx in range(boundary_index + 1):
      # Using deepcopy to avoid modifying original input if it contains mutable elements (though ints are immutable)
      # For clarity and safety with list structure
      output_grid.append(list(input_grid[r_idx])) 

  # Create a row of zeros
  zero_row = [0] * num_cols

  # Fill remaining rows below the boundary with zeros
  for r_idx in range(boundary_index + 1, num_rows):
      output_grid.append(list(zero_row)) # Append a copy of the zero row

  return output_grid