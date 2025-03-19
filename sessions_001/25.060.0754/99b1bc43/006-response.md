# 99b1bc43 • 006 • refine_coder

---
```python
"""
Divide the input grid into non-overlapping 2x2 blocks. If a 2x2 block contains any yellow (4) pixel, 
consolidate the entire block into a single green (3) pixel in the output grid. Otherwise, if there are no
yellow cells, keep that cell unchanged, but reduce dimensions based on 2x2 blocks.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid dimensions.  The output grid will have dimensions based on the 2x2 block counts
    input_grid = np.array(input_grid)
    block_height = 2
    block_width = 2
    output_height = (input_grid.shape[0] + block_height - 1) // block_height  #correct rounding up
    output_width = (input_grid.shape[1] + block_width - 1) // block_width #correct rounding up
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid in 2x2 blocks
    for i in range(0, input_grid.shape[0], block_height):
        for j in range(0, input_grid.shape[1], block_width):
            # Extract the 2x2 block
            block = input_grid[i:min(i + block_height, input_grid.shape[0]), j:min(j + block_width, input_grid.shape[1])]

            # Check for the presence of yellow (4) in the block
            if 4 in block:
                # Consolidate to green (3)
                output_grid[i // block_height, j // block_width] = 3
            else:
                # Keep original cell color, accounting for blocks that are not 2x2
                output_grid[i//block_height, j //block_width] = block[0,0]

    return output_grid.tolist()
```
