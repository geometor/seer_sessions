"""
The transformation rule involves identifying rows containing white pixels in the input grid. For each such row, three rows are added to the output grid. The first of these three rows has white pixels in the first and last columns, and the other columns are red. The following two rows are all red.  If there are no white pixels in any input rows then there should not be any output.

The width of the output grid is always 4.

"""

import numpy as np

def transform(input_grid):
    # Find rows with white pixels
    white_rows = np.any(input_grid == 0, axis=1)
    input_white_row_indices = np.where(white_rows)[0]

    # Calculate output height: 3 rows for each input row with white.
    output_height = len(input_white_row_indices) * 3
    output_width = 4

    # Initialize output_grid with red (2) if there are any white rows; otherwise return an empty array
    if output_height > 0:
      output_grid = np.full((output_height, output_width), 2)
    else:
      return np.empty((0,4))


    # Create output rows based on input white rows
    output_row_index = 0
    for i in input_white_row_indices:
        # White row
        output_grid[output_row_index, 0] = 0
        output_grid[output_row_index, 3] = 0
        output_row_index += 1
        # Add two more rows, that are all red
        output_row_index += 1
        output_row_index += 1
    

    return output_grid