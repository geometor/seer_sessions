"""
Constructs a larger grid by tiling the input grid and its horizontally flipped version in a specific 3x3 pattern.
The output grid has dimensions 3 times the height and 3 times the width of the input grid.
The tiling pattern consists of 3 rows and 3 columns of blocks, each the size of the input grid.
Blocks in the top (row 0) and bottom (row 2) rows are copies of the input grid.
Blocks in the middle row (row 1) are horizontally flipped copies of the input grid.
"""

import numpy as np

def horizontal_flip(grid):
  """Horizontally flips a 2D numpy array."""
  return np.fliplr(grid)

def transform(input_grid):
  """
  Tiles the input grid and its horizontally flipped version to create a larger output grid.

  Args:
    input_grid: A 2D numpy array representing the input grid.

  Returns:
    A 2D numpy array representing the transformed output grid.
  """
  # Convert input list of lists to numpy array for easier manipulation
  input_np = np.array(input_grid, dtype=int)

  # Get the dimensions of the input grid
  H, W = input_np.shape

  # Create a horizontally flipped version of the input grid
  flipped_input = horizontal_flip(input_np)

  # Create the three rows of tiles needed for the output grid
  # Row 0: Tile the original input grid 3 times horizontally
  row0 = np.tile(input_np, (1, 3))
  # Row 1: Tile the flipped input grid 3 times horizontally
  row1 = np.tile(flipped_input, (1, 3))
  # Row 2: Tile the original input grid 3 times horizontally (same as row 0)
  row2 = np.tile(input_np, (1, 3))

  # Stack the three rows vertically to form the final output grid
  output_grid = np.vstack((row0, row1, row2))

  # Convert back to list of lists if necessary, though numpy array is often preferred
  return output_grid.tolist()