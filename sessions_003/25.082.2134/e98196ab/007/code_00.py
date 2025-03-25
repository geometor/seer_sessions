"""
1.  **Locate Separator:** Find the horizontal line consisting entirely of grey (5) pixels within the input grid. This is the separator.

2.  **Copy Upper Region:** Copy all rows of the input grid *above* the separator line to a new, initially empty, output grid.

3.  **Overlay from Lower Region:** Iterate through the rows *below* the separator line in the input grid. For each non-zero pixel found:
    *   Determine the corresponding column index (the same as in the input grid).
    *   Determine the insert row. The insert row is incremented with each row below the separator.
    *   If the insert row is within the current bounds of the output grid, set the pixel at that row and the determined column in `output_grid` to the non-zero value from the lower region.
    *   If the insert row is beyond the current bounds of the `output_grid` (i.e. the output grid needs to grow), create a new row of zeros, set the pixel in the determined column to be the non-zero value from the lower region, and add that row to the `output_grid`.

4.  **Remove all-zero rows:** After all rows below the separator are processed, eliminate any rows from the output grid containing only zeros.
"""

import numpy as np

def find_grey_line(grid):
    # Find the row index of the grey line (all 5s).
    for i, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            return i
    return -1  # Grey line not found

def transform(input_grid):
    input_grid = np.array(input_grid)
    grey_line_index = find_grey_line(input_grid)
    output_grid = []

    # Copy rows above the grey line
    for i in range(grey_line_index):
        output_grid.append(list(input_grid[i]))

    # Insert non-zero elements from below grey line, overlaying onto copied region.
    insert_row = 0  # Initialize insert_row to 0
    for i in range(grey_line_index + 1, len(input_grid)):
        for j in range(len(input_grid[0])):
            if input_grid[i][j] != 0:
                if insert_row < len(output_grid):
                    # Overlay if row exists
                    output_grid[insert_row][j] = input_grid[i][j]
                else:
                    # Create a new row of zeros and then insert
                    new_row = [0] * len(input_grid[0])
                    new_row[j] = input_grid[i][j]
                    output_grid.append(new_row)
        insert_row += 1 # Increment the insertion row

    # Delete any all-zero rows
    output_grid = [row for row in output_grid if any(x != 0 for x in row)]

    return output_grid