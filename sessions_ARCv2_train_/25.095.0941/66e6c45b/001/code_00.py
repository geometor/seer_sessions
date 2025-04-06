"""
1. Initialize a new 4x4 output grid, filling all cells with the value 0.
2. Identify the four values located in the central 2x2 subgrid of the input grid (at positions (1,1), (1,2), (2,1), and (2,2)).
3. Place the value from input grid position (1,1) into the output grid position (0,0).
4. Place the value from input grid position (1,2) into the output grid position (0,3).
5. Place the value from input grid position (2,1) into the output grid position (3,0).
6. Place the value from input grid position (2,2) into the output grid position (3,3).
7. The resulting output grid is the final output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving the values from the central 2x2 subgrid
    to the corners of a new grid.
    """
    # Convert input list of lists to a numpy array for easier indexing
    input_array = np.array(input_grid)
    
    # Get the dimensions of the input grid (assuming it's always 4x4 based on examples)
    rows, cols = input_array.shape
    
    # Initialize a new 4x4 output grid filled with zeros
    output_grid = np.zeros((rows, cols), dtype=int)

    # Identify the four values from the central 2x2 subgrid
    # input_grid[1][1] is the top-left of the central 2x2
    # input_grid[1][2] is the top-right of the central 2x2
    # input_grid[2][1] is the bottom-left of the central 2x2
    # input_grid[2][2] is the bottom-right of the central 2x2

    # Place the identified values into the corresponding corners of the output grid
    # Input (1,1) -> Output (0,0)
    output_grid[0, 0] = input_array[1, 1]
    # Input (1,2) -> Output (0,3)
    output_grid[0, cols - 1] = input_array[1, 2] # Use cols-1 for generality
    # Input (2,1) -> Output (3,0)
    output_grid[rows - 1, 0] = input_array[2, 1] # Use rows-1 for generality
    # Input (2,2) -> Output (3,3)
    output_grid[rows - 1, cols - 1] = input_array[2, 2]

    # Convert back to list of lists if necessary (often required by the framework)
    return output_grid.tolist()
