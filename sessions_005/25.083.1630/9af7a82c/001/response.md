```python
"""
1.  **Identify Objects:** Consider each horizontal row of the input grid as distinct objects.
2.  **Reorder Columns:** Reverse the horizontal order of colors within each input row object, placing it in the same row number of the output.
3.  **Output Dimensions:** output is always 5 rows tall, input row count is less than or equal to 5.
4.  **Fill Remaining:** Fill the remaining cells of the output grid with 0 (white).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((5, cols), dtype=int)

    # iterate over input rows
    for i in range(rows):
        # reverse colors in row and assign to output row
        output_grid[i, :] = input_grid[i, ::-1]

    return output_grid
```