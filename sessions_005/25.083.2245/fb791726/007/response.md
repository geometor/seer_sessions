```python
"""
1. Double the Width: The output grid's width is twice the input grid's width.
2. Iterate Through Rows: Examine each row of the input grid.
3. Check for Non-zero: Copy and translate any row that contains one or more non-zero entries, preserving relative position of elements within that row.
4. Insert Green Rows: For each row in the input grid which contains a non-zero value, insert a row of green pixels (all 3s) with a width equal to the *output* grid's width into the *output* grid. These green rows are inserted *into* the set of translated input rows.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_width = 2 * input_width
    output_grid_list = []

    # Iterate through rows of the input grid
    for row in input_grid:
        # Check for non-zero elements in the current row
        if np.any(row != 0):
            # Create a new row for the output, initialized with zeros
            new_row = np.zeros(output_width, dtype=int)
            # Copy non-zero elements to their original positions
            for i in range(input_width):
                if row[i] != 0:
                    new_row[i] = row[i]
            # Add the new row to the output list
            output_grid_list.append(new_row)

            # Create and add a green row
            green_row = np.full(output_width, 3, dtype=int)
            output_grid_list.append(green_row)
        else: # all elements are zero
              new_row = np.zeros(output_width, dtype=int)
              output_grid_list.append(new_row)


    # Convert the list of rows to a NumPy array
    output_grid = np.array(output_grid_list)

    return output_grid
```
