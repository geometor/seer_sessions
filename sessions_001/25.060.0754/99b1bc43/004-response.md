# 99b1bc43 • 004 • example_1 • investigate_coder

---
```python
"""
Divide the input grid into non-overlapping 2x2 blocks. If a 2x2 block contains any yellow (4) pixel, 
consolidate the entire block into a single green (3) pixel in the output grid. Otherwise, if there are no
yellow cells, consolidate the block to white pixels (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid dimensions.  The output grid will have dimensions based on the 2x2 block counts
    input_grid = np.array(input_grid)
    block_height = 2
    block_width = 2
    output_height = input_grid.shape[0] // block_height
    output_width = input_grid.shape[1] // block_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid in 2x2 blocks
    for i in range(0, input_grid.shape[0], block_height):
        for j in range(0, input_grid.shape[1], block_width):
            # Extract the 2x2 block
            block = input_grid[i:i + block_height, j:j + block_width]

            # Check for the presence of yellow (4) in the block
            if 4 in block:
                # Consolidate to green (3)
                output_grid[i // block_height, j // block_width] = 3
            else:
                # Consolidate to white (0)
                output_grid[i // block_height, j // block_width] = 0 # already initialized to 0

    return output_grid.tolist()
```
