# 539a4f51 • 004 • refine_coder

---
```python
"""
1.  **Replicate:** The input grid is replicated four times in a 2x2 grid pattern within the output grid. This creates four quadrants in the output grid, each identical to the input grid. The top-left corners of these quadrants are at (0,0), (0, *w*), (*h*, 0), and (*h*, *w*), where *h* is the height of the input and *w* is the width.

2.  **Fill:** The remaining cells of the output grid (those not part of the replicated pattern) are filled based on extending the edges of the input into the output:
  *  **Row Extension:** If the output grid cell's row index is greater than or equal to the input height *h*, then the values of that row index *modulo h* in the input are extended into the ouput.
  * **Column Extension:** If the output grid cell's column index is greater to or equal than the input width *w*, then the values of that column index *modulo w* in the input are extended into the output.
"""

import numpy as np

def transform(input_grid):
    input_h, input_w = input_grid.shape
    output_h, output_w = input_h * 2, input_w * 2
    output_grid = np.zeros((output_h, output_w), dtype=int)

    # Replicate the input grid 2x2
    for i in range(2):
        for j in range(2):
            output_grid[i*input_h:(i+1)*input_h, j*input_w:(j+1)*input_w] = input_grid

    # Fill based on row and column extensions
    for row in range(output_h):
        for col in range(output_w):
            if row < input_h and col < input_w:
                continue  # Skip cells within the replicated areas

            if row >= input_h:
                # Row Extension:
                input_row = row % input_h
                output_grid[row, col] = input_grid[input_row, col % input_w]

            if col >= input_w:
                # Column Extension
                input_col = col % input_w
                output_grid[row,col] = input_grid[row % input_h, input_col ]


    return output_grid
```
