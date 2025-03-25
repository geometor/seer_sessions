```python
"""
1.  **Locate Separator:** Find the index of the horizontal line consisting entirely of grey (5) pixels within the input grid. This line acts as a separator.

2.  **Copy Upper Region:** Copy all rows of the input grid *above* the separator line to a new grid, which will become the output grid.

3.  **Insert from Lower Region:** Iterate through the rows *below* the separator line in the input grid. For each non-zero pixel found, insert its value into the output grid.
    -   The column index for insertion is the same as the column index in the input grid.
    -   The insertion starts by overlaying on the first row of the upper region.
    -   For each row below the seperator in the input, insert values into the corresponding next row of the output grid.

4.  **Remove Empty Rows:** After inserting all non-zero pixels, remove any rows in the output grid that consist entirely of zeros.
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

    # Insert non-zero elements below grey line into copied region.
    insert_row = 0
    for i in range(grey_line_index + 1, len(input_grid)):
        for j in range(len(input_grid[0])):
            if input_grid[i][j] != 0:
                if insert_row < len(output_grid):
                  output_grid[insert_row][j] = input_grid[i][j]
        insert_row += 1

    #delete any all-zero rows
    output_grid = [row for row in output_grid if any(x != 0 for x in row)]

    return output_grid
```