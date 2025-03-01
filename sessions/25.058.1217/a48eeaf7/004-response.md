# a48eeaf7 • 004 • example_1 • investigate_coder

---
```python
"""
Moves gray pixels to form a larger square around a red block.
"""

import numpy as np

def find_objects(grid, color):
    # Find coordinates of pixels with the specified color.
    return np.argwhere(grid == color).tolist()

def find_block(grid, color, block_size=(2, 2)):
    # Find the top-left corner of a block of the specified color and size.
    rows, cols = grid.shape
    for i in range(rows - block_size[0] + 1):
        for j in range(cols - block_size[1] + 1):
            if np.all(grid[i:i+block_size[0], j:j+block_size[1]] == color):
                return (i, j)
    return None

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find gray pixels.
    gray_pixels = find_objects(input_grid, 5)
    
    # Find the 2x2 red block.
    red_block_pos = find_block(input_grid, 2)

    if red_block_pos is None:
        return output_grid

    # Define target positions for gray pixels relative to the red block.
    target_positions = [
        (red_block_pos[0] - 1, red_block_pos[1]),  # Top of top-left
        (red_block_pos[0] , red_block_pos[1]+2),      # Right of top-right
        (red_block_pos[0] +2, red_block_pos[1]+2)     # Below bottom-right
    ]
    
    # Move gray pixels to their new positions, remove from origin
    for i, pos in enumerate(target_positions):
      if i < len(gray_pixels):
        old_r, old_c = gray_pixels[i]
        output_grid[old_r, old_c] = 0  # Remove from old position
        output_grid[pos[0], pos[1]] = 5     # place at new position
        

    return output_grid
```
