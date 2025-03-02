"""
1.  **Input and Output Grids:** The input and output grids have the same shape (height and width).
2.  **Color Identification**: Input grid have rows that consist of pixels with colors white(0) and blue(1).
3.  **Color Transformation**:
      - For each row, identify the position of first blue pixel.
      - Create output row of same length, and filled with white(0).
      - Replace white(0) in the output row with azure(8) at the identified position in step above.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    # Initialize output grid with all white (0) with the same shape as input
    output_grid = np.zeros_like(input_grid)

    # Iterate through each row
    for i in range(input_grid.shape[0]):
        # Find the index of the first blue (1) pixel in the row
        blue_indices = np.where(input_grid[i] == 1)[0]
        if len(blue_indices) > 0:
          #if blue pixel found
          first_blue_index = blue_indices[0]
          # Set the corresponding pixel in the output grid to azure (8)
          output_grid[i, first_blue_index] = 8
        else:
          #if no blue pixel found, copy input row to output
          output_grid[i] = input_grid[i]
    return output_grid.tolist()