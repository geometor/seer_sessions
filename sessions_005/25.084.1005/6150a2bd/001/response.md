```python
"""
Take the input grid.
Rotate the entire grid by 180 degrees around its center point.
The resulting grid is the output.
"""

import numpy as np

def rotate_180(grid):
  """
  Rotates a 2D numpy array by 180 degrees.

  Args:
    grid: A 2D numpy array representing the input grid.

  Returns:
    A 2D numpy array representing the grid rotated by 180 degrees.
  """
  # np.rot90 rotates 90 degrees counter-clockwise by default.
  # Applying it twice results in a 180-degree rotation.
  return np.rot90(grid, k=2)


def transform(input_grid):
    """
    Transforms the input grid by rotating it 180 degrees.

    Args:
      input_grid: A 2D list or numpy array representing the input grid.

    Returns:
      A 2D numpy array representing the transformed grid.
    """
    # Convert input_grid to a numpy array if it's not already
    np_input_grid = np.array(input_grid, dtype=int)

    # Rotate the grid by 180 degrees
    output_grid = rotate_180(np_input_grid)

    # Return the rotated grid
    return output_grid

```