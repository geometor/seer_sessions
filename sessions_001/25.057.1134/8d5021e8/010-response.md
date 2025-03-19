# 8d5021e8 • 010 • refine_coder

---
```python
"""
The transformation rule involves identifying the rows containing white pixels in the input grid and creating a corresponding output grid. For each row with a white pixel in the input, three rows are created in the output. The first of these three rows has white pixels in the first and last columns.  The next two rows will be red and the last row created will be white.
"""

import numpy as np

def transform(input_grid):
    # Find rows with white pixels
    white_rows = np.any(input_grid == 0, axis=1)
    input_white_row_indices = np.where(white_rows)[0]

    # Calculate output height: 3 rows for each input row with white + one row
    output_height = len(input_white_row_indices) * 3 + (1 if len(input_white_row_indices) else 0)
    output_width = 4

    # Initialize output_grid with red (2)
    output_grid = np.full((output_height, output_width), 2)

    # Create output rows based on input white rows
    output_row_index = 0
    for i in input_white_row_indices:
        # White row
        output_grid[output_row_index, 0] = 0
        output_grid[output_row_index, 3] = 0
        output_row_index += 1
        #add a two more rows, that are all red and they will be overwritten later, if required
        output_row_index += 1
        output_row_index += 1
    
    #add a white at bottom if any white rows found
    if len(input_white_row_indices) > 0:
        output_grid[output_row_index, 0] = 0
        output_grid[output_row_index, 3] = 0
    

    return output_grid
```
