```python
"""
The output grid takes on the number of rows from the input, and the
number of columns is 4. We find column 5 in the input (color 4), and transform it
to an output where every column to it's left is filled with the color red
(value 2), with all other values being 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows = len(input_grid)
    cols = 4
    output_grid = np.zeros((rows, cols), dtype=int)

    # find the anchor column (where color 4 is)
    anchor_col = 4  # It's always the 5th column (index 4)

    # populate output grid with red (2) up to the anchor column
    for r in range(rows):
        for c in range(cols):
            if c < anchor_col :
                output_grid[r][c] = 2

    return output_grid
```