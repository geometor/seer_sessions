# 93b581b8 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves identifying a 2x2 central block in the input grid and mirroring/reflecting it to the four corner 2x2 blocks of the output grid.
"""

import numpy as np

def get_central_block(grid):
    """Extracts the 2x2 central block from the input grid."""
    rows, cols = grid.shape
    center_row = rows // 2
    center_col = cols // 2
    return grid[center_row-1:center_row+1, center_col-1:center_col+1]

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Get the central 2x2 block
    central_block = get_central_block(input_grid)

    # Get the dimensions of the input grid
    rows, cols = input_grid.shape
    center_row = rows // 2
    center_col = cols // 2
    
    # set the center 2x2 block to be same
    output_grid[center_row-1:center_row+1, center_col-1:center_col+1] = central_block
    
    # Mirror/reflect the central block to the four corners
    output_grid[0:2, 0:2] = np.array([[central_block[1,1], central_block[1,0]], [central_block[0,1], central_block[0,0]]]) # Top-left
    output_grid[0:2, cols-2:cols] = np.array([[central_block[1,1], central_block[1,0]], [central_block[0,1], central_block[0,0]]]) #top right
    output_grid[rows-2:rows, 0:2] = np.array([[central_block[1,1], central_block[1,0]], [central_block[0,1], central_block[0,0]]])  # Bottom-left
    output_grid[rows-2:rows, cols-2:cols] = np.array([[central_block[1,1], central_block[1,0]], [central_block[0,1], central_block[0,0]]]) # Bottom-right

    return output_grid
```
