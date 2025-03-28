"""
The input grid is expanded into a 9x9 grid. The original 3x3 input is placed in the top-left corner of the output grid. Certain parts of the input grid are replicated and positioned at specific locations within the output grid based on rows and columns, and empty cells default to white.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as 9x9 filled with white (0)
    output_grid = np.zeros((9, 9), dtype=int)

    # Copy the input_grid to the top-left corner of output_grid
    output_grid[:3, :3] = input_grid

    # Copy the top row of the input to output location (0,3)
    output_grid[0, 3:6] = input_grid[0, :]
    
    # copy the top row of the input to the output at (0,6)
    output_grid[0, 6:9] = input_grid[0, :]

    # copy the second row and third row to output locations (2,3) and (2,6)
    output_grid[2, 3:6] = input_grid[1:3, 1]
    output_grid[2, 5:8] = input_grid[1:3, 2]
    
    # copy columns two and three from the input to (6,3), (6,4), (6,5)
    output_grid[6:9, 3:6] =  input_grid[:,:]
    
    # copy column three to the ouput at (6,7), (6,8)
    output_grid[6:9, 7] = input_grid[:2, 2]
    output_grid[6, 8] = input_grid[2, 2]

    # copy row three to (8,4)
    output_grid[8, 4:6] = input_grid[2,1:]

    # copy elements (2,1) and (2,2) to output (8, 7) and (8,8)
    output_grid[8, 7:9] = input_grid[2, 1:]
    
    return output_grid