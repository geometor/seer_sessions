"""
Transforms a 5x5 input grid into a 5x5 output grid.
The transformation first copies the input grid to the output grid.
Then, it identifies the four values in the top-left 2x2 corner of the input grid.
Finally, it updates specific cells in the bottom-right 3x3 area of the output grid
using the values identified from the top-left input corner according to a fixed mapping:
- output[2][2] = input[1][0]
- output[2][3] = input[1][1]
- output[3][2] = input[0][0]
- output[3][3] = input[0][1]
- output[4][4] = input[1][1]
"""

import copy

def transform(input_grid):
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid (list of list of int): The 5x5 input grid.

    Returns:
        list of list of int: The transformed 5x5 output grid.
    """
    # Initialize output_grid as a deep copy of the input_grid to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)

    # Check if the grid has the expected dimensions (at least 2x2 for the source pattern)
    if len(input_grid) < 2 or len(input_grid[0]) < 2:
        # Handle cases where the grid is too small, maybe return the copy or raise an error
        # For this specific task based on examples, we assume 5x5, but defensively check 2x2 source
        return output_grid 

    # Extract the values from the top-left 2x2 subgrid of the input
    val_a = input_grid[0][0] # Top-left
    val_b = input_grid[0][1] # Top-right
    val_c = input_grid[1][0] # Bottom-left
    val_d = input_grid[1][1] # Bottom-right

    # Check if the grid has the expected dimensions for the target pattern (at least 5x5)
    if len(output_grid) < 5 or len(output_grid[0]) < 5:
         # Handle cases where the grid is too small for the target placement
         # For this specific task, we expect 5x5, so this might indicate an issue
         return output_grid # Or raise an error depending on desired behavior

    # Update the specific cells in the output grid's bottom-right 3x3 area
    # based on the extracted values
    output_grid[2][2] = val_c
    output_grid[2][3] = val_d
    output_grid[3][2] = val_a
    output_grid[3][3] = val_b
    output_grid[4][4] = val_d

    # Return the modified output grid
    return output_grid