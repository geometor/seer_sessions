"""
Downsamples the input grid to a 3x3 grid, representing the azure (8) cross-like structure with blue (1) and filtering out the magenta (6) noise.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Define the mapping between input and output grid coordinates.
    # This essentially divides the input grid into 3x3 regions, with overlap
    y_coords = [0, input_height//2, input_height - 1 ]
    x_coords = [0, input_width//2, input_width - 1 ]

    # Iterate through each cell of the output grid
    for i in range(3):
        for j in range(3):
            # Define the bounds of the corresponding region in the input grid
            y_start = y_coords[i]
            y_end = y_coords[i] + (input_height//2) + (input_height+1)%2
            x_start = x_coords[j]
            x_end = x_coords[j] + (input_width//2) + (input_width+1)%2

            # Extract subgrid
            subgrid = input_grid[y_start:y_end, x_start:x_end]
            
            # check if subgrid contained azure
            if 8 in subgrid:
                output_grid[i,j] = 1

    return output_grid.tolist()