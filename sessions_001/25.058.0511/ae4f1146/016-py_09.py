"""
The transformation extracts all azure (8) pixels from the input grid and
constructs a new grid containing only those azure pixels, preserving their
original vertical positions, but arranging them into a single column. If
there are white (0) pixels between the azure pixels in the same column, these
are also included in the output, preserving their relative vertical positions to the
azure pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts azure pixels and any white pixels between them in the same columns,
    placing them in a single column in the output grid, preserving vertical
    order.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_list = []

    # Iterate through each column
    for c in range(cols):
        # find azure and white pixels
        azure_found = False
        temp_col = []
        for r in range(rows):
           if input_grid[r,c] == 8:
              azure_found = True
              temp_col.append(8)
           elif input_grid[r,c] == 0 and azure_found:
              temp_col.append(0)

        # extract data from temp
        if azure_found:
           output_list.extend(temp_col)

    # create the output
    if len(output_list) > 0:
      output_grid = np.array(output_list).reshape(-1,1)
      return output_grid.tolist()
    else:
      return []