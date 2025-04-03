"""
Transforms the input grid by performing a 180-degree rotation.
Each element at position (r, c) in the input grid is moved to position 
(num_rows - 1 - r, num_cols - 1 - c) in the output grid.
"""

import numpy as np

def rotate_180(grid):
  """
  Rotates a 2D grid by 180 degrees.
  
  Args:
    grid: A list of lists or numpy array representing the 2D grid.
  
  Returns:
    A numpy array representing the grid rotated by 180 degrees.
  """
  # Convert input to numpy array for easier manipulation
  input_array = np.array(grid, dtype=int)
  # Rotate the array 180 degrees (equivalent to two 90-degree rotations)
  rotated_array = np.rot90(input_array, k=2)
  return rotated_array

def transform(input_grid):
    """
    Applies a 180-degree rotation to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the rotated output grid.
    """
    
    # Perform the 180-degree rotation using the helper function
    output_array = rotate_180(input_grid)
    
    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid
