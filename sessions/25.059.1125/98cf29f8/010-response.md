# 98cf29f8 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves repositioning the yellow shape relative to the red rectangle, creating a vertically aligned, smaller rectangle from an irregular shape.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None
    # Calculate top-left and bottom-right coordinates
    min_y, min_x = coords.min(axis=0)
    max_y, max_x = coords.max(axis=0)
    # Extract the object's shape
    shape = grid[min_y:max_y+1, min_x:max_x+1]
    return (min_x, min_y), shape, (min_x,min_y) # Return top_left, shape, and topleft again (for consistency)


def move_object(output_grid, shape, new_position):
    # Place the shape onto the output grid at the new position
    x, y = new_position
    height, width = shape.shape
    output_grid[y:y+height, x:x+width] = shape
    return output_grid
    
def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the red rectangle
    red_top_left, red_shape, _ = find_object(input_grid, 2)

    # Find the yellow shape
    yellow_top_left, yellow_shape, yellow_origin = find_object(input_grid, 4)
    
    #create the regularized yellow shape
    new_yellow_shape = np.full((3, 3), 4)


    # Determine the new position for the yellow shape
    #   - Aligned vertically with the top of the red rectangle
    #   - x coordinate matches the red rectangle's x coordinate
    new_yellow_position = (red_top_left[0]-3, red_top_left[1])

    #clear the old yellow from the grid
    for y in range(yellow_origin[1], yellow_origin[1] + yellow_shape.shape[0]):
          for x in range(yellow_origin[0], yellow_origin[0] + yellow_shape.shape[1]):
            if input_grid[y,x] == 4:
              output_grid[y, x] = 0

    # Move the yellow shape to its new position in the output grid
    output_grid = move_object(output_grid, new_yellow_shape, new_yellow_position)
    
    return output_grid
```
