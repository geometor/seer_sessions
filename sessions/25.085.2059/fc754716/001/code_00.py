"""
Identifies the single non-white pixel color in the input grid and uses this color to draw a border on an output grid of the same dimensions, filling the interior with white.
"""

import numpy as np

def find_non_white_color(grid):
  """Finds the color of the single non-white pixel in the grid."""
  for r in range(grid.shape[0]):
    for c in range(grid.shape[1]):
      if grid[r, c] != 0:
        return grid[r, c]
  # Should not happen based on task description, but return a default if no non-white found
  return 0 

def transform(input_grid):
    """
    Transforms the input grid by creating a border with the color of the
    single non-white pixel found in the input.
    """
    # Convert input list of lists to a numpy array
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    height, width = input_np.shape
    
    # Find the color of the unique non-white pixel in the input grid
    border_color = find_non_white_color(input_np)
    
    # Create a new output grid of identical dimensions, initialized with white (0)
    output_grid = np.zeros((height, width), dtype=int)
    
    # Fill the border pixels with the identified color
    # Top row
    output_grid[0, :] = border_color
    # Bottom row
    output_grid[height - 1, :] = border_color
    # First column (excluding corners already set)
    output_grid[1:-1, 0] = border_color
    # Last column (excluding corners already set)
    output_grid[1:-1, width - 1] = border_color
            
    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()
