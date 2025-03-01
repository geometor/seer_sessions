# eb281b96 • 014 • example_2 • investigate_coder

---
```python
"""
The input grid consists of a 2x2 checkerboard pattern of white (0) and red (2) pixels.
The transformation expands the input grid vertically to create the output grid. 
The output grid maintains the same 2x2 checkerboard pattern and width as the input.
The height is expanded from 4 to 13, by rules based on the color.

"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_height = 13
    output_grid = np.zeros((output_height, width), dtype=int)

    # Iterate through the input grid in 2x2 blocks.
    for i in range(0, height):
        for j in range(0, width):
            # Map input rows to output rows.

            output_row_start = 0
            if i == 0:
              output_row_start = 0
            if i == 1 or i == 2:
              output_row_start = i * 3
            if i == 3:
              output_row_start = 9
            
            output_grid[output_row_start, j] = input_grid[i,j]

            if input_grid[i, j] == 0:
                if output_row_start+1 < output_height:
                  output_grid[output_row_start + 1, j] = input_grid[i,j]
                if output_row_start+2 < output_height:
                  output_grid[output_row_start + 2, j] = input_grid[i, j]
            if input_grid[i,j] == 2:
                if output_row_start+1 < output_height:
                  output_grid[output_row_start+1, j] = input_grid[i,j]

    return output_grid.tolist()
```
