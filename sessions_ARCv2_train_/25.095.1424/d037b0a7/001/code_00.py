"""
Transforms an input grid by propagating the last seen non-zero value downwards within each column.
1.  Creates a copy of the input grid to serve as the output grid.
2.  Iterates through each column of the grid.
3.  Within each column, iterates through the rows from top to bottom.
4.  Keeps track of the 'last_non_zero_value' encountered in the current column.
5.  If a cell in the input grid contains a non-zero value, updates 'last_non_zero_value'.
6.  If a cell in the input grid contains zero and 'last_non_zero_value' is non-zero, 
    sets the corresponding cell in the output grid to 'last_non_zero_value'.
7.  Returns the modified output grid.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the downward propagation transformation to the input grid.

    Args:
        input_grid: A list of lists representing the 2D integer grid.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Ensure the input is not empty
    if not input_grid or not input_grid[0]:
        return []

    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    # This preserves original non-zero values and provides a canvas to modify zeros
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each column
    for c in range(width):
        # Initialize the last non-zero value seen in this column
        last_non_zero_value = 0
        # Iterate through each row in the current column, from top to bottom
        for r in range(height):
            # Get the value from the original input grid for checking
            input_value = input_grid[r][c]

            # Check if the current cell in the input grid is non-zero
            if input_value != 0:
                # Update the last non-zero value seen in this column
                last_non_zero_value = input_value
            # Else, if the current cell in the input grid is zero AND we have seen a non-zero value above it
            elif last_non_zero_value != 0:
                # Update the corresponding cell in the output grid with the last non-zero value
                output_grid[r][c] = last_non_zero_value

    # Return the transformed grid
    return output_grid