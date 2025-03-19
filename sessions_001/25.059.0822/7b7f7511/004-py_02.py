"""
The transformation rule is to remove every other column starting from the right.
Specifically, columns 5 and 7 are removed, leaving columns 1, 2, 3, 4, 6, and 8.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)
    
    # Get the number of columns in the input grid
    num_cols = input_array.shape[1]
    
    # Create a list of column indices to keep
    cols_to_keep = [i for i in range(num_cols) if (i+1) % 2 != 0 or (i+2) % 4 != 0 ]
    cols_to_keep = [i for i in range(num_cols//2) if (i*2) < num_cols]
    
    # Use array slicing to select the columns to keep
    output_array = input_array[:, cols_to_keep]
    
    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid