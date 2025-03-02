# ce4f8723 • 014 • refine_coder

---
```python
"""
The transformation identifies non-zero colored regions in the input and creates a representation of them in the output.  The output dimensions and content are derived from the position and color of objects in the input, not necessarily the largest. It appears the top-most and then left-most object are used for the transformation.

1. Find the top-most, then left-most non-zero colored contiguous region (object) in the input grid.
2. The output grid's height is equal to the number of rows from beginning of the found object up to the last row containing any colored pixel of the found color.
3. The output grid's width is equal to the horizontal length (number of columns) the object takes in the first row where the object appears.
4. The output grid is populated by replicating the color and width of the object as it appears in the first row where it is found, and extended down to be the height.
"""

import numpy as np

def find_top_left_object(grid):
    """Finds the top-left non-zero colored object."""
    rows, cols = grid.shape
    object_color = 0
    start_row = -1
    start_col = -1
    end_row = -1 # inclusive

    # find color and top-left start
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                object_color = grid[r, c]
                start_row = r
                start_col = c
                break
        if start_row != -1:
            break
    
    if start_row == -1:
        return 0, -1, -1, -1 # no object

    # determine object extent vertically
    for r in range(start_row, rows):
        if not np.any(grid[r,:] == object_color):
            break
        else:
            end_row = r

    # determine object horizontal extent in the first row
    first_row_width = 0
    for c in range(start_col, cols):
        if grid[start_row,c] == object_color:
            first_row_width+=1
        else:
            break
    return object_color, start_row, start_col, first_row_width, end_row

def transform(input_grid):
    input_grid = np.array(input_grid)
    object_color, start_row, start_col, first_row_width, end_row = find_top_left_object(input_grid)

    if start_row == -1: # handle no object case
        return []

    output_height = end_row - start_row + 1
    output_width = first_row_width

    # Create output grid
    output_grid = np.full((output_height, output_width), object_color, dtype=int)

    return output_grid.tolist()
```
