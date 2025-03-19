# 6430c8c4 • 023 • refine_coder

---
```python
"""
1.  Identify the orange object: Find the contiguous block of orange (7) pixels in the input grid.
2.  Determine its shape and size:  Calculate the dimensions (height and width) of the orange object. It may be a square or a rectangle.
3.  Copy the shape:** Create a copy of the orange object's shape.
4.  Recolor the copy: Change the color of all pixels in the copied shape to green (3).
5.  Place the green shape: Position the green shape in the output grid at the *exact same location* as the original orange shape in the input grid. The top-left corner of the green shape should have the same row and column coordinates as the top-left corner of the orange shape.
6. The program should ignore any other colors.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color.
    pixels = np.argwhere(grid == color)
    if pixels.size == 0:
        return None, (0, 0)  # Return None for bounding box and (0,0) for size if no object found

    # Calculate the bounding box.
    min_row = np.min(pixels[:, 0])
    min_col = np.min(pixels[:, 1])
    max_row = np.max(pixels[:, 0])
    max_col = np.max(pixels[:, 1])

    bounding_box = (min_row, min_col, max_row + 1, max_col + 1)  # +1 for inclusive
    shape_size = (max_row - min_row + 1, max_col - min_col + 1) # rows, cols
    return bounding_box, shape_size

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the orange object.
    orange_bounding_box, orange_shape_size = find_object(input_grid, 7)
    if orange_bounding_box is None:
        return output_grid #return input grid if no orange object is found
    
    # Extract coordinates of top-left corner of orange object
    orange_top_left_row, orange_top_left_col = orange_bounding_box[0], orange_bounding_box[1]


    # Recolor the corresponding region in the output grid to green.
    for r in range(orange_shape_size[0]):
        for c in range(orange_shape_size[1]):
            output_grid[orange_top_left_row + r, orange_top_left_col + c] = 3

    return output_grid
```
