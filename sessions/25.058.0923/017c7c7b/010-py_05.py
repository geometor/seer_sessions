"""
1. Identify: Recognize the alternating pattern of 0s and 1s in the input, where 1 represents blue.
2. Create Output: Generate an output grid that is always 3 rows high and matches the width of the input grid.
3. Substitute: In the output grid, replace all positions that were blue (1) in the input with red (2). The positions follow the alternating pattern.
4. Preserve: Keep all white (0) pixels unchanged.
5. Maintain: The output grid maintains the checkerboard pattern of the input, but with a fixed height of 3 rows and with blue (1) replaced by red (2).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with 3 rows and the same width as the input, filled with white (0)
    input_height, input_width = input_grid.shape
    output_height = 3
    output_grid = np.zeros((output_height, input_width), dtype=int)
    
    # Fill the output grid with the checkerboard pattern, substituting blue with red
    for row in range(output_height):
      for col in range(input_width):
          if (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0): # Checkerboard pattern positions.
              output_grid[row, col] = 2  # change to red (2)
          else:
              output_grid[row,col] = 0 # Stays white (0)

    return output_grid