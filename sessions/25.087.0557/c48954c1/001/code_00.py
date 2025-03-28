"""
Takes a 3x3 input grid and produces a 9x9 output grid.
The output grid is constructed by tiling nine 3x3 subgrids.
The central subgrid is the original input grid.
Subgrids adjacent horizontally to the center are flipped horizontally.
Subgrids adjacent vertically to the center are flipped vertically.
Corner subgrids are flipped both horizontally and vertically.
"""

import numpy as np

def flip_horizontal(grid):
  """Flips a grid horizontally."""
  return np.fliplr(grid)

def flip_vertical(grid):
  """Flips a grid vertically."""
  return np.flipud(grid)

def flip_both(grid):
  """Flips a grid both horizontally and vertically."""
  return np.fliplr(np.flipud(grid))
  # Alternatively: return np.rot90(grid, 2)

def transform(input_grid):
    """
    Tiles a 3x3 grid of transformed versions of the input grid to create the output.
    """
    input_np = np.array(input_grid)
    h, w = input_np.shape

    # Calculate output dimensions
    output_h = h * 3
    output_w = w * 3

    # Initialize the output grid
    output_grid = np.zeros((output_h, output_w), dtype=input_np.dtype)

    # Generate the transformed versions of the input grid
    I = input_np
    Ih = flip_horizontal(I)
    Iv = flip_vertical(I)
    Ihv = flip_both(I)

    # Tile the output grid with the transformed subgrids
    # Top row
    output_grid[0:h, 0:w] = Ihv
    output_grid[0:h, w:2*w] = Iv
    output_grid[0:h, 2*w:3*w] = Ihv

    # Middle row
    output_grid[h:2*h, 0:w] = Ih
    output_grid[h:2*h, w:2*w] = I
    output_grid[h:2*h, 2*w:3*w] = Ih

    # Bottom row
    output_grid[2*h:3*h, 0:w] = Ihv
    output_grid[2*h:3*h, w:2*w] = Iv
    output_grid[2*h:3*h, 2*w:3*w] = Ihv

    return output_grid.tolist()