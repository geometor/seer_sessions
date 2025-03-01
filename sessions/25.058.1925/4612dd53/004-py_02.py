"""
The transformation identifies shapes created by blue objects, and changes white
cells inside and diagonally adjacent to the blue pixels to red.
"""

import numpy as np

def find_blue_objects(grid):
    """Finds contiguous regions of blue (1) pixels."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != 1:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_inside(r, c, object_coords):
    """Crude check if a point is inside a shape defined by object_coords."""
    # Find the bounding box of the object
    min_r = min(coord[0] for coord in object_coords)
    max_r = max(coord[0] for coord in object_coords)
    min_c = min(coord[1] for coord in object_coords)
    max_c = max(coord[1] for coord in object_coords)

    # Check if the point is within the bounding box
    if not (min_r <= r <= max_r and min_c <= c <= max_c):
        return False

    # Basic 'enclosed' check:  If the cell is within the bounding box, consider it "inside".
    #  More sophisticated methods might be needed for concave shapes.
    return True


def is_diagonally_adjacent(r, c, object_coords):
    """Checks if a cell (r, c) is diagonally adjacent to any cell in object_coords."""
    for obj_r, obj_c in object_coords:
        if abs(r - obj_r) == 1 and abs(c - obj_c) == 1:
            return True
    return False

def transform(input_grid):
    # Initialize output_grid with a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = len(input_grid), len(input_grid[0])

    # Find blue objects
    blue_objects = find_blue_objects(input_grid)

    # Iterate through all cells
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 0:  # Consider only white cells
                for obj_coords in blue_objects:

                    if is_inside(r,c, obj_coords) or is_diagonally_adjacent(r, c, obj_coords):
                        output_grid[r][c] = 2  # Fill with red
                        break # move to the next cell

    return output_grid