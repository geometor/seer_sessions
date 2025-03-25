```python
"""
1.  **Identify Top Row Pattern:** Examine the first row (top row) of the input grid. Note the colors and their order, including azure (8) pixels. This is the "top row pattern".

2.  **Row Matching:** Iterate through each row of the input grid, starting from the second row (index 1).

3.  **Conditional Row Transformation:**
    *   Compare the *entire* current row with the *entire* top row.
    *   If the rows are *identical* (including azure pixels), copy the top row to the output grid at the current row's position.  Then, propagate *all* non-azure colors in the copied row downwards.
        - **Propagation:**  For each non-azure pixel in the copied row, copy its value downwards through all subsequent rows in the output grid, within the same column.  Later transformations *overwrite* earlier ones.

    *   If the rows are *not identical*, attempt to transform based on column changes, but only propagate colors *until* a matched row:
        - **Column Change Detection:** Compare *each* pixel in the current row to the corresponding pixel in the row *above* it.
        - **Propagation of Changed Pixels:** If a pixel has changed color (and is not azure), propagate the *new* color downwards in the output grid, within that column. Stop the propagation if you encounter a row that matches the top row.

4.  **Handling Azures:** Azure pixels do *not* propagate downwards on their own in unmatched rows.  They are only copied when an entire row matches the top row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify Top Row Pattern (including azures)
    top_row = input_grid[0]

    # 2. & 3. Row Matching and Conditional Transformation
    for y in range(height):
        # Check for entire row match
        if np.array_equal(input_grid[y], top_row):
            # Copy top row to output
            output_grid[y] = np.copy(top_row)

            # Propagate non-azure colors downwards
            for x in range(width):
                if top_row[x] != 8:
                    for row_below in range(y + 1, height):
                        output_grid[row_below, x] = top_row[x]
        else:
            # Handle unmatched rows: propagate changes downwards
            if y > 0:  # Start from the second row
                prev_row = input_grid[y - 1]
                curr_row = input_grid[y]
                for x in range(width):
                    # Check for changed pixel (and not azure)
                    if curr_row[x] != prev_row[x] and curr_row[x] != 8:
                        # Propagate new color downwards
                        for row_below in range(y + 1, height):
                            if np.array_equal(input_grid[row_below], top_row):
                                break  # Stop propagation at matched row
                            output_grid[row_below, x] = curr_row[x]

    return output_grid.tolist()
```