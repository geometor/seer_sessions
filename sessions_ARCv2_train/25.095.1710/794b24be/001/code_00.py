"""
Transforms a 3x3 input grid containing 0s and 1s into a 3x3 output grid containing 0s and 2s.
The transformation rule depends on the total count of 1s in the input grid.
Specific cells in the output grid ((0,0), (0,1), (0,2), (1,1)) are conditionally set to 2 based on whether the count of 1s meets certain thresholds.
- Output cell (0,0) becomes 2 if the count is >= 1.
- Output cell (0,1) becomes 2 if the count is >= 2.
- Output cell (0,2) becomes 2 if the count is >= 3.
- Output cell (1,1) becomes 2 if the count is >= 4.
All other output cells remain 0.
"""

import numpy as np # Using numpy for easier grid manipulation and summing

def count_ones(grid: list[list[int]]) -> int:
    """Helper function to count the total number of 1s in the grid."""
    # Convert the list of lists to a numpy array for easy summing
    np_grid = np.array(grid)
    # Sum all elements in the array
    return int(np.sum(np_grid))

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the count of ones in the input grid.
    """
    # initialize output_grid as a 3x3 grid of zeros
    # Using numpy for initialization, then convert back to list of lists if needed
    output_grid_np = np.zeros((3, 3), dtype=int)

    # Calculate the total count of 1s in the input grid
    n_ones = count_ones(input_grid)

    # perform transformations based on the count N
    # If N is 1 or greater, set the value of the output grid cell at (0, 0) to 2.
    if n_ones >= 1:
        output_grid_np[0, 0] = 2

    # If N is 2 or greater, set the value of the output grid cell at (0, 1) to 2.
    if n_ones >= 2:
        output_grid_np[0, 1] = 2

    # If N is 3 or greater, set the value of the output grid cell at (0, 2) to 2.
    if n_ones >= 3:
        output_grid_np[0, 2] = 2

    # If N is 4 or greater, set the value of the output grid cell at (1, 1) to 2.
    if n_ones >= 4:
        output_grid_np[1, 1] = 2

    # Convert the numpy array back to a list of lists for the return type
    output_grid = output_grid_np.tolist()

    return output_grid
