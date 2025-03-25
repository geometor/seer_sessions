"""
Extract the 2x2 subgrid from the top-left corner of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Extract the 2x2 subgrid from the top-left corner.
    output_array = input_array[:2, :2]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    
    return output_grid