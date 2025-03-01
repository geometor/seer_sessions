# 46442a0e • 006 • refine_coder

---
```python
"""
The transformation rule replicates the input grid to produce an output grid that is twice the size in both dimensions. The input grid acts as a tile that is repeated four times (2x2) to create the output grid. The pattern of colors and objects within the input grid is maintained during this replication.
"""

import numpy as np

def transform(input_grid):
    # Determine Input Dimensions: Get the height and width of the input grid.
    input_height, input_width = input_grid.shape

    # Calculate Output Dimensions: Multiply both the height and width by two to get the output grid's dimensions.
    output_height, output_width = input_height * 2, input_width * 2

    # Create Output Grid: Initialize an empty output grid with the calculated dimensions.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate Input: Iterate through each cell of the *output* grid.
    for i in range(output_height):
        for j in range(output_width):
            # For each cell, calculate its corresponding position in the *input* grid
            # using the modulo operator (%) with the input grid's dimensions.
            input_row = i % input_height
            input_col = j % input_width

            # Copy the value from the corresponding input cell to the current output cell.
            output_grid[i, j] = input_grid[input_row, input_col]

    return output_grid
```

