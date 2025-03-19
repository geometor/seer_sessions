# 10fcaaa3 • 018 • refine_coder

---
```python
"""
Double the dimensions of the input grid. Fill the output grid with an azure checkerboard pattern. 
For each yellow pixel in the input, place a yellow pixel in the output grid at [2*row+1, 2*col+1] 
and another at [2*row+1, 2*(input_width-1-col)+1].
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with doubled dimensions
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Fill with Azure checkerboard background
    for row in range(output_height):
        for col in range(output_width):
            if (row + col) % 2 == 0:
                output_grid[row, col] = 8

    # Replicate and Mirror Yellow pixels
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 4:  # If yellow pixel found
                # Original position replication
                output_grid[2 * row + 1, 2 * col + 1] = 4
                # Mirrored position replication
                output_grid[2 * row + 1, 2 * (input_width - 1 - col) + 1] = 4

    return output_grid
```

