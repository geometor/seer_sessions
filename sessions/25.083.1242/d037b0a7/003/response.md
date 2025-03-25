```python
"""
The program identifies "source" rows by checking for non-zero values in their last element.
For each source row, it modifies subsequent "target" rows. It replaces zeros in the target row
with corresponding non-zero values from the source row, *excluding* the last element.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = []

    # Identify source rows (rows where the last element is not zero)
    source_rows_indices = [i for i, row in enumerate(input_grid) if row[-1] != 0]

    # Iterate through all rows to build the output grid
    row_index = 0
    while row_index < len(input_grid):
        row = input_grid[row_index]
        output_grid.append(row.tolist())  # Always append the original row first

        #if is source row,
        if row_index in source_rows_indices:

            #check next row if it exist
            if row_index + 1 < len(input_grid):

                next_row_index = row_index + 1

                #if next row index is less than len of input grid
                while next_row_index < len(input_grid):

                    #copy next row
                    modified_row = input_grid[next_row_index].copy()

                    #if last element are different, merge
                    if input_grid[next_row_index][-1] != input_grid[row_index][-1]:

                        # Iterate and merge
                        for j in range(len(modified_row) - 1):  # Exclude the last element
                            if modified_row[j] == 0 and row[j] != 0:
                                modified_row[j] = row[j]

                        output_grid.append(modified_row.tolist())
                    #if they are same, append current row copy
                    else:
                        output_grid.append(input_grid[row_index].tolist())


                    next_row_index += 1

        row_index += 1 #increment to next row

    return output_grid
```