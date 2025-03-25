```python
"""
Transforms an irregular yellow region in the input grid into a centered, expanded rectangle in the output grid.
The output width is twice the input bounding box width.
The output height is 6, unless the input height is greater than the input width, in which case the output height is also twice the input bounding box width.
The output is filled with a centered yellow rectangle where rows or columns are added as needed.
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

def transform(input_grid):
    input_grid = np.array(input_grid)

    # 1. Identify the Yellow Region
    yellow_coords = find_yellow_region(input_grid)

    # If no yellow region, return a blank grid (arbitrary size, based on prompt examples)
    if len(yellow_coords) == 0:
        return np.zeros((6,6), dtype=int).tolist()

    # 2. Bounding Box
    bbox = bounding_box(yellow_coords)
    min_row, min_col, max_row, max_col = bbox
    input_width = max_col - min_col + 1
    input_height = max_row - min_row + 1


    # 3. Determine Output Dimensions
    output_width = 2 * input_width
    output_height = 6 if input_height <= input_width else 2 * input_width

    # 4. Create Output Grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 5. Determine Inner Filled Rectangle Dimensions
    fill_width = input_width * 2
    fill_height = input_height

    if fill_width > output_width:
      fill_width = output_width
    
    if fill_height > output_height:
      fill_height = output_height

    if input_height <= input_width:
      fill_height = output_width # add rows to make a square
    else:
       fill_width = output_height # add columns to make a square

    # 6. Center and Fill
    row_start = (output_height - fill_height) // 2
    col_start = (output_width - fill_width) // 2

    for row in range(row_start, row_start + fill_height):
        for col in range(col_start, col_start + fill_width):
            output_grid[row, col] = 4
            
    return output_grid.tolist()
```