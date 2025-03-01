# 31aa019c • 016 • refine_coder

---
```python
"""
Create a 10x10 output grid filled with white (0). Locate a 3x3 region in the output grid adjacent to the top and right borders. Fill this 3x3 region with red (2). Change the color of the center pixel of the 3x3 region to magenta (6).
"""

import numpy as np

def transform(input_grid):
    # Initialize a 10x10 output grid filled with white (0)
    output_grid = np.zeros((10, 10), dtype=int)

    # Define the dimensions of the output block
    block_size = 3

    # Determine the starting row and column for the block (top-right corner)
    start_row = 0
    start_col = output_grid.shape[1] - block_size

    # Fill the 3x3 block with red (2)
    output_grid[start_row:start_row + block_size, start_col:start_col + block_size] = 2

    # Change the center pixel of the block to magenta (6)
    center_row = start_row + block_size // 2
    center_col = start_col + block_size // 2
    output_grid[center_row, center_col] = 6
    
    return output_grid
```

