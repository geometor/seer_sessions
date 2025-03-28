"""
For each white pixel in the input grid, determine if it is horizontally bounded by red pixels
within its row. If it is, change its color to maroon in the output grid. Otherwise, keep its color.
All non-white pixels retain their original color in the output grid.

Specifically:
1. Create the output grid as an identical copy of the input grid.
2. For each row in the grid:
   a. Find the column indices of all red (2) pixels within that row.
   b. If there are at least two red pixels in the row:
      i. Determine the minimum column index (`min_red_col`) and the maximum column index (`max_red_col`) of the red pixels in that row.
      ii. For each column index `col` strictly between `min_red_col` and `max_red_col`:
         1. If the pixel at (`row`, `col`) in the input grid is white (0), change the color of the pixel at (`row`, `col`) in the output grid to maroon (9).
3. Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing white pixels (0) to maroon (9) 
    if they are horizontally located between two red pixels (2) in the same row.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_array)
    
    height, width = input_array.shape

    # Iterate through each row of the grid
    for r in range(height):
        # Find the column indices of all red (2) pixels in the current row
        red_indices = np.where(input_array[r, :] == 2)[0]
        
        # Proceed only if there are at least two red pixels in the row
        if len(red_indices) >= 2:
            # Find the minimum and maximum column index of red pixels in this row
            min_red_col = np.min(red_indices)
            max_red_col = np.max(red_indices)
            
            # Iterate through the columns strictly between the min and max red pixel columns
            for c in range(min_red_col + 1, max_red_col):
                # Check if the pixel in the original input grid at this location is white (0)
                if input_array[r, c] == 0:
                    # If it's white and between two red pixels horizontally, change it to maroon (9) in the output grid
                    output_grid[r, c] = 9

    # Convert the NumPy array back to a list of lists before returning
    return output_grid.tolist()
