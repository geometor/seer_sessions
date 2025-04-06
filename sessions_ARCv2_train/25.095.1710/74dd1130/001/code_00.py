import math
import collections

"""
Take the input 3x3 grid. Create a new, empty 3x3 grid for the output. 
For each element in the input grid at position (row, column), place that element 
into the output grid at position (column, row). The resulting grid is the final output.
This operation is known as transposing the grid.
"""

# No external libraries beyond standard Python are needed for this operation

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transposes a given grid (list of lists).

    Args:
        input_grid: A list of lists representing the input grid. Assumed to be
                    non-empty and rectangular (though examples are 3x3).

    Returns:
        A new list of lists representing the transposed grid.
    """

    # Get the dimensions of the input grid
    num_rows = len(input_grid)
    # Handle potential empty grid
    if num_rows == 0:
        return []
    num_cols = len(input_grid[0])
    # Handle potential grid with empty rows
    if num_cols == 0:
        return [[] for _ in range(num_rows)]

    # Initialize the output grid with swapped dimensions
    # Rows of output = columns of input, Columns of output = rows of input
    # Initialize with a placeholder (like 0 or None) - using 0 here.
    output_grid = [[0 for _ in range(num_rows)] for _ in range(num_cols)]

    # Iterate through each element of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            # Perform the transpose: element at input[r][c] goes to output[c][r]
            output_grid[c][r] = input_grid[r][c]

    # Return the newly created transposed grid
    return output_grid