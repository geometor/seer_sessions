"""
Iterate through each row of the input grid.
Compare the current row with all previously encountered rows.
If the current row is identical to any previously seen row, skip it.
If the current row is not identical to any previously seen row, add the entire row as a new row in the output grid.
The output should contain a list of unique rows from the input.
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
            #append the whole row
            output_grid.append(list(row))

    return output_grid