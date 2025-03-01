"""
The transformation extracts gray (5) shapes from the input grid and redraws them, scaled down, into a 9x9 output grid. The shapes and relative positions of the gray objects are preserved during the scaling. The scaling is done by finding a bounding box that encompasses all gray objects, and then proportionally scaling that box to fit within the 9x9 output grid.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the specified color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                stack = [(r, c)]
                while stack:
                    curr_r, curr_c = stack.pop()
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color and not visited[curr_r, curr_c]:
                        visited[curr_r, curr_c] = True
                        obj.append((curr_r, curr_c))
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c), (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects.append(obj)
    return objects

def get_encompassing_bounding_box(objects):
    # Calculate a bounding box encompassing a *list* of objects.
    all_coords = [coord for obj in objects for coord in obj]
    if not all_coords:  # Handle the case where there are no objects.
        return (0, 0, 0, 0)
    min_r = min(r for r, c in all_coords)
    max_r = max(r for r, c in all_coords)
    min_c = min(c for r, c in all_coords)
    max_c = max(c for r, c in all_coords)
    return (min_r, min_c, max_r, max_c)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)

    # Find gray objects
    gray_objects = find_objects(input_grid, 5)

    # Find encompassing bounding box
    min_r, min_c, max_r, max_c = get_encompassing_bounding_box(gray_objects)

    # Calculate scaling factors
    bbox_height = max_r - min_r + 1
    bbox_width = max_c - min_c + 1

    if bbox_height == 0 or bbox_width == 0:  # Handle cases with no objects or a single point
        scale = 0  # No scaling if there are no gray pixels
    else:
        scale = min(9 / bbox_height, 9 / bbox_width)


    # Extract and project pattern into smaller grid, scaling based off encompassing box
    for obj in gray_objects:
        for r, c in obj:
          # calculate scaled coordinates using the encompassing bounding box
          scaled_r = int((r - min_r) * scale)
          scaled_c = int((c - min_c) * scale)

          # Check bounds (due to rounding, some coordinates might fall outside)
          if 0 <= scaled_r < 9 and 0 <= scaled_c < 9:
            output_grid[scaled_r, scaled_c] = 5

    return output_grid