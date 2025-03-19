"""
1.  Identify: Recognize the alternating checkerboard pattern of 0s (white) and 1s (blue) in the input grid.
2.  Create Output: Generate an output grid.
3.  Determine Output Height:
    *   If the input grid's height is less than or equal to 3, set output height = 3.
    *   If the input grid's height is greater than 3, set output height = input height.
4.  Set Output Width: The output grid width is the same as the input grid width.
5.  Substitute Colors:** In the output grid, replace all positions that were blue (1) in the input with red (2), maintaining the checkerboard pattern.
6.  Preserve Colors:** Keep all white (0) pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    input_height, input_width = input_grid.shape
    
    # Determine output height
    if input_height <= 3:
        output_height = 3
    else:
        output_height = input_height
        
    output_grid = np.zeros((output_height, input_width), dtype=int)
    
    # change output pixels, substituting blue with red in checkerboard pattern
    for row in range(output_height):
      for col in range(input_width):
          if (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0): # Checkerboard pattern positions.
              output_grid[row, col] = 2  # change to red (2)
          else:
              output_grid[row,col] = 0 # Stays white (0)

    return output_grid