# f2829549 • 028 • example_5 • investigate_coder

---
```python
"""
Transforms an input grid by reducing its dimensions and changing blue (1) pixels to green (3) and all other colors to white (0). The output grid has the same number of rows as the input, but only includes columns from the input that contained a blue pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    rows = input_grid.shape[0]

    # Find columns containing the value 1 (blue).
    blue_columns = np.where(np.any(input_grid == 1, axis=0))[0]
    
    # create the intermediate grid using only columns with a blue pixel
    intermediate_array = input_grid[:, blue_columns]

    # Initialize output grid with dimensions: same rows as input, same columns as blue_columns
    output_grid = np.zeros((rows, intermediate_array.shape[1]), dtype=int)


    # Iterate through the intermediate array and map colors.
    for i in range(rows):
        for j in range(intermediate_array.shape[1]):
            if intermediate_array[i, j] == 1:
                output_grid[i, j] = 3
            else:
                output_grid[i, j] = 0

    return output_grid
```
