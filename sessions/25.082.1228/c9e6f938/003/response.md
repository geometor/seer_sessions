```python
"""
Expands the input grid horizontally by a factor of 2. 
Each original column is copied to the output, and 
a column is inserted after each copied column. 
The inserted column mirrors the values from the column 
immediately to its right.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with double the width, filled with 0s.
    input_grid = np.array(input_grid)
    output_width = input_grid.shape[1] * 2
    output_height = input_grid.shape[0]
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through input columns and copy them to the output grid.
    for i in range(input_grid.shape[1]):
        output_grid[:, 2 * i] = input_grid[:, i]

    # Iterate through the inserted columns and copy from the right neighbor
    for i in range(input_grid.shape[1]):
        output_grid[:, 2 * i + 1] = input_grid[:,i]


    return output_grid.tolist()
```