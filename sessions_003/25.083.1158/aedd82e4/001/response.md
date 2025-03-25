```python
"""
Replace the bottom-right red pixel (value 2) of any 2x2 block of red pixels with a blue pixel (value 1).
"""

import numpy as np

def find_2x2_red_blocks(grid):
    """
    Finds all 2x2 blocks of red pixels (value 2) in the grid.
    Returns a list of (row, col) coordinates of the bottom-right pixel of each block.
    """
    blocks = []
    rows, cols = len(grid), len(grid[0])
    for row in range(rows - 1):
        for col in range(cols - 1):
            if (grid[row][col] == 2 and grid[row+1][col] == 2 and
                grid[row][col+1] == 2 and grid[row+1][col+1] == 2):
                blocks.append((row + 1, col + 1))
    return blocks

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Replace the bottom-right red pixel (value 2) of any 2x2 block of red
    pixels with a blue pixel (value 1).
    """
    output_grid = np.copy(input_grid)  # Create a copy to modify
    rows, cols = len(input_grid), len(input_grid[0])

    # Find all bottom-right corners of 2x2 red blocks
    bottom_right_corners = find_2x2_red_blocks(input_grid)
    
    # change identified pixels to blue
    for row, col in bottom_right_corners:
        output_grid[row][col] = 1
    
    return output_grid
```