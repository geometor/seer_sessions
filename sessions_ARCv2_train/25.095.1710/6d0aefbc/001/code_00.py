"""
Transforms a 3x3 input grid into a 3x6 output grid. 
The output grid consists of the original input grid concatenated horizontally 
with a horizontally flipped version of the input grid.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x6 list of lists representing the transformed output grid.
    """

    # Get the dimensions of the input grid
    rows = len(input_grid)
    cols = len(input_grid[0]) # Assuming a non-empty grid

    # Initialize the output grid with the correct dimensions (3x6)
    # We can start by creating a deep copy of the input grid for the first half
    output_grid = [row[:] for row in input_grid] # Shallow copy of rows is ok here

    # Create the horizontally flipped version of the input grid
    flipped_grid = []
    for r in range(rows):
        # Reverse each row from the input grid
        flipped_row = input_grid[r][::-1]
        flipped_grid.append(flipped_row)

    # Concatenate the flipped grid to the output grid
    for r in range(rows):
        # Extend each row of the output grid with the corresponding row from the flipped grid
        output_grid[r].extend(flipped_grid[r])

    # Return the final 3x6 output grid
    return output_grid
