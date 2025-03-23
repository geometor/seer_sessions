"""
The transformation rule involves swapping the values of specific pixels across the anti-diagonal.

1. Swap the pixel at position (0, 0) with the pixel at position (2, 2).
2. Swap the pixel at position (0, 1) with the pixel at position (2, 1)
3. Swap the pixel at position (1, 0) with the pixel at position (1,2)
4. Swap the pixel at position (2,0) with the pixel at position (0, 2).
    If a coordinate has previously been swapped it should retain its new
    value.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.array(input_grid)

    # Anti-diagonal Swap: (0, 0) with (2, 2)
    output_grid[0, 0], output_grid[2, 2] = output_grid[2, 2], output_grid[0, 0]

    # Anti-diagonal Swap: (0, 1) with (2, 1)
    output_grid[0, 1], output_grid[2, 1] = output_grid[2, 1], output_grid[0, 1]
    
    # Anti-diagonal Swap: (1, 0) with (1, 2)
    output_grid[1, 0], output_grid[1, 2] = output_grid[1, 2], output_grid[1, 0]

    # Anti-diagonal Swap: (0, 2) with (2, 0)
    output_grid[0, 2], output_grid[2, 0] = output_grid[2, 0], output_grid[0, 2]
    

    return output_grid.tolist()