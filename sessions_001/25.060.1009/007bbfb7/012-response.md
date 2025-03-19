# 007bbfb7 • 012 • example_2 • investigate_coder

---
```python
"""
Expand a 3x3 input grid to a 9x9 output grid, replicating and strategically placing yellow (4) pixels based on their positions in the input grid, while leaving the rest of the output grid as white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 9x9 array filled with white (0)
    output_grid = np.zeros((9, 9), dtype=int)

    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Iterate through the input grid to find and replicate yellow pixels
    for i in range(input_height):
        for j in range(input_width):
            if input_grid[i, j] == 4:
                # Copy yellow cells from row 0 to output row 0 and row 2*input_width
                if i == 0:
                    output_grid[i, j] = 4
                    output_grid[i , j + 2* input_width] = 4

                # Copy yellow cell from row 2 to output row 2 and to row 6 and 8
                if i == 2 :
                    output_grid[i,j]=4
                    output_grid[i + input_width * (i-1) , input_width + j ] = 4 #cell from input[2,1] copied to [6,5]
                    output_grid[i + input_width * i,  j + input_width ]=4 # and to [8,4]

    return output_grid
```
