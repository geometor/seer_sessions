# e48d4e1a • 018 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify Objects: Recognize the white background (0), the magenta cross shape (6), and the gray shape(5).
2. Remove Gray: Remove the gray shape(5)
3. Rotate Magenta Shape: Rotate the magenta cross shape 90 degrees counter-clockwise.
4. Remove Center: From rotated figure, remove the new intersection point of the vertical and horizontal bars of the rotated cross.
5. Output: The resulting grid consists of the rotated magenta shape minus its central intersection point on the white background.
"""

import numpy as np

def find_object(grid, color):
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    return coords

def rotate_magenta_shape(grid, magenta_coords):
  #make a copy to modify
    rotated_grid = np.copy(grid)

    # Find the center of the magenta cross.  For this particular
    # object, the center is the average of all magenta coordinates.
    center_row = int(np.mean(magenta_coords[:, 0]))
    center_col = int(np.mean(magenta_coords[:, 1]))
    
    #clear old cross
    for r, c in magenta_coords:
        rotated_grid[r,c] = 0

    new_magenta_coords = []
    for r, c in magenta_coords:
        # Translate to origin
        translated_row = r - center_row
        translated_col = c - center_col

        # Rotate 90 degrees counter-clockwise
        rotated_row = translated_col
        rotated_col = -translated_row

        # Translate back to original position
        new_row = rotated_row + center_row
        new_col = rotated_col + center_col
        new_magenta_coords.append( (new_row,new_col) )

    return rotated_grid, new_magenta_coords

def remove_center(grid, magenta_coords):
    # Find new center - assume shape is an L
    min_row = min(magenta_coords, key=lambda item: item[0])[0]
    max_row = max(magenta_coords, key=lambda item: item[0])[0]
    min_col = min(magenta_coords, key=lambda item: item[1])[1]
    max_col = max(magenta_coords, key=lambda item: item[1])[1]

    center_row = max_row
    center_col = min_col
    
    grid[center_row, center_col] = 0

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find and Remove Gray (5)
    gray_coords = find_object(output_grid, 5)
    if gray_coords is not None:
        for r, c in gray_coords:
            output_grid[r, c] = 0

    # Find Magenta (6)
    magenta_coords = find_object(output_grid, 6)

    # Rotate
    rotated_grid, new_magenta_coords = rotate_magenta_shape(output_grid, magenta_coords)
    output_grid = rotated_grid

    #rebuild and Find new center after rotation
    new_magenta_coords_arr = np.array([(r,c) for r,c in new_magenta_coords if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]])
    new_magenta_coords_valid = [(r,c) for r,c in new_magenta_coords if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]]

    #remove old points, and set new points
    for r,c in magenta_coords:
      output_grid[r,c]=0
    for r,c in new_magenta_coords_valid:
      output_grid[r,c] = 6

    remove_center(output_grid, new_magenta_coords_arr)


    return output_grid
```
