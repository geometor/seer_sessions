"""
1. Identify two objects within the grid: a magenta (6) inverted-U shape at the top and a red (2) square with a hole beneath it.
2. Locate the leftmost column of the red object.
3. Change the color of the pixels in that column, of the red object, to white (0).
4. Leave all other parts of the image unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid based on color contiguity.
    Returns a dictionary where keys are object IDs and values are lists of (row, col) coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, object_id):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        objects.setdefault(object_id, []).append((row, col))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(row + dr, col + dc, color, object_id)

    object_id_counter = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                object_id_counter += 1
                dfs(r, c, grid[r, c], object_id_counter)
    return objects

def get_leftmost_column(object_coords):
    """
    Returns the column index of the leftmost pixel in the object.
    """
    return min(col for _, col in object_coords)


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find objects
    objects = find_objects(input_grid)

    # find red object (color 2)
    red_object_id = None
    for obj_id, coords in objects.items():
        if input_grid[coords[0]] == 2:  # Check color of the first pixel
            red_object_id = obj_id
            break
    
    if red_object_id is None:
        return output_grid  # Return original if no red object found

    # locate leftmost col
    red_object_coords = objects[red_object_id]
    leftmost_col = get_leftmost_column(red_object_coords)


    # change red pixels in that column to white
    for r, c in red_object_coords:
        if c == leftmost_col:
           output_grid[r,c] = 0

    return output_grid