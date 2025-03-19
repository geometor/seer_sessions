# eb281b96 • 016 • refine_coder

---
```python
"""
The input grid is transformed into an output grid with the same width but a fixed height of 13. 
Each row of the input grid is expanded vertically based on the row index and, for the first row, the color of the pixel.
- First row (index 0): White (0) pixels are replicated three times, red (2) pixels are replicated twice.
- Second and third rows (index 1 and 2): All pixels are replicated twice.
- Fourth row (index 3): All pixels are replicated three times.
The horizontal arrangement of pixels remains unchanged.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_height = 13
    output_grid = np.zeros((output_height, width), dtype=int)

    # Iterate through the input grid rows.
    output_row_index = 0
    for i in range(height):
        # Apply row-specific expansion rules.
        if i == 0:
            for j in range(width):
              if input_grid[i,j] == 0: # white
                output_grid[output_row_index,j] = input_grid[i,j]
                output_grid[output_row_index+1,j] = input_grid[i,j]
                output_grid[output_row_index+2,j] = input_grid[i,j]
              elif input_grid[i,j] == 2:
                output_grid[output_row_index,j] = input_grid[i,j]
                output_grid[output_row_index+1,j] = input_grid[i,j]
            output_row_index += 3

        elif i == 1 or i == 2:
            for j in range(width):
                output_grid[output_row_index, j] = input_grid[i, j]
                output_grid[output_row_index + 1, j] = input_grid[i, j]
            output_row_index += 2
        elif i == 3:
            for j in range(width):
                output_grid[output_row_index, j] = input_grid[i, j]
                output_grid[output_row_index + 1, j] = input_grid[i, j]
                output_grid[output_row_index + 2, j] = input_grid[i, j]
            output_row_index += 3


    return output_grid.tolist()
```
