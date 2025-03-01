# a740d043 • 006 • refine_coder

---
```python
"""
Extract a subgrid around the interaction of green and red objects, dynamically determining the center and size.
"""

import numpy as np

def find_objects(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return []

    # Group coordinates into contiguous objects
    objects = []
    visited = set()
    for r, c in coords:
        if (r, c) not in visited:
            obj_coords = []
            queue = [(r, c)]
            while queue:
                curr_r, curr_c = queue.pop(0)
                if (curr_r, curr_c) in visited:
                    continue
                visited.add((curr_r, curr_c))
                obj_coords.append([curr_r, curr_c])
                # Check adjacent cells
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_r, new_c = curr_r + dr, curr_c + dc
                    if 0 <= new_r < grid.shape[0] and 0 <= new_c < grid.shape[1] and grid[new_r, new_c] == color and (new_r, new_c) not in visited:
                        queue.append((new_r, new_c))
            objects.append(np.array(obj_coords))
    return objects

def get_center(coords):
    # Get the center coordinate of a group of pixels.
    return np.mean(coords, axis=0).astype(int)

def get_top_left(coords):
    # Get the top-left coordinate of a group of pixels.
    min_row = np.min(coords[:, 0])
    min_col = np.min(coords[:, 1])
    return np.array([min_row, min_col])

def min_distance(green_obj, red_objects):
    """find minimum distance between a green object and any red object"""
    min_dist = float('inf')
    for red_obj in red_objects:
        for green_coord in green_obj:
            for red_coord in red_obj:
                dist = abs(green_coord[0]-red_coord[0]) + abs(green_coord[1]-red_coord[1])
                if dist < min_dist:
                    min_dist = dist
                    closest_green = green_coord
    return closest_green

def transform(input_grid):
    # Find green and red objects.
    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)

    # Determine the reference point.
    if len(green_objects) == 1 and len(red_objects) == 1:
      # Center of the red object.
      reference_point = get_center(red_objects[0])
    else:
      # Top-left corner of the green object closest to any red object.
      closest_green = min_distance(green_objects[0], red_objects)
      reference_point = closest_green
      

    # Initialize output grid with white.
    output_grid = np.zeros((3, 3), dtype=int)

    # Calculate the offset for the 3x3 subgrid within the input grid.
    row_offset = reference_point[0] - 1
    col_offset = reference_point[1] - 1

    # Transfer red and green pixels to the output grid.
    for r in range(3):
        for c in range(3):
            input_row = row_offset + r
            input_col = col_offset + c

            # Check if the input coordinates are within the bounds of the input grid.
            if 0 <= input_row < input_grid.shape[0] and 0 <= input_col < input_grid.shape[1]:
                pixel = input_grid[input_row, input_col]
                if pixel == 2 or pixel == 3:  # red and green
                    output_grid[r, c] = pixel

    return output_grid
```
