# a48eeaf7 • 006 • refine_coder

---
```python
"""
Moves one gray pixel to the position adjacent to the top-left corner of a 2x2 red block, and removes other gray pixels.
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

    # Determine the target position (top-left adjacent cell).
    target_row = red_block_pos[0] - 1
    target_col = red_block_pos[1] - 1


    # Move one gray pixel to the target position and remove the others
    if gray_pixels:
        # use the first grey pixel found
        old_r, old_c = gray_pixels[0]
        # only move if within bounds, and the target is empty
        if 0 <= target_row < output_grid.shape[0] and 0<= target_col < output_grid.shape[1] and output_grid[target_row, target_col] == 0:
          output_grid[target_row, target_col] = 5  # Move to target position
          output_grid[old_r, old_c] = 0       # clear the old position

    # Remove any other gray pixels
    for i in range(1, len(gray_pixels)):
      old_r, old_c = gray_pixels[i]
      output_grid[old_r, old_c] = 0



    return output_grid
```
