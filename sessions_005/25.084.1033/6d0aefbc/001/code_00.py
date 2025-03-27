"""
Take the input grid, create a horizontally flipped copy of it, and then concatenate the original grid and the flipped grid side-by-side horizontally to form the output grid.
"""

import numpy as np

def reflect_horizontal(grid):
  """Horizontally reflects a grid."""
  return np.fliplr(grid)

def concatenate_horizontal(grid1, grid2):
  """Concatenates two grids horizontally."""
  return np.concatenate((grid1, grid2), axis=1)

def transform(input_grid):
    """
    Transforms the input grid by concatenating it with its horizontal reflection.
    
    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Create a horizontally flipped copy of the input grid
    reflected_grid = reflect_horizontal(input_np)
    
    # Concatenate the original input grid and the reflected grid horizontally
    output_np = concatenate_horizontal(input_np, reflected_grid)

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
