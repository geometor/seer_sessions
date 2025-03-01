# a87f7484 • 017 • refine_coder

---
```python
"""
1.  **Identify Yellow Pixels:** Locate all pixels with the color value 4 (yellow) within the input grid.
2.  **Bounding Box:** Determine the smallest rectangular bounding box that encompasses all identified yellow pixels.
3.  **Extract Subgrid:** Extract the subgrid defined by the bounding box.
4.  **Rotate:** Rotate the extracted subgrid 90 degrees clockwise.
5.  **Output:** The rotated subgrid is the output. If there are no yellow pixels, return an empty grid (or potentially a 1x1 grid with a default value – this needs clarification from more examples if they exist).
"""

import numpy as np

def find_object_by_color(grid, color):
    coords = np.argwhere(grid == color)
    return coords

def get_bounding_box(coords):
    if len(coords) == 0:  # Handle empty coords
        return 0, 0, -1, -1 #empty grid
    min_y, min_x = np.min(coords, axis=0)
    max_y, max_x = np.max(coords, axis=0)
    return min_y, min_x, max_y, max_x

def extract_subgrid(grid, bounding_box):
    min_y, min_x, max_y, max_x = bounding_box
    return grid[min_y:max_y+1, min_x:max_x+1]

def rotate_clockwise(grid):
    return np.rot90(grid, k=-1)

def transform(input_grid):
    # Find coordinates of yellow pixels.
    yellow_coords = find_object_by_color(input_grid, 4)

    # Get the bounding box around the yellow pixels.
    bounding_box = get_bounding_box(yellow_coords)

    # Extract the subgrid.
    subgrid = extract_subgrid(input_grid, bounding_box)

    # Rotate the subgrid clockwise.
    rotated_subgrid = rotate_clockwise(subgrid)

    return rotated_subgrid
```
