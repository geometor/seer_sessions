# 1f642eb9 • 012 • refine_coder

---
```python
"""
Insert a single pixel of a specific color to the left of each object of the target colors magenta (6), orange (7), green (3), blue (1), and red (2), according to a specific color mapping.
"""

import numpy as np

def find_objects(grid, color):
    """Finds all distinct objects of a given color in the grid."""
    mask = (grid == color)
    labeled_mask, num_labels = ndimage.label(mask)
    objects = []
    for i in range(1, num_labels + 1):
        coords = np.argwhere(labeled_mask == i)
        objects.append(coords)
    return objects

def transform(input_grid):
    """Transforms the input grid by inserting colored pixels to the left of target-colored objects."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Color mapping for insertion
    color_map = {
        6: 2,  # Magenta -> Red
        7: 1,  # Orange -> Blue
        3: 6,  # Green -> Magenta
        1: 3,  # Blue -> Green
        2: 7,  # Red -> Orange
    }

    # Iterate through target colors
    for target_color, insert_color in color_map.items():
        # Find all objects of the target color
        target_objects = find_objects(input_grid, target_color)

        # Iterate through each target object
        for obj_coords in target_objects:
            # Find the leftmost x-coordinate
            leftmost_x = min(coord[1] for coord in obj_coords)

            # Insert the pixel if within bounds
            insert_x = leftmost_x - 1
            if insert_x >= 0:
                insert_y = obj_coords[0][0]  # Row of the first pixel in the object
                output_grid[insert_y, insert_x] = insert_color

    return output_grid

from scipy import ndimage
```
