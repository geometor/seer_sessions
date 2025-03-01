"""
1.  **Identify Magenta Shapes:** Locate all contiguous blocks of magenta (6) pixels within the azure (8) background. These constitute the initial shapes.
2.  **Outline and Fill:** For each identified magenta shape, replace the azure pixels on the immediate outline with green(3). The shape interior defined by the magenta pixels is also replaced by green.
3.  **Inset Yellow Square:** In the top-most filled shape, find the two by two azure (8) pixel area at the center and change the azure color to yellow(4).
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous blocks of the specified color.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

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

def outline_and_fill(grid, object_coords, outline_color, fill_color):
    # Create a copy of the grid to modify
    modified_grid = np.copy(grid)

    # Determine boundary pixels for fill
    min_row = min(r for r, c in object_coords)
    max_row = max(r for r, c in object_coords)
    min_col = min(c for r, c in object_coords)
    max_col = max(c for r, c in object_coords)

    # fill
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            modified_grid[row, col] = fill_color

    # Outline the object
    for row, col in object_coords:

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < modified_grid.shape[0] and 0 <= nc < modified_grid.shape[1] and modified_grid[nr,nc] != fill_color):
                modified_grid[nr, nc] = outline_color


    return modified_grid

def get_topmost_object(objects):
    # Return the object with the smallest minimum row.
    if not objects:
        return None
    return min(objects, key=lambda obj: min(r for r, c in obj))

def get_object_center(object_coords):
    # compute the center of the object
    min_row = min(r for r, c in object_coords)
    max_row = max(r for r, c in object_coords)
    min_col = min(c for r, c in object_coords)
    max_col = max(c for r, c in object_coords)
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2

    return center_row, center_col

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find magenta objects.
    magenta_objects = find_objects(output_grid, 6)

    # Outline and fill each magenta object with green.
    for obj in magenta_objects:
        output_grid = outline_and_fill(output_grid, obj, 3, 3)

    # Find the topmost object.
    topmost_object = get_topmost_object(magenta_objects)

    # Insert yellow square in the topmost object
    if topmost_object:
        center_row, center_col = get_object_center(topmost_object)
        # adjust for green outline
        output_grid[center_row, center_col] = 4
        output_grid[center_row+1,center_col] = 4
        output_grid[center_row, center_col + 1] = 4
        output_grid[center_row+1, center_col + 1] = 4


    return output_grid