# 98cf29f8 • 014 • refine_coder

---
```python
"""
1.  **Identify Red and Yellow Objects:** Find the bounding rectangles of all red and yellow pixels in the input grid.
2.  **Clear Yellow:** Remove the original yellow object from the grid.
3.  **Reshape Yellow:** Create a new yellow object. The new yellow object is always one pixel in height and one pixel in width.
4. **Position Yellow:**
    The new yellow object's x coordinate is the same as the red object's x coordinate of its top edge, plus half of its width (rounded down).
    The new yellow object's y coordinate is one less than the y-coordinate of the top edge of the red object.
5. **Place** place the new yellow object at the new position.
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
    return (min_x, min_y), shape, (min_x, min_y)

def clear_color(grid, color):
    #set all pixels of the color to zero
    grid[grid == color] = 0
    return grid

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find the red rectangle
    red_top_left, red_shape, _ = find_object(input_grid, 2)
    if red_top_left is None:
        return output_grid  # Nothing to do

    # Find and clear the yellow shape
    yellow_top_left, yellow_shape, yellow_origin = find_object(input_grid, 4)
    if yellow_top_left is None:
        return output_grid  # Nothing to do
    output_grid = clear_color(output_grid, 4)

    # Create the reshaped yellow object: 1x1 pixel
    new_yellow_shape = np.array([[4]])

    # Determine the new position for the yellow shape: above red, centered
    new_yellow_x = red_top_left[0] + red_shape[1] // 2
    new_yellow_y = red_top_left[1] - 1
    new_yellow_position = (new_yellow_x, new_yellow_y)


    # Place the reshaped yellow shape, handling out-of-bounds
    if 0 <= new_yellow_x < output_grid.shape[1] and 0 <= new_yellow_y < output_grid.shape[0]:
        output_grid[new_yellow_y, new_yellow_x] = 4

    return output_grid
```
