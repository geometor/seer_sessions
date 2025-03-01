# 0b148d64 • 018 • refine_coder

---
```python
"""
1.  **Identify the Target Region:** Locate the contiguous region of yellow (4) pixels in the input grid. It is at the bottom-left.
2.  **Define Extraction Boundaries:** Determine a rectangular boundary around the yellow region. Expand the region to contain contiguous white or blue pixels.
3.  **Extract Sub-Grid:** from the coordinates of the bounding box created, copy the contents.
4.  **Form Output:** The resulting sub-grid becomes the output grid.
"""

import numpy as np

def find_object(grid, color):
    # returns a list of coordinates
    coords = np.argwhere(grid == color)
    return coords

def get_bounding_box(coords):
    # finds the bounding box of a set of coordinates
    min_y = np.min(coords[:, 0])
    max_y = np.max(coords[:, 0])
    min_x = np.min(coords[:, 1])
    max_x = np.max(coords[:, 1])
    return (min_y, min_x), (max_y, max_x)

def expand_bounding_box(grid, top_left, bottom_right):
    # Expands the bounding box to include contiguous white and blue pixels
    min_y, min_x = top_left
    max_y, max_x = bottom_right
    
    
    def is_valid(y, x):
        # check if pixel is in the grid
        return 0 <= y < grid.shape[0] and 0 <= x < grid.shape[1]
    
    def should_expand(y,x):
        # only expand to white or blue
        return (grid[y,x] == 0) or (grid[y,x] == 1)

    
    # Expand upwards
    while min_y > 0 and should_expand(min_y - 1, min_x):
        min_y -= 1
    # Expand downwards
    while max_y < grid.shape[0] - 1 and should_expand(max_y + 1, min_x):
        max_y += 1
    # Expand left
    while min_x > 0 and should_expand(min_y, min_x - 1):
        min_x -= 1
    # Expand Right
    while max_x < grid.shape[1] - 1 and should_expand(min_y, max_x+1):
        max_x += 1
        
    # Expand upwards
    while min_y > 0 and should_expand(min_y - 1, max_x):
        min_y -= 1
    # Expand downwards
    while max_y < grid.shape[0] - 1 and should_expand(max_y + 1, max_x):
        max_y += 1    
        
    # diagonal expansion
    while min_y > 0 and min_x > 0 and should_expand(min_y-1, min_x - 1):
            min_y -= 1
            min_x -= 1    
    while max_y < grid.shape[0] -1 and max_x < grid.shape[1] - 1 and should_expand(max_y + 1, max_x + 1):
        max_y += 1
        max_x += 1

    return (min_y, min_x), (max_y, max_x)

def transform(input_grid):
    # Find coordinates of yellow pixels (color 4).
    yellow_coords = find_object(input_grid, 4)

    # Determine the bounding box around the yellow region.
    top_left, bottom_right = get_bounding_box(yellow_coords)

    # Expand bounding box
    top_left, bottom_right = expand_bounding_box(input_grid, top_left, bottom_right)
   
    # Extract the sub-grid based on the bounding box.
    output_grid = input_grid[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1].copy()

    return output_grid
```
