# a87f7484 • 018 • refine_coder

---
```python
"""
The transformation extracts a subgrid from the input grid. This subgrid is defined by the bounding box surrounding all yellow pixels. The output grid is a direct copy of this subgrid, preserving all colors and their relative positions.
"""

import numpy as np

def find_object_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    coords = np.argwhere(grid == color)
    return coords

def get_bounding_box(coords):
    """Calculates the bounding box of a set of coordinates. Handles empty coordinate lists."""
    if len(coords) == 0:
        return 0, 0, -1, -1  # Return an invalid bounding box
    min_y, min_x = np.min(coords, axis=0)
    max_y, max_x = np.max(coords, axis=0)
    return min_y, min_x, max_y, max_x

def extract_subgrid(grid, bounding_box):
    """Extracts a subgrid defined by the bounding box. Handles invalid bounding boxes."""
    min_y, min_x, max_y, max_x = bounding_box
    if min_y > max_y or min_x > max_x: #invalid
        return np.array([[]])
    return grid[min_y:max_y+1, min_x:max_x+1]

def transform(input_grid):
    """Extracts a subgrid based on yellow pixels in the input"""
    # Find all yellow pixels
    yellow_coords = find_object_by_color(input_grid, 4)

    # Determine the bounding box formed by the yellow pixels.
    bounding_box = get_bounding_box(yellow_coords)

    # Extract the region defined by the bounding box.
    output_grid = extract_subgrid(input_grid, bounding_box)

    return output_grid
```
