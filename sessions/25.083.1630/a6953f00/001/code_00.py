"""
The transformation extracts the first two columns of the input grid to create the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Initialize the output grid as an empty list.
    output_grid = []
    
    # Get number of rows
    num_rows = input_array.shape[0]

    # Select the first two columns.
    selected_columns = input_array[:, :2]
    
    # Convert to list
    output_grid = selected_columns.tolist()
    

    return output_grid