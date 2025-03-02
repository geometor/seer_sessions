# f2829549 • 030 • refine_coder

---
```python
"""
Transforms an input grid by selecting columns containing blue (1) pixels. If no blue pixels are found, creates an output grid with the same number of rows but zero columns.  Transforms blue pixels to green (3) and all other colors to white (0) within the selected columns.
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

    # Conditional column selection and output grid initialization.
    if blue_columns.size > 0:
        # create the intermediate grid using only columns with a blue pixel
        intermediate_array = input_grid[:, blue_columns]
        output_grid = np.zeros((rows, intermediate_array.shape[1]), dtype=int)

        # Iterate through the intermediate array and map colors.
        for i in range(rows):
            for j in range(intermediate_array.shape[1]):
                if intermediate_array[i, j] == 1:
                    output_grid[i, j] = 3
                else:
                    output_grid[i, j] = 0
    else:
        # Create an output grid with zero columns.
        output_grid = np.zeros((rows, 0), dtype=int)
    return output_grid
```

