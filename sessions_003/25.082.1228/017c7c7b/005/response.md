```python
"""
Iterate through each row of the input grid. If a row contains any blue (1) pixels, replace all blue pixels in that row with red (2) pixels, and add the modified row to a new list of rows. After processing all rows, create a single "summary" row. The width of this row should match the width of the input grid. For each column position in the summary row check all of the rows in the input grid: if any of the original input grid rows had a blue pixel (1) at that column position, set the corresponding pixel in the summary row to red (2). Otherwise set to white (0). Append this "summary" row to the list of modified rows. Return the list of rows as a new grid.
"""

import numpy as np

def transform(input_grid):
    output_rows = []
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row and perform replacements.
    for row in input_grid:
        if 1 in row:
            new_row = [2 if cell == 1 else cell for cell in row]
            output_rows.append(new_row)
        else:
            output_rows.append(list(row))


    # Create the summary row.
    summary_row = [0] * cols
    for col_index in range(cols):
        for row_index in range(rows):
            if input_grid[row_index, col_index] == 1:
                summary_row[col_index] = 2
                break  # Once a blue is found in the column, move to the next

    # Append the summary row.
    output_rows.append(summary_row)

    return output_rows
```