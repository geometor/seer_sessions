# eb281b96 • 018 • refine_coder

---
```python
"""
The input grid is transformed into an output grid. Each row of the input grid is replicated vertically in the output grid. The number of times a row is replicated (the expansion factor) depends on its index within the input grid:

*   Row index 0: Replicated 3 times.
*   Row index 1: Replicated 2 times.
*   Row index 2: Replicated 2 times.
*   Row Index 3: Replicated 3 times.
*   If a row index does not exist, it is not used.

The horizontal arrangement (order of pixels within each row) remains unchanged. The output grid's height is the sum of all the replicated rows.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, width = input_grid.shape

    # Determine the output height based on the expansion factors.
    output_height = 0
    for i in range(input_height):
        if i == 0 or i == 3:
            output_height += 3
        elif i == 1 or i == 2:
            output_height += 2

    # Initialize the output grid.
    output_grid = np.zeros((output_height, width), dtype=int)

    # Iterate through input rows and replicate them in the output grid.
    output_row_index = 0
    for input_row_index in range(input_height):
        if input_row_index == 0 or input_row_index == 3:
            expansion_factor = 3
        elif input_row_index == 1 or input_row_index == 2:
            expansion_factor = 2
        else:
            continue # skip if row index is greater than 3.

        for _ in range(expansion_factor):
            output_grid[output_row_index] = input_grid[input_row_index]
            output_row_index += 1

    return output_grid.tolist()
```
