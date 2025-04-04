# 3906de3d • 010 • example_2 • investigate_coder

---
```python
"""
Identifies a blue shape and a red shape in the input grid. Moves the red color upwards to be adjacent to or within the outline of the blue shape, creating a contiguous red area within the blue shape.
"""

import numpy as np

def find_shape(grid, color):
    """Finds the coordinates of pixels of a specific color."""
    coords = np.argwhere(grid == color)
    return coords

def transform(input_grid):
    """Transforms the input grid by moving red pixels upwards to the blue shape."""
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Find the blue and red shapes
    blue_coords = find_shape(input_grid, 1)
    red_coords = find_shape(input_grid, 2)
    
    # Get boundaries
    min_blue_row = np.min(blue_coords[:, 0]) if len(blue_coords) > 0 else 0

    # Transfer red color upwards
    for r_coord in red_coords:
        row, col = r_coord
        
        nearest_blue_row = -1
        min_dist = float('inf')
        
        for b_row, b_col in blue_coords:
            if b_row <= row and b_col == col :
                nearest_blue_row = b_row
                break;
            elif b_row <= row :
                dist = abs(b_col - col) + abs(b_row - row) # Manhattan distance
                if dist < min_dist:
                    min_dist = dist
                    nearest_blue_row = b_row


        if nearest_blue_row != -1:
             output_grid[nearest_blue_row:row, col] = 2
        else:
            # find closest blue pixel if we are outside of range
             for b_row, b_col in blue_coords:
                if b_row <= min_blue_row :
                    dist = abs(b_col - col) + abs(b_row - row)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_blue_row = b_row
             output_grid[nearest_blue_row:row, col] = 2

    return output_grid
```
