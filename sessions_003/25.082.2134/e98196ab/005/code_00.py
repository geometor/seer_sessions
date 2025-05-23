"""
1.  **Locate Separator:** Find the index of the horizontal line consisting entirely of grey (5) pixels within the input grid. This line is the separator.

2.  **Copy Upper Region:** Copy all rows of the input grid *above* the separator line to a new grid (the output grid).

3.  **Overlay from Lower Region:** Iterate through the rows *below* the separator line in the input grid. For each non-zero pixel found:
    *   Determine the corresponding column index (same as in the input grid).
    *   Iterate over rows of the output_grid, starting with index 0:
        * If the current row index of the *output_grid* exists, set that pixel to the non-zero pixel of the *input_grid*.
        * If the current row index of the *output_grid* does not exist, create a new row of zeros in *output_grid* and set that pixel to the non-zero pixel of the *input_grid*
4. **Remove all-zero rows**: After all the rows below the separator have been processed, eliminate all rows in *output_grid* that contain only zeros.
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
    insert_row = 0
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
        insert_row += 1

    # Delete any all-zero rows
    output_grid = [row for row in output_grid if any(x != 0 for x in row)]

    return output_grid