"""
Copies each row from the input grid and places a reflected copy above or below the original row.
Some rows might have additional replications.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by vertically mirroring and duplicating each row.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid = np.array(input_grid)
    num_rows = input_grid.shape[0]
    output_grid = []

    # Iterate through each row of the input grid
    for i in range(num_rows):
        # Get the current row
        current_row = input_grid[i].tolist()

        # Add a copy above the current row
        output_grid.insert(0, current_row)
        output_grid.append(current_row)


    new_output = []
    for i in range(num_rows):
      for row in output_grid:
        new_output.append(row)
    output_grid = new_output


    return output_grid