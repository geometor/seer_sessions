```python
"""
Constructs the output grid by horizontally concatenating the input grid and its horizontal reflection in an alternating pattern. The sequence is: Input, Reflected, Input, Reflected, Input.
"""

import numpy as np

def reflect_horizontally(grid):
  """
  Reflects a grid horizontally (left-to-right).
  """
  return np.fliplr(grid)

def transform(input_grid):
  """
  Transforms the input grid according to the described pattern.

  Args:
    input_grid: A list of lists or numpy array representing the input grid.

  Returns:
    A numpy array representing the transformed output grid.
  """
  # Convert input to numpy array for easier manipulation
  grid_np = np.array(input_grid, dtype=int)

  # Create the horizontally reflected version of the input grid
  reflected_grid = reflect_horizontally(grid_np)

  # Define the sequence of grids to concatenate
  grids_to_concatenate = [
      grid_np,          # 1st block: Original input
      reflected_grid,   # 2nd block: Reflected input
      grid_np,          # 3rd block: Original input
      reflected_grid,   # 4th block: Reflected input
      grid_np           # 5th block: Original input
  ]

  # Concatenate the grids horizontally (along axis 1)
  output_grid = np.concatenate(grids_to_concatenate, axis=1)

  return output_grid

```