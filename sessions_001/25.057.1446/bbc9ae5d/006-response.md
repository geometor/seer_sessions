# bbc9ae5d • 006 • refine_coder

---
```python
"""
1.  **Identify** the blue (1) object within the input grid.
2.  **Determine** the bounding box of this blue object, specifically noting its height and the x-coordinates of its left-most and right-most pixels (min and max columns).
3.  **Create** an output grid. The output grid's width is the same as the input grid's width. The output grid's height is the same as blue object's height.
4. **Fill** a rectangle within the output grid with blue (1) pixels. This rectangle's height is the same height as the blue object's height. Its width spans from the leftmost x-coordinate to the rightmost x-coordinate of the blue object in the input grid. The y position is set to 0.
5. copy the white pixels from the input to the output
"""

import numpy as np

def get_blue_object_bbox(grid):
    # return bounding box of the blue object
    rows, cols = np.where(grid == 1)
    if rows.size > 0:
        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)
        return {
            'min_row': min_row,
            'max_row': max_row,
            'min_col': min_col,
            'max_col': max_col,
            'height': max_row - min_row + 1,
            'width': max_col - min_col + 1
        }
    else:
        return None

def get_white_pixels(grid):
    # return a list of (x,y) coordinates for all white pixels
    white_pixels = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 0:
                white_pixels.append((x, y))
    return white_pixels

def transform(input_grid):
    # get bounding box of the blue object
    blue_bbox = get_blue_object_bbox(input_grid)

    # create an output grid
    if blue_bbox:
        output_height = blue_bbox['height']
    else:
        output_height = 0 # or input_grid.shape[0]? Consider what to do when no blue object
    output_grid = np.zeros((max(output_height,input_grid.shape[0]), input_grid.shape[1]), dtype=int)

    # fill rectangle with blue pixels
    if blue_bbox:
        for y in range(blue_bbox['height']):
            for x in range(blue_bbox['min_col'], blue_bbox['max_col'] + 1):
                output_grid[y, x] = 1
    
    # copy ALL white pixels, preserving position
    white_pixels = get_white_pixels(input_grid)
    for x, y in white_pixels:
        if y < output_grid.shape[0]:  # Ensure we don't write out of bounds
             output_grid[y, x] = 0

    return output_grid
```
