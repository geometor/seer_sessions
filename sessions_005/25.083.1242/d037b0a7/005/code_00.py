"""
The program identifies "source" rows as those having any non-zero elements.
For each source row, it copies it to the output, then modifies subsequent "target" rows.
It replaces zeros in the target row with corresponding non-zero values from the source row.
The last element of the source row is always copied to the last element of the target row.
This continues for consecutive target rows until the next source row or the end of the grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = []

    # Identify source rows (rows where any element is not zero)
    source_rows_indices = [i for i, row in enumerate(input_grid) if np.any(row != 0)]

    row_index = 0
    while row_index < len(input_grid):
        row = input_grid[row_index]

        if row_index in source_rows_indices:
            # Copy the source row to output
            output_grid.append(row.tolist())

            next_row_index = row_index + 1
            #check if we have subsequent rows
            while next_row_index < len(input_grid) and next_row_index not in source_rows_indices :
                modified_row = input_grid[next_row_index].copy()

                # Merge: Replace 0s in target with corresponding non-0s from source
                for j in range(len(modified_row) - 1):
                    if modified_row[j] == 0 and row[j] != 0:
                        modified_row[j] = row[j]

                #copy last element from source to target
                modified_row[-1] = row[-1]
                output_grid.append(modified_row.tolist())
                next_row_index += 1

            row_index = next_row_index

        #if not source row, just append
        else:
             output_grid.append(row.tolist())
             row_index+= 1

    return output_grid