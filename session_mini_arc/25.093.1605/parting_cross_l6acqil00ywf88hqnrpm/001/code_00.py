"""
Transform a 5x5 input grid by mapping its top-left 2x2 values 
(indices [0:2, 0:2]) to the corners of a 3x3 pattern placed in the 
bottom-right of the output grid (indices [2:5, 2:5]), filling the 
non-corner cells of the 3x3 pattern with 5. The rest of the output 
grid is filled with 0.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or numpy array): The 5x5 input grid.

    Returns:
        numpy array: The transformed 5x5 output grid.
    """
    # Convert input to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Create a new 5x5 grid, initialized entirely with zeros
    output_grid = np.zeros((5, 5), dtype=int)

    # 2. Fill the 3x3 subgrid (rows 2-4, columns 2-4) with 5
    fill_value = 5
    output_grid[2:5, 2:5] = fill_value

    # 3. Map input[0, 0] to output[2, 2]
    output_grid[2, 2] = input_np[0, 0]

    # 4. Map input[0, 1] to output[2, 4]
    output_grid[2, 4] = input_np[0, 1]

    # 5. Map input[1, 0] to output[4, 2]
    output_grid[4, 2] = input_np[1, 0]

    # 6. Map input[1, 1] to output[4, 4]
    output_grid[4, 4] = input_np[1, 1]

    # 7. Return the resulting grid
    return output_grid
