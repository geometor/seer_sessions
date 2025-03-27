"""
Transforms an 11x11 input grid partitioned by Azure (8) lines into a 3x3 output grid. 
The input grid has Azure lines at rows 3, 7 and columns 3, 7, creating nine 3x3 subgrids.
The output grid's cell at (r, c) corresponds to the input subgrid starting at (r*4, c*4).
An output cell is set to Blue (1) if the corresponding 3x3 input subgrid contains exactly two Magenta (6) pixels. Otherwise, the output cell remains White (0).
"""

import numpy as np

def count_color_in_subgrid(grid, start_row, start_col, size, color):
  """Counts the occurrences of a specific color within a subgrid."""
  subgrid = grid[start_row:start_row+size, start_col:start_col+size]
  return np.count_nonzero(subgrid == color)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 3x3 numpy array representing the output grid.
    """
    # Initialize output_grid: 3x3, filled with White (0)
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Define the target color and count
    magenta_color = 6
    target_count = 2
    subgrid_size = 3

    # Iterate through the 3x3 output grid positions, which correspond to the 3x3 input subgrids
    for out_r in range(3):
        for out_c in range(3):
            # Calculate the top-left corner coordinates of the corresponding input subgrid
            # The partitioning lines are at indices 3 and 7, so subgrids start at 0, 4, 8
            in_r_start = out_r * 4
            in_c_start = out_c * 4
            
            # Count the number of Magenta pixels in the current 3x3 input subgrid
            magenta_count = count_color_in_subgrid(input_grid, in_r_start, in_c_start, subgrid_size, magenta_color)
            
            # Apply the transformation rule: if count is exactly 2, set output pixel to Blue (1)
            if magenta_count == target_count:
                output_grid[out_r, out_c] = 1 # Blue

    return output_grid
