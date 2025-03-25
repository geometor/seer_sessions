```python
"""
1.  **Find Grey Row:** Locate the row containing only grey (5) pixels and copy it to the output grid at the same index.
2.  **Iterate Rows:** Process each row in the input, except the Grey Row, as follows to create output row.
3.  **Non-Grey Row Processing:** For each non-grey input row:
    *   Create a new output row of the same length as the input row, initially all zeros.
    *   Iterate through each pixel in the *input* row.
        *  if a pixel is *followed* by a blue (1) or red (2) pixel in the *input* row.
            *   Copy the current pixel's value to *two* adjacent cells at the current index in the new output row.
            *   Increment a modified flag.
        *  Otherwise, *if* a pixel is *not* followed by a blue or red and the modified flag has not been set:
            *   If the pixel to the right is 1 or 2, then save current pixel value to output row, otherwise write zero
        *  Otherwise, if the modified flag is set and pixel is NOT blue or red:
            * copy current pixel value to current index in the new output row.

4.  **Output:** Return the modified grid.
"""

import numpy as np

def find_grey_row(grid):
    """Finds the index of the row containing only grey pixels."""
    rows, cols = grid.shape
    for i in range(rows):
        if np.all(grid[i] == 5):
            return i
    return -1  # Should not happen in valid tasks, but good practice

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    grey_row_index = find_grey_row(input_grid)

    # Copy grey row if it exists
    if grey_row_index != -1:
        output_grid[grey_row_index] = input_grid[grey_row_index]

    # Process each row
    for i in range(rows):
        if i == grey_row_index:
            continue  # Skip grey row, already copied

        modified = False
        new_row = np.zeros(cols, dtype=int)

        for j in range(cols):
            if j + 1 < cols and (input_grid[i, j+1] == 1 or input_grid[i, j+1] == 2):
                # Duplicate pixel
                new_row[j] = input_grid[i, j]
                modified = True
            elif not modified:
                if j + 1 < cols and (input_grid[i,j+1] == 1 or input_grid[i,j+1] == 2):
                    new_row[j] = input_grid[i,j]

            elif modified:
                new_row[j] = input_grid[i,j]

        output_grid[i] = new_row

    return output_grid.tolist()
```