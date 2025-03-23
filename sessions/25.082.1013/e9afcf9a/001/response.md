```python
"""
The input consists of 2 rows with the same number of columns. Each row of input consists of a single color.
Construct the output by alternating columns from the input.
The first output row takes the first column of the first input row, then the first column of the second input row. Repeating this process, creates the first output row.
The second output row starts with the first column of the second input row, then takes the first column of the first input row. Repeating this process, creates the second output row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # change output pixels 
    for i in range(cols):
        # first output row gets input row 1, then input row 2
        output_grid[0, i] = input_grid[0 if i % 2 == 0 else 1, i if i % 2 == 0 else (i-1 if i> 0 else i)]
        # first output row gets input row 2, then input row 1
        output_grid[1, i] = input_grid[1 if i % 2 == 0 else 0, i if i % 2 == 0 else (i-1 if i> 0 else i)]

    return output_grid
```
