```python
import copy

def find_value(grid, value):
  """Finds the (row, col) coordinates of the first occurrence of a value in the grid."""
  for r, row in enumerate(grid):
    for c, cell in enumerate(row):
      if cell == value:
        return r, c
  return None # Should not happen based on problem description

def transform(input_grid):
  """
  Transforms the input grid based on the relative positions of the cells containing '1' and '2'.

  1. Finds the coordinates of the cells containing '1' (pos_1) and '2' (pos_2).
  2. Checks if these cells are diagonally adjacent (absolute row difference is 1 AND absolute column difference is 1).
  3. If they are diagonally adjacent:
     - Creates a copy of the input grid.
     - Changes the value at pos_2 to '1'.
     - Changes the value at pos_1 to '0'.
     - Returns the modified grid.
  4. If they are not diagonally adjacent:
     - Returns an identical copy of the input grid.
  """

  # Find the coordinates of the cells containing 1 and 2
  pos_1 = find_value(input_grid, 1)
  pos_2 = find_value(input_grid, 2)

  if pos_1 is None or pos_2 is None:
      # This case should ideally not happen based on the problem description
      # If it does, return a copy as a safe default
      return copy.deepcopy(input_grid)

  row_1, col_1 = pos_1
  row_2, col_2 = pos_2

  # Check for diagonal adjacency
  is_diagonal = abs(row_1 - row_2) == 1 and abs(col_1 - col_2) == 1

  # Create the output grid (start with a copy)
  output_grid = copy.deepcopy(input_grid)

  # Apply transformation if cells are diagonally adjacent
  if is_diagonal:
    output_grid[row_2][col_2] = 1 # Change '2' to '1'
    output_grid[row_1][col_1] = 0 # Change '1' to '0'
  # Else: output_grid remains an identical copy (already handled by deepcopy)

  return output_grid
```