```python
"""
Transforms an irregular yellow region in the input grid into a centered, expanded square in the output grid.
"""

import numpy as np

def find_yellow_region(grid):
    # Find coordinates of all yellow pixels
    yellow_coords = np.argwhere(grid == 4)
    return yellow_coords

def bounding_box(coords):
    # Calculate the bounding box of a set of coordinates
    if len(coords) == 0:
      return None
    
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    return (min_row, min_col, max_row, max_col)

def expand_box(bbox):

    min_row, min_col, max_row, max_col = bbox

    # Calculate center of input
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2

    # expand
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    new_height = height + 2
    new_width = width + 2

    # compute new corners
    new_min_row = center_row - new_height // 2
    new_max_row = new_min_row + new_height - 1
    new_min_col = center_col - new_width // 2
    new_max_col = new_min_col + new_width - 1
    
    return (new_min_row, new_min_col, new_max_row, new_max_col)


def transform(input_grid):
    # Initialize output grid with all zeros (white)
    output_grid = np.zeros((6,6), dtype=int) # all outputs so far have been 6 x 6
    input_grid = np.array(input_grid) # ensure it is a numpy array

    # Find the yellow region coordinates
    yellow_coords = find_yellow_region(input_grid)

    # If no yellow region, return a blank grid
    if len(yellow_coords) == 0:
        return output_grid.tolist() # task requires a list

    # Determine the bounding box
    bbox = bounding_box(yellow_coords)

    # expand the box
    expanded_bbox = expand_box(bbox)
    
    new_min_row, new_min_col, new_max_row, new_max_col = expanded_bbox

    # fit box into the output
    height, width = output_grid.shape
    new_min_row = max(0,new_min_row)
    new_min_col = max(0, new_min_col)
    new_max_row = min(height -1, new_max_row)
    new_max_col = min(width - 1, new_max_col)

    # Fill the expanded square region with yellow (4)
    for row in range(new_min_row, new_max_row + 1):
        for col in range(new_min_col, new_max_col + 1):
            output_grid[row, col] = 4
            
    return output_grid.tolist()
```