"""
1.  Extract the Last Column: Examine the input grid and extract the values from the last column, forming a list.
2.  Determine Output Color: The output color is present in the last column. The specific element selected from the last column is the *last* element in the column.
3.  Create Output Grid: Create a new grid (output grid) with the same dimensions (number of rows and columns) as the input grid.
4.  Fill Output Grid: Fill every cell of the output grid with the determined output color (from step 2).
5.  Return Output Grid: Return the newly created and filled output grid.
"""

import numpy as np

def get_last_column(grid):
    """Helper function to extract the last column of a grid."""
    return [row[-1] for row in grid]

def get_last_element(column):
    """Helper function to get the last element of a list"""
    return column[-1]

def transform(input_grid):
    # Extract the Last Column
    last_column = get_last_column(input_grid)

    # Determine Output Color: last element of last column
    output_color = get_last_element(last_column)

    # Create Output Grid: same dimensions as input
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.full((rows, cols), output_color)

    # the output grid is already filled

    return output_grid.tolist()