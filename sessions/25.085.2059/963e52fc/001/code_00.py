import copy

"""
The transformation takes an input grid and creates an output grid with the same 
height but double the width. The output grid's content is formed by horizontally
concatenating the input grid with an identical copy of itself.
"""

def transform(input_grid):
    """
    Duplicates the input grid horizontally to create the output grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the output grid, which is the
                         input grid duplicated horizontally.
    """
    # Get the dimensions of the input grid
    input_height = len(input_grid)
    if input_height == 0:
        return []  # Handle empty input grid
    input_width = len(input_grid[0])
    if input_width == 0:
        return [[] for _ in range(input_height)] # Handle grid with empty rows

    # Initialize the output grid (not strictly necessary with list concatenation)
    output_grid = []

    # Iterate through each row of the input grid
    for r in range(input_height):
        # Get the current row from the input
        input_row = input_grid[r]
        
        # Create the new row for the output grid by concatenating the input row with itself
        output_row = input_row + input_row
        
        # Append the newly created row to the output grid
        output_grid.append(output_row)

    return output_grid
