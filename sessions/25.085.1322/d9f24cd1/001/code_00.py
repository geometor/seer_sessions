"""
1. Initialize the output grid as a copy of the input grid.
2. Identify the indices of the columns that contain a red (2) pixel in the last row of the input grid.
3. For each identified column index:
   a. Iterate through all rows of that column.
   b. If the pixel at the current row and identified column index in the *input* grid is white (0), change the corresponding pixel in the *output* grid to red (2).
   c. If the pixel was gray (5) or already red (2) in the input, it remains unchanged in the output (handled by initial copy).
"""

import numpy as np

def transform(input_grid):
    """
    Fills columns with red (2) based on red markers in the last row,
    preserving existing gray (5) pixels.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the grid
    height, width = input_array.shape
    
    # Initialize output_grid as a copy of the input grid
    output_array = np.copy(input_array)
    
    # Identify the indices of columns containing red (2) in the last row
    last_row_index = height - 1
    red_marker_columns = np.where(input_array[last_row_index, :] == 2)[0]
    
    # Iterate through each identified column index
    for col_idx in red_marker_columns:
        # Iterate through all rows for this column
        for row_idx in range(height):
            # Check if the pixel in the *original* input grid at this position is white (0)
            if input_array[row_idx, col_idx] == 0:
                # If it's white, change the corresponding pixel in the *output* grid to red (2)
                output_array[row_idx, col_idx] = 2
                
    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid
