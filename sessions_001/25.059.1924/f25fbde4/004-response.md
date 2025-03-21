# f25fbde4 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to identify a cross-shaped object made of yellow pixels in the input grid, 
determine its boundaries, and then fill the bounding box defined by those boundaries with yellow pixels, 
and finally cropping rows and columns that are all white at the image boundary.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords

def bounding_box(coords):
    # Calculate the bounding box of a set of coordinates.
    min_y, min_x = np.min(coords, axis=0)
    max_y, max_x = np.max(coords, axis=0)
    return min_y, min_x, max_y, max_x

def crop_grid(grid):
    # Crop empty (all zero) rows and cols
    rows_to_keep = np.any(grid != 0, axis=1)
    cols_to_keep = np.any(grid != 0, axis=0)
    cropped_grid = grid[rows_to_keep][:, cols_to_keep]
    return cropped_grid
    

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the yellow cross object.
    yellow_pixels = find_object(input_grid, 4)

    # If no yellow pixels are found, return an empty grid.
    if len(yellow_pixels) == 0:
        return np.array([])

    # Determine the bounding box of the cross.
    min_y, min_x, max_y, max_x = bounding_box(yellow_pixels)
    
    #create a new output grid that contains only the bounding box
    output_grid = np.copy(input_grid[min_y:max_y+1, min_x:max_x+1])

    # Fill the bounding box with yellow.
    output_grid[:] = 4
    
    #crop
    output_grid = crop_grid(output_grid)

    return output_grid
```
