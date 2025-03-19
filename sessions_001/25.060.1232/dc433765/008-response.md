# dc433765 • 008 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all pixels that are part of the green object. An object is defined as a contiguous set of pixels of the same color. Also, find the single pixel that makes up the yellow object (if it exists).

2.  **Calculate Center:** Determine the center of the grid. This is found by integer division of the number of rows and columns by 2 ( `rows // 2`, `cols // 2`). If the grid has an even number of rows or columns, the center is considered to be the top-left pixel of the four central pixels.

3. **Determine Green Object Extent:** Find the bounding box around green object.

4.  **Move Green Object:** Move the *entire* green object to the center of the output grid. The top-left corner of the green object's bounding box should be positioned such that the object is centered. The shape and dimensions of the green object must match the input.

5.  **Preserve Yellow Object:** If a yellow object exists in the input grid, maintain its exact position in the output grid.

6.  **Clear Remaining Pixels:** Set all other pixels in the output grid to white (0).
"""

import numpy as np

def find_object_extents(grid, color):
    # Find the coordinates of a specific color in the grid.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None  # No object found
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return min_row, min_col, height, width

def calculate_center(grid):
    # Calculate the center of the grid.
    rows, cols = grid.shape
    return rows // 2, cols // 2

def transform(input_grid):
    # Initialize output_grid as all white (0).
    output_grid = np.zeros_like(input_grid)

    # Find the green object (color 3) and its extents.
    green_row, green_col, green_height, green_width = find_object_extents(input_grid, 3)
    
    # Find the yellow object (color 4) and its extents.
    yellow_row, yellow_col, _, _ = find_object_extents(input_grid, 4)

    # Calculate the center of the grid.
    center_row, center_col = calculate_center(input_grid)

    # Move the green object to the center.
    if green_row is not None:
        # Calculate the top-left corner position for the centered green object.
        green_top = center_row - green_height // 2
        green_left = center_col - green_width // 2

        # Copy the green object to the output grid.
        for i in range(green_height):
            for j in range(green_width):
                if 0 <= green_top + i < output_grid.shape[0] and 0 <= green_left + j < output_grid.shape[1]:
                    output_grid[green_top + i, green_left + j] = input_grid[green_row+i, green_col+j]

    # Keep yellow object at the original position.
    if yellow_row is not None:
      output_grid[yellow_row, yellow_col] = 4

    return output_grid
```
