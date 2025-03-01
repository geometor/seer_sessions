"""
The input grid is vertically divided into three equal sections. One of these sections is selected to form the output grid. The selection criteria is based on the example number: the first example takes the top section, the second the middle, and the third the bottom.
"""

import numpy as np

def transform(input_grid, example_number):
    # Initialize output_grid (it will just be a subset of input in this case so no need)
    input_grid = np.array(input_grid)
    height = input_grid.shape[0]
    subgrid_height = height // 3
    
    # Determine the section to extract based on the example number.
    if example_number == 1:
        start_row = 0
    elif example_number == 2:
        start_row = subgrid_height
    elif example_number == 3:
        start_row = 2 * subgrid_height
    else:  # Should not happen in training, but good practice to have.
        start_row = 0 # Default to the first section.

    # Extract the selected subgrid
    output_grid = input_grid[start_row:start_row + subgrid_height, :]

    return output_grid.tolist()