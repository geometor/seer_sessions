"""
Iterate through each row of the input grid.
For each row, check if an identical row has already been processed.
If the row is unique (not seen before), take the first element (pixel value) of that row.
Create a new row in the output grid containing only the extracted first element.
If the row is a duplicate, skip it and proceed to the next row.
The output is a grid whose rows are the first element of each unique row in the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = []

    # Iterate through each row of input grid
    seen_rows = []
    for row in input_grid:
        # Convert row to tuple for efficient comparison
        row_tuple = tuple(row)
        # check if we've see this row before
        if row_tuple not in seen_rows:
            #add this to the rows we have seen
            seen_rows.append(row_tuple)
            #append the first element of the row as a new row
            output_grid.append([row[0]])

    return output_grid