# 77fdfe62 • 002 • example_1 • investigate_coder

---
```python
"""
Extracts corner colors from the input grid and its 2x2 subgrids, then constructs a smaller output grid. 
Colors from the corners of the subgrids are placed into the output grid. White corners are replaced with white(0) in the output.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_height = height // 2
    output_width = width // 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through 2x2 subgrids
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            # Extract subgrid
            subgrid = input_grid[i:i+2, j:j+2]
            
            #fill output grid
            output_row = i // 2
            output_col = j // 2
            
            if subgrid[0, 0] != 0 and subgrid[0, 0] != 1:
              output_grid[output_row, output_col] = subgrid[0, 0]
            if subgrid[0, 1] != 0 and subgrid[0, 1] != 1:
              output_grid[output_row, output_col+1] = subgrid[0, 1]
            if subgrid[1, 0] != 0 and subgrid[1, 0] != 1:
              output_grid[output_row+1, output_col] = subgrid[1, 0]
            if subgrid[1, 1] != 0 and subgrid[1, 1] != 1:
              output_grid[output_row+1, output_col+1] = subgrid[1, 1]

    return output_grid.tolist()
```
