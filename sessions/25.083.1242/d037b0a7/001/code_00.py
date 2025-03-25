"""
The program identifies rows by looking at last columns, and using
those rows expands their values to output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = []

    # Iterate through each row of the input grid.
    for i, row in enumerate(input_grid):
        # Check the value in the last column of the current row.
        if row[-1] != 0:
            # append original row
            output_grid.append(row.tolist())
            #create new row for expansion
            new_row = row.copy()
            # get last column value
            last_col_val = row[-1]

            # Iterate though each element in the row starting from second to last element.
            for j in range(len(new_row)):
                #append last column to each element
                new_row[j] = last_col_val if input_grid[i,j] == 0 and j != len(new_row) - 1 else input_grid[i,j]

            output_grid.append(new_row.tolist())

        else:
            #append row
            output_grid.append(row.tolist())


    return output_grid