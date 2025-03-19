# ff28f65a • 002 • example_8 • investigate_coder

---
```python
"""
Maps the presence of 2x2 red blocks in the input grid to blue pixels in a 3x3 output grid.
"""

import numpy as np

def find_2x2_blocks(grid, value):
    # Find all 2x2 blocks of the specified value in the grid.
    rows, cols = grid.shape
    blocks = []
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i:i+2, j:j+2] == value).all():
                blocks.append((i, j))
    return blocks

def transform(input_grid):
    # Initialize a 3x3 output grid with all white pixels (0).
    output_grid = np.zeros((3, 3), dtype=int)
    input_grid = np.array(input_grid)
    
    rows, cols = input_grid.shape
    row_block_size = rows // 3
    col_block_size = cols // 3
    
    # Iterate through each of the nine regions in the output grid.
    for i in range(3):
        for j in range(3):
            # Define the corresponding region in the input grid.
            row_start = i * row_block_size
            row_end = (i + 1) * row_block_size
            col_start = j * col_block_size
            col_end = (j + 1) * col_block_size
            
            # Extract the region from the input grid.  Handle edge cases.
            region = input_grid[row_start:row_end, col_start:col_end]
            
            
            # Check for 2x2 red blocks (value 2) within this region.
            blocks = find_2x2_blocks(region, 2)
            
            # If any 2x2 red blocks are found, set the output pixel to blue (1).
            if blocks:
                output_grid[i, j] = 1

    return output_grid
```
