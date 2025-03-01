# 7df24a62 • 012 • refine_coder

---
```python
"""
Copies yellow pixels from the input to the output grid. Conditionally creates a 3x4 blue block with a central yellow pixel based on the presence and position of yellow pixels in the input.
"""

import numpy as np

def find_yellow_pixels(grid):
    """Finds the coordinates of all yellow (4) pixels in the grid."""
    return np.argwhere(grid == 4)

def create_blue_block(output_grid, center_x, center_y):
    """Creates a 3x4 blue block with a central yellow pixel."""
    for i in range(center_y - 1, center_y + 3):  # Iterate for height of 4
        for j in range(center_x - 1, center_x + 2):  # width of three
            if 0 <= i < output_grid.shape[0] and 0 <= j < output_grid.shape[1]:
                output_grid[i, j] = 1
    # Place yellow pixel at center
    yellow_row = center_y + 1
    yellow_col = center_x
    if 0 <= yellow_row < output_grid.shape[0] and 0 <= yellow_col < output_grid.shape[1]:
        output_grid[yellow_row, yellow_col] = 4

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Copy Yellow Pixels
    yellow_pixels = find_yellow_pixels(input_grid)
    #for y, x in yellow_pixels:  #This is redundant as we copied the input grid
    #    output_grid[y, x] = 4

    # Conditional Blue Block Creation
    if len(yellow_pixels) > 0:
        # Find midpoints
        min_y = np.min(yellow_pixels[:, 0])
        max_y = np.max(yellow_pixels[:, 0])
        min_x = np.min(yellow_pixels[:, 1])
        max_x = np.max(yellow_pixels[:, 1])

        mid_y = (min_y + max_y) // 2
        mid_x = (min_x + max_x) // 2
        
        # Blue block placement based on example
        if max_y - min_y <= 1 :
          center_y = mid_y - 2
        else :
          center_y = max_y

        center_x = mid_x
        create_blue_block(output_grid, center_x, center_y)
    else:
        # Center of the grid
        center_y = height // 2
        center_x = width // 2
        create_blue_block(output_grid, center_x, center_y-1)


    return output_grid
```
