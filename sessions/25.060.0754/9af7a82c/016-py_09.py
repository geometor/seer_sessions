"""
Copies input grid columns to corresponding output grid columns. 
Then, based on which source column we are looking at:
- column 3: horizontal fill with 0 to the right on the same row
- column 4: horizontal fill with 0 to the right, and vertical down.
- column 1 and 2: vertical fill with 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros, sized 5x4
    output_grid = np.zeros((5, 4), dtype=int)

    # Get input grid dimensions
    input_rows, input_cols = input_grid.shape

    # Copy Column 1 to Output Column 1, fill the remaining rows of output col 1 with 0.
    for i in range(min(input_rows, output_grid.shape[0])):
        output_grid[i, 0] = input_grid[i, 0]
    #for i in range(input_rows, 5):
    #    output_grid[i, 0] = 0
    
    # Copy Column 2 to Output Column 2, fill the remaining rows of output col 2 with 0.
    for i in range(min(input_rows, output_grid.shape[0])):
        output_grid[i, 1] = input_grid[i, 1]
    #for i in range(input_rows, 5):
    #    output_grid[i, 1] = 0

    # Copy Column 3 to Output Column 3.  Fill cells to right with 0.
    for i in range(min(input_rows, output_grid.shape[0])):
        output_grid[i, 2] = input_grid[i, 2]
        for j in range(3, 4):  # Fill to the right
            output_grid[i, j] = 0

    # Copy Column 4 to Output Column 4, fill cells to right and below with 0.
    for i in range(min(input_rows, output_grid.shape[0])):
        output_grid[i, 3] = input_grid[i, 3]
        for j in range(i, 5):
           output_grid[j,3] = 0


    return output_grid