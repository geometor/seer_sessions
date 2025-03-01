# af902bf9 • 020 • refine_coder

---
```python
"""
Transforms an input grid by changing the central yellow (4) pixel of each contiguous yellow object to red (2) *only if* a blue (1) object is present in the input grid.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous regions (objects) of a specified color in a grid.
    Returns a list of lists, where each inner list contains the coordinates
    of pixels belonging to a single object.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def calculate_object_center(object_coordinates):
    """
    Calculates the centroid (center) of an object given its pixel coordinates.
    Returns (row_center, col_center) as floats.
    """
    rows, cols = zip(*object_coordinates)
    center_row = sum(rows) / len(rows)
    center_col = sum(cols) / len(cols)

    return center_row, center_col
    
def get_nearest_pixel(float_coords, object_coords):
    """
    Finds the nearest pixel to given float coordinates within object coordinates
    """
    min_dist = float('inf')
    nearest_pixel = None
    for pixel in object_coords:
        dist = (pixel[0] - float_coords[0])**2 + (pixel[1] - float_coords[1])**2
        if dist < min_dist:
            min_dist = dist
            nearest_pixel = pixel
    return nearest_pixel

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find yellow objects
    yellow_objects = find_objects(input_grid, 4)
    
    # Check for presence of blue object
    blue_objects = find_objects(input_grid, 1)
    blue_present = len(blue_objects) > 0

    # change output pixels
    for obj in yellow_objects:
        # Calculate object center
        center_row, center_col = calculate_object_center(obj)
        
        # Find the nearest pixel to the center
        pixel_to_change = get_nearest_pixel((center_row, center_col), obj)

        # Change center pixel to red, conditional on blue being present
        if blue_present:
            output_grid[pixel_to_change[0], pixel_to_change[1]] = 2
    
    return output_grid
```
