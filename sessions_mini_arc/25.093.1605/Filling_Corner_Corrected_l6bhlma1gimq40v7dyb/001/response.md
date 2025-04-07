```python
import copy

"""
Transforms a 2D grid by changing the value of cells containing 0 to 2 if they are orthogonally adjacent (up, down, left, or right) to a cell containing 4. Cells containing 4 and 0s not adjacent to any 4 remain unchanged.
"""

def is_within_bounds(r, c, height, width):
  """Checks if the given row and column are within the grid boundaries."""
  return 0 <= r < height and 0 <= c < width

def transform(input_grid):
  """
  Applies the transformation rule to the input grid.

  Args:
    input_grid: A list of lists representing the input 2D grid.

  Returns:
    A list of lists representing the transformed output 2D grid.
  """
  # Get grid dimensions
  height = len(input_grid)
  if height == 0:
    return []
  width = len(input_grid[0])
  if width == 0:
    return [[] for _ in range(height)]

  # Initialize output_grid as a deep copy of the input grid
  # This ensures that original 4s and non-adjacent 0s are preserved,
  # and we check conditions based on the original input state.
  output_grid = copy.deepcopy(input_grid)

  # Iterate through each cell of the input grid
  for r in range(height):
    for c in range(width):
      # Check if the current cell in the *input* grid contains a 4
      if input_grid[r][c] == 4:
        # Define potential orthogonal neighbors (dr, dc offsets)
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        # Check each neighbor
        for nr, nc in neighbors:
          # Check if the neighbor is within grid bounds
          if is_within_bounds(nr, nc, height, width):
            # Check if the neighbor cell in the *input* grid is 0
            if input_grid[nr][nc] == 0:
              # If conditions met, update the corresponding cell in the *output* grid to 2
              output_grid[nr][nc] = 2

  # Return the final transformed grid
  return output_grid
```