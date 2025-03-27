```python
"""
Rotates the input grid by 180 degrees around its center point.
"""

import numpy as np

def rotate_180(grid):
  """Rotates a 2D list (grid) by 180 degrees."""
  # Convert the input list of lists to a numpy array
  np_grid = np.array(grid, dtype=int)
  
  # Rotate the numpy array 180 degrees (equivalent to two 90-degree rotations)
  rotated_grid = np.rot90(np_grid, 2)
  
  # Convert the rotated numpy array back to a list of lists
  return rotated_grid.tolist()

def transform(input_grid):
    """
    Applies a 180-degree rotation to the input grid.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the output grid after rotation.
    """
    
    # Perform the 180-degree rotation using the helper function
    output_grid = rotate_180(input_grid)

    # Return the rotated grid
    return output_grid

```