# c8cbb738 • 006 • example_1 • investigate_coder

---
```python
"""
The transformation extracts a 5x5 subgrid from the input grid. This subgrid is defined by 
identifying the minimum bounding box of all non-green colors in input grid.
This region is extended by 1 cell in each direction (up, down, left, right).
The colors and relative positions within this bounding box are preserved.
"""

import numpy as np

def get_bounding_box(grid):
    # Find coordinates of non-green pixels
    non_green_coords = np.argwhere(grid != 3)

    # If no non-green pixels are found, return default box
    if non_green_coords.size == 0:
        return (0, 0, grid.shape[0]-1, grid.shape[1]-1)

    # Get min and max row/col indices
    min_row = np.min(non_green_coords[:, 0])
    max_row = np.max(non_green_coords[:, 0])
    min_col = np.min(non_green_coords[:, 1])
    max_col = np.max(non_green_coords[:, 1])

    return (min_row, min_col, max_row, max_col)

def add_padding(bounding_box, grid_shape, padding=1):
    min_row, min_col, max_row, max_col = bounding_box

    # increase bounding box by adding padding.
    min_row = max(0, min_row - padding)
    min_col = max(0, min_col - padding)
    max_row = min(grid_shape[0] -1, max_row + padding)
    max_col = min(grid_shape[1] -1 , max_col + padding)

    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Get the bounding box of non-green pixels
    bounding_box = get_bounding_box(input_grid)
    
    #add padding around bounding box
    padded_bounding_box = add_padding(bounding_box, input_grid.shape)
    
    min_row, min_col, max_row, max_col = padded_bounding_box

    # Extract the 5x5 subgrid
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    #if output grid not square, pad green on shortest edge
    while output_grid.shape[0] != output_grid.shape[1]:
        if output_grid.shape[0] < output_grid.shape[1]:
           padding = ((0,1),(0,0))
        elif output_grid.shape[1] < output_grid.shape[0]:
           padding = ((0,0),(0,1))
           
        output_grid = np.pad(output_grid, padding, mode='constant', constant_values=3)
           
    return output_grid.tolist()
```
