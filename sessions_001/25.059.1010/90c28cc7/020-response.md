# 90c28cc7 • 020 • refine_coder

---
```python
"""
Divides the input grid into a 3x2 grid of equally-sized blocks and outputs a 3x2 grid where each cell represents the color of the corresponding block in the input grid.
"""

import numpy as np

def get_block_color(grid, row_start, row_end, col_start, col_end):
    """Extracts the color of a block from the grid."""
    # we are interested in a single solid color
    first_color = grid[row_start, col_start]
    return first_color

def transform(input_grid):
    """Transforms the input grid into a 3x2 grid of color values representing the blocks."""
    # Determine the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Calculate block dimensions.
    block_height = rows // 3
    block_width = cols // 2

    # Initialize an empty 3x2 output grid.
    output_grid = np.zeros((3, 2), dtype=int)

    # Iterate through the blocks and get color, then place it to output_grid
    
    # top-left block
    output_grid[0, 0] = get_block_color(input_grid, 0, block_height, 0, block_width)

    # top-right block
    output_grid[0, 1] = get_block_color(input_grid, 0, block_height, block_width, 2 * block_width)
    
    # middle-left block
    output_grid[1, 0] = get_block_color(input_grid, block_height, 2* block_height, 0, block_width)

    # middle-right block
    output_grid[1, 1] = get_block_color(input_grid, block_height, 2*block_height, block_width, 2 * block_width)

    # bottom-left block
    output_grid[2, 0] = get_block_color(input_grid, 2 * block_height, 3 * block_height, 0, block_width)

    # bottom-right block
    output_grid[2, 1] = get_block_color(input_grid, 2 * block_height, 3 * block_height, block_width, 2 * block_width)

    return output_grid
```
