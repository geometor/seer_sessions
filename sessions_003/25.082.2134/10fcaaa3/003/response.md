```python
"""
The transformation rule involves expanding each pixel from the input grid into a 2x2 block in the output grid. The top-left pixel of each 2x2 block is azure (8). If the original input pixel is non-zero, the remaining three pixels of the 2x2 block match the original pixel's color. If the original input pixel is zero, the remaining three pixels of the 2x2 block are also zero.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Double Dimensions: Calculate output grid dimensions.
    output_height = input_height * 2
    output_width = input_width * 2

    # initialize output_grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid.
    for i in range(input_height):
        for j in range(input_width):
            # 2x2 Block Transformation: Determine the corresponding 2x2 block in the output.
            row_start = i * 2
            col_start = j * 2

            # Azure Pixel Placement: Set the top-left pixel of the 2x2 block to azure.
            output_grid[row_start, col_start] = 8

            # Non-Zero and Zero Pixel Replication: Fill the remaining pixels of the 2x2 block.
            if input_grid[i, j] != 0:
                output_grid[row_start + 1, col_start] = input_grid[i, j]  # Bottom-left
                output_grid[row_start, col_start + 1] = input_grid[i, j]  # Top-right
                output_grid[row_start + 1, col_start + 1] = input_grid[i, j]  # Bottom-right
            else:
                output_grid[row_start + 1, col_start] = 0  # Bottom-left
                output_grid[row_start, col_start + 1] = 0      # Top-right
                output_grid[row_start + 1, col_start + 1] = 0  # Bottom-right

    return output_grid
```
