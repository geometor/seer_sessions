"""
The transformation extracts a 2x2 subgrid from the top row of the input grid.
The subgrid is always aligned to the right, in other words, the final column of the input grid is the final column of the output grid.
The first column of the output subgrid will be the column preceding the final column of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_array = np.array(input_grid)
    
    # Get the width of the input array.
    width = input_array.shape[1]
    
    # Extract the 2x2 subgrid from the top-right corner,
    # specifically the last two columns and the first two rows.
    output_array = input_array[:2, width-2:]
    
    # Convert the result back to a list.
    output_grid = output_array.tolist()

    return output_grid