"""
The transformation rule is as follows:
1. Identify Key Column: The program focuses on the fourth column (index 3) of the input grid, containing only the blue pixels.
2. Grid Reduction: Create output grid with dimensions based on number of unique values on either side.
3. Copy and Recolor: The column index with all the '1's from input is used to create the output, and then, the '1's are changed to '3's in the output grid. All other values are '0's.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # Find the column with all '1's (blue)
    key_column_index = -1
    for j in range(cols):
        if np.all(input_grid[:, j] == 1):
            key_column_index = j
            break
            
    #count unique values to left and right
    left_unique_count = len(np.unique(input_grid[:, :key_column_index]))
    right_unique_count = len(np.unique(input_grid[:, key_column_index+1:]))


    output_grid = np.zeros((rows, 3), dtype=int)
    
    if key_column_index != -1:
         # Create the output grid with reduced dimensions (e.g., same height, 3 columns).
        
        # Copy and recolor the key column to the new grid.
        output_grid[:, 1] = 3

    return output_grid.tolist()