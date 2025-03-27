"""
Construct the output grid by horizontally concatenating the input grid, a
horizontally flipped version of the input grid, the input grid again, the
flipped grid again, and finally the input grid one last time. The sequence is
[original, flipped, original, flipped, original]. The height remains the same,
and the width becomes 5 times the original width.
"""

import numpy as np

def flip_horizontal(grid):
  """
  Flips a grid horizontally.
  Args:
    grid: A NumPy array representing the grid.
  Returns:
    A NumPy array representing the horizontally flipped grid.
  """
  return grid[:, ::-1]

def transform(input_grid):
  """
  Transforms the input grid according to the rule: concatenate the original
  grid, its horizontal flip, the original, the flip, and the original again.
  Args:
    input_grid: A list of lists representing the input grid.
  Returns:
    A list of lists representing the transformed output grid.
  """
  # Convert input list of lists to a NumPy array for easier manipulation
  grid_np = np.array(input_grid, dtype=int)

  # Create the horizontally flipped version of the grid
  flipped_grid_np = flip_horizontal(grid_np)

  # Concatenate the grids in the specified order: [original, flipped, original, flipped, original]
  output_grid_np = np.concatenate(
      (grid_np, flipped_grid_np, grid_np, flipped_grid_np, grid_np),
      axis=1 # Concatenate along the columns (horizontally)
  )

  # Convert the resulting NumPy array back to a list of lists
  output_grid = output_grid_np.tolist()

  return output_grid