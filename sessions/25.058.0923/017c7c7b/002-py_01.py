"""
Iterate through each pixel in the input grid. If a pixel is blue (1), change it to red (2) in the output grid.
If a pixel is white (0), keep it white (0) in the output grid. Add an additional row on the bottom of the grid.
Copy row 3 to row 7 and row 4 to row 8. Add an additional final row with the pattern 0,2,0.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with extra rows
    input_rows, input_cols = input_grid.shape
    output_grid = np.zeros((input_rows + 3, input_cols), dtype=int)

    # Change blue pixels to red, keep white pixels
    for i in range(input_rows):
        for j in range(input_cols):
            if input_grid[i, j] == 1:
                output_grid[i, j] = 2
            else:
                output_grid[i, j] = input_grid[i,j]

    # Copy row 3 to row 7 and row 4 to 8
    output_grid[input_rows] = output_grid[2]
    output_grid[input_rows+1] = output_grid[3]

    # Add final row with the pattern
    output_grid[input_rows+2] = [0,2,0]

    return output_grid