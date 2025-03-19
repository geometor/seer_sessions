# 10fcaaa3 • 006 • refine_coder

---
```python
"""
Double the input grid's dimensions. Replicate both gray and green pixels into 2x2 blocks 
at doubled coordinates. Create a checkered pattern of azure and white on even rows, 
skipping positions occupied by the replicated gray or green blocks.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate Gray and Green pixels into 2x2 blocks
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 5 or input_grid[row, col] == 3:
                output_grid[row*2, col*2] = input_grid[row, col]
                output_grid[row*2+1, col*2] = input_grid[row, col]
                output_grid[row*2, col*2+1] = input_grid[row, col]
                output_grid[row*2+1, col*2+1] = input_grid[row, col]

    # Fill Azure and White pattern on even rows
    for row in range(0, output_height, 2):  # Iterate through even rows only
        for col in range(output_width):
            if output_grid[row, col] == 0: # Check if the cell is not occupied
                if col % 2 == 0:
                    output_grid[row, col] = 8  # Even column: azure
                else:
                    output_grid[row, col] = 0  # Odd column: white

    return output_grid
```
