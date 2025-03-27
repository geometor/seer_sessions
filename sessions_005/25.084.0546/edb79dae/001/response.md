```python
"""
The input grid is processed in 3x3 blocks, which are compressed into single pixels in the output grid. 
The output grid has a gray (5) background.
Colors in input 3x3 blocks are transformed:
    - 3s become 4s
    - 6s become 7s
    - 8s become 2s
    - 2s become 8s
    - 1s become 8s
    - 4s become 2s
The top and bottom rows, and leftmost and rightmost columns, of the output grid are filled with 5s.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Calculate output dimensions based on 3x3 block processing,
    # excluding the first row and col, and last row and col.
    output_height = (input_height - 2)
    output_width = (input_width - 2)

    # Initialize output_grid with 5s (gray background)
    output_grid = np.full((output_height, output_width), 5, dtype=int)

    # Iterate through input_grid in 3x3 blocks
    for i in range(0, input_height - 2):
      for j in range(0, input_width - 2):
        block = input_grid[i:i+1,j:j+1]
        #get the value, default to 5 to handle edges
        value = input_grid[i,j]
        # Apply color transformations, else preserve original color if not in the transformation
        if value == 3:
            value = 4
        elif value == 6:
            value = 7
        elif value == 8:
            value = 2
        elif value == 2:
            value = 8
        elif value == 1:
            value=8
        elif value == 4:
              value=2

        output_grid[i,j] = value

    return output_grid
```