# 47c1f68c • 016 • example_3 • investigate_coder

---
```python
"""
1. Identify the cross shape composed of yellow (4) pixels in the input grid.
2. Filter: Remove all pixels that are not yellow (4).
3. Rotate: Rotate the remaining pixels 90 degrees clockwise.
"""

import numpy as np

def get_yellow_object(grid):
    # Find the coordinates of yellow pixels
    yellow_coords = np.argwhere(grid == 4)
    return yellow_coords

def rotate_point(point, origin, angle_degrees):
    """Rotate a point around an origin by a given angle in degrees."""
    angle_radians = np.radians(angle_degrees)
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle_radians) * (px - ox) - np.sin(angle_radians) * (py - oy)
    qy = oy + np.sin(angle_radians) * (px - ox) + np.cos(angle_radians) * (py - oy)
    return int(round(qx)), int(round(qy))
    

def transform(input_grid):
    """Transforms the input grid by extracting the yellow cross, rotating it 90 degrees clockwise,
    and placing it in a new grid."""

    input_grid = np.array(input_grid)
    
    # 1. Identify yellow pixels
    yellow_coords = get_yellow_object(input_grid)

    # 2. Determine the center of the yellow object for rotation.  Use the centroid.
    centroid_row = int(np.mean(yellow_coords[:, 0]))
    centroid_col = int(np.mean(yellow_coords[:, 1]))
    centroid = (centroid_row, centroid_col)

    #initialize the output grid
    #find min and max row after rotation to determine output grid size
    rotated_coords = []
    for coord in yellow_coords:
      rotated_coords.append(rotate_point( (coord[0], coord[1]), centroid, 90))
    min_row = min(rotated_coords, key=lambda item:item[0])[0]
    max_row = max(rotated_coords, key=lambda item:item[0])[0]

    min_col = min(rotated_coords, key=lambda item:item[1])[1]
    max_col = max(rotated_coords, key=lambda item:item[1])[1]

    output_grid_rows = max_row - min_row + 1
    output_grid_cols = max_col - min_col + 1
    output_grid = np.zeros((output_grid_rows, output_grid_cols), dtype=int)

    # 3. & 4. Rotate and place in output grid.
    rotated_coords = []
    row_offset = 0 - min_row
    col_offset = 0 - min_col
    for coord in yellow_coords:
        rotated_coord = rotate_point( (coord[0], coord[1]), centroid, 90)
        rotated_row = rotated_coord[0] + row_offset
        rotated_col = rotated_coord[1] + col_offset
        
        output_grid[rotated_row, rotated_col] = 4


    return output_grid.tolist()
```
