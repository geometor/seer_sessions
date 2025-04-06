"""
Transforms a 5x5 input grid into a 5x5 output grid.
The transformation first copies the input grid to the output grid.
The top-left 2x2 subgrid (indices [0:2, 0:2]) of the output remains identical to the input.
The bottom-right 3x3 subgrid (indices [2:5, 2:5]) of the output is modified based on the values
from the input's top-left 2x2 subgrid, denoted as [[a, b], [c, d]].
The cell output[4][4] is always set to the value d (input[1][1]).
The central 2x2 block within the bottom-right 3x3 (output[2:4, 2:4]) is populated based on a condition:
- If a == c == d, then:
    output[2][2] = c (input[1][0])
    output[2][3] = d (input[1][1])
    output[3][2] = a (input[0][0])
    output[3][3] = b (input[0][1])
- Otherwise:
    output[2][2] = c (input[1][0])
    output[2][3] = b (input[0][1])
    output[3][2] = d (input[1][1])
    output[3][3] = a (input[0][0])
"""

import copy

def transform(input_grid):
    """
    Applies the described conditional transformation to the input grid.

    Args:
        input_grid (list of list of int): The 5x5 input grid.

    Returns:
        list of list of int: The transformed 5x5 output grid.
    """
    # Initialize output_grid as a deep copy of the input_grid
    output_grid = copy.deepcopy(input_grid)

    # Basic dimension checks to ensure we can access the required indices
    if len(input_grid) < 2 or len(input_grid[0]) < 2:
        # Cannot extract the 2x2 source pattern
        return output_grid 
    if len(output_grid) < 5 or len(output_grid[0]) < 5:
        # Cannot place the target pattern
        return output_grid

    # Extract the values from the top-left 2x2 subgrid of the input
    a = input_grid[0][0] # Top-left
    b = input_grid[0][1] # Top-right
    c = input_grid[1][0] # Bottom-left
    d = input_grid[1][1] # Bottom-right

    # Apply the conditional mapping to the central 2x2 block of the target area
    if a == c and c == d: # Check if a, c, and d are all equal
        output_grid[2][2] = c
        output_grid[2][3] = d
        output_grid[3][2] = a
        output_grid[3][3] = b
    else:
        # The alternative mapping observed in train_3
        output_grid[2][2] = c
        output_grid[2][3] = b
        output_grid[3][2] = d
        output_grid[3][3] = a

    # Set the bottom-right corner of the target area
    output_grid[4][4] = d

    # Return the modified output grid
    return output_grid