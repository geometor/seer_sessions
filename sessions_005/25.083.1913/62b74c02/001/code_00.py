"""
Copy edge value to the edges.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for i in range(rows):
        # Find non-zero indices in the current row
        non_zero_indices = np.nonzero(input_grid[i, :])[0]

        # If there are non-zero elements in the row
        if non_zero_indices.size > 0:
            # Get the leftmost and rightmost non-zero indices
            leftmost_index = non_zero_indices[0]
            rightmost_index = non_zero_indices[-1]

            # Fill values to the left
            output_grid[i, :leftmost_index] = input_grid[i, leftmost_index]

            # Fill the values between the non-zero values
            for j in range(len(non_zero_indices) - 1):
               left_index =  non_zero_indices[j]
               right_index = non_zero_indices[j+1]
               output_grid[i,left_index:right_index+1] = input_grid[i,left_index]

            # Fill values to the right
            output_grid[i, rightmost_index + 1:] = input_grid[i, rightmost_index]
        
    return output_grid