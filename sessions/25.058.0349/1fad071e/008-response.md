# 1fad071e • 008 • example_2 • investigate_coder

---
```python
"""
Iterates through each column of the input grid. For each column, it counts the number of blue (1) pixels.
If the count of blue pixels is greater than zero, it outputs a blue (1) pixel. Otherwise, it outputs a white (0) pixel.
The output is a 1D array (row) representing the presence of blue in each column.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into a 1D array based on the presence of blue pixels in each column.
    """
    input_grid = np.array(input_grid)
    num_cols = input_grid.shape[1]
    output_grid = []

    # Iterate through each column
    for j in range(num_cols):
        # Count the number of blue (1) pixels in the current column
        blue_count = np.count_nonzero(input_grid[:, j] == 1)

        # If blue count is greater than 0, append 1 to output; otherwise, append 0
        if blue_count > 0:
            output_grid.append(1)
        else:
            output_grid.append(0)

    return output_grid
```
