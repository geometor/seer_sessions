# a740d043 • 008 • refine_coder

---
```python
"""
1.  **Identify the Region of Interest:** The region of interest is determined by the smallest rectangular bounding box enclosing all non-blue pixels, *unless* all pixels are blue, in which case it's the top-left pixel. If the non-blue region has a height or width of 0, select the entire input grid's corresponding rows or columns.
"""

import numpy as np

def find_non_blue_region(grid):
    # Find coordinates of non-blue pixels
    non_blue_coords = np.argwhere(grid != 1)
    return non_blue_coords

def get_bounding_box(coords, grid_shape):
    # Get the min and max row and col to define the bounding box

    if len(coords) == 0 : # special case of no non-blue pixels
        min_row, min_col = 0, 0
        max_row, max_col = 0, 0
    else :
        min_row, min_col = np.min(coords, axis=0)
        max_row, max_col = np.max(coords, axis=0)

    # Adjust for cases where region is empty, take entire corresponding rows/cols.
    if max_row - min_row < 0:
       max_row = grid_shape[0] -1

    if max_col - min_col < 0:
       max_col = grid_shape[1] - 1
        
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find the non-blue region
    non_blue_coords = find_non_blue_region(input_grid)

    # Get bounding box of non blue region, pass full input_grid shape
    min_row, min_col, max_row, max_col = get_bounding_box(non_blue_coords, input_grid.shape)

    # Calculate the dimensions of the output grid
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Initialize the output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the pixels from the input grid's region of interest to the output grid
    for i in range(output_height):
        for j in range(output_width):
            output_grid[i, j] = input_grid[min_row + i, min_col + j]
            
    return output_grid.tolist()
```
