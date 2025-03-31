import numpy as np

"""
Transforms an input grid into a 15x15 output grid by following these steps:
1. Initialize a 15x15 output grid filled with orange (7).
2. Extract the "inner pattern" from the input grid by removing the outermost 1-pixel border.
3. Place a copy of the inner pattern onto the output grid starting at position (row=2, col=2).
4. Place another copy of the inner pattern onto the output grid starting at position (row=8, col=8).
"""

def extract_inner_pattern(grid):
  """
  Extracts the subgrid excluding the 1-pixel border.

  Args:
    grid: A numpy array representing the input grid.

  Returns:
    A numpy array representing the inner pattern.
  """
  return grid[1:-1, 1:-1]

def place_pattern(output_grid, pattern, start_row, start_col):
  """
  Places a pattern onto a grid at specified coordinates.

  Args:
    output_grid: The numpy array representing the grid to place onto.
    pattern: The numpy array representing the pattern to place.
    start_row: The starting row index for placement.
    start_col: The starting column index for placement.
  """
  pattern_height, pattern_width = pattern.shape
  output_grid[start_row : start_row + pattern_height, 
              start_col : start_col + pattern_width] = pattern

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
      input_grid: A list of lists representing the input grid.

    Returns:
      A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Define output grid properties
    output_height = 15
    output_width = 15
    background_color = 7
    
    # 1. Initialize the output grid with the background color
    output_grid = np.full((output_height, output_width), background_color, dtype=int)
    
    # 2. Extract the inner pattern from the input grid
    inner_pattern = extract_inner_pattern(input_np)
    
    # 3. Place the first copy of the inner pattern
    #    Target top-left corner: (row=2, col=2)
    place_pattern(output_grid, inner_pattern, start_row=2, start_col=2)
    
    # 4. Place the second copy of the inner pattern
    #    Target top-left corner: (row=8, col=8)
    place_pattern(output_grid, inner_pattern, start_row=8, start_col=8)

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()