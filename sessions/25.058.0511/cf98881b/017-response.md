# cf98881b • 017 • refine_coder

---
```python
"""
1.  **Identify the Rightmost Object:** Find the rightmost column in the input grid that contains any non-zero (non-white) pixels. This column defines the "rightmost object."

2.  **Extract Column Data:** Extract all pixels from the identified column.

3. If the input contains rows of all the same color, include those.

4.  **Construct Output Grid:** Create a new grid. The width of this new grid will be 4. The height is the same as the input.

5.  **Populate output.** Copy the pixel data from the column identified in the input into column 1 of the output. If all pixels extracted in step 2 are white, make the entire output grid white.
If we found any matching rows in step 3, copy them to the output.

6. fill any remaining output columns with 0
"""

import numpy as np

def _find_rightmost_nonzero_column(grid):
    """Finds the index of the rightmost column with non-zero values."""
    height, width = grid.shape
    for j in range(width - 1, -1, -1):
        if np.any(grid[:, j] != 0):
            return j
    return -1

def _extract_column(grid, col_index):
    """Extracts a column from the grid as a list."""
    return grid[:, col_index].tolist()

def _find_matching_rows(grid):
    """find rows that are all the same color"""
    matching_rows = []
    height, width = grid.shape
    for r in range(height):
        if np.all(grid[r] == grid[r,0]):
            matching_rows.append(grid[r].tolist())

    return matching_rows


def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_width = 4
    output_height = input_height
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 1. Identify the Rightmost Object
    rightmost_col_index = _find_rightmost_nonzero_column(input_grid)

    # 2. Extract Column Data
    extracted_column = []
    if rightmost_col_index != -1:
        extracted_column = _extract_column(input_grid, rightmost_col_index)

        # 5. Populate Output (part 1)
        if not np.all(np.array(extracted_column) == 0):  # If not all white
             output_grid[:, 0] = extracted_column
        #else all output is white - initialized to 0

    # 3. find matching rows
    matching_rows = _find_matching_rows(input_grid)

    #copy them to output
    for row in matching_rows:
        output_row_index = input_grid.tolist().index(row)
        output_grid[output_row_index] = row[:output_width]  #copy only first n elements to match width

    return output_grid.tolist()
```
