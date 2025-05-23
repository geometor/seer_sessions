# 9ecd008a • 010 • example_2 • investigate_coder

---
```python
"""
The transformation extracts a 3x3 grid representing specific regions of the larger input grid.
It appears to select a prominent color from the corners and center of the input to build
the output.
"""

import numpy as np

def get_corner_and_center_colors(input_grid):
    """
    Extracts colors from the four corners and the center of the input grid.
    Divides the grid to nine blocks, and selects a color in each block.
    """
    height, width = input_grid.shape
    block_height = height // 3
    block_width = width // 3

    colors = {}

    # Top-left
    colors[(0, 0)] = input_grid[block_height // 2, block_width // 2]
    # Top-center
    colors[(0, 1)] = input_grid[block_height // 2, block_width + block_width // 2]

    # Top-right
    colors[(0, 2)] = input_grid[block_height // 2, 2*block_width + block_width//2]

    # Middle-left
    colors[(1, 0)] = input_grid[block_height + block_height // 2, block_width // 2]

    # Center
    colors[(1, 1)] = input_grid[height // 2, width // 2]

    #Middle-right
    colors[(1, 2)] = input_grid[block_height + block_height//2, 2*block_width + block_width//2]
    
    # Bottom-left
    colors[(2, 0)] = input_grid[2*block_height + block_height//2, block_width // 2]

    # Bottom-center
    colors[(2, 1)] = input_grid[2*block_height + block_height//2, block_width + block_width // 2]

    # Bottom-right
    colors[(2, 2)] = input_grid[2*block_height + block_height//2, 2*block_width + block_width//2]

    return colors

def transform(input_grid):
    # Get the corner and center colors
    colors = get_corner_and_center_colors(input_grid)

    # Initialize the output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the output grid
    for (row, col), color in colors.items():
        output_grid[row, col] = color

    return output_grid
```
