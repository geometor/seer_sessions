"""
1.  **Find Objects:** Identify all distinct objects within the input grid. An object is a group of orthogonally connected pixels of the same non-zero color.

2.  **Isolate and Pad:** For each identified object, determine its bounding box (the smallest rectangle that fully contains the object). Add a one-pixel border of white (0) around this bounding box.

3.  **Extract:** Extract each padded object as an individual grid.

4.  **Combine (Horizontal):** If multiple objects were extracted, combine them into a single output grid. Place the extracted objects side-by-side, horizontally, with a single column of white pixels (0) separating adjacent objects. If there is only one object extract, that is the solution.
"""

import numpy as np

def find_objects(grid):
    # Find coordinates of all non-zero pixels.
    grid = np.array(grid)
    non_zero_coords = np.argwhere(grid != 0)
    if non_zero_coords.size == 0:
        return []  # No objects found

    objects = []
    visited = set()

    def get_neighbors(coord):
        row, col = coord
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))  # Up
        if row < grid.shape[0] - 1:
            neighbors.append((row + 1, col))  # Down
        if col > 0:
            neighbors.append((row, col - 1))  # Left
        if col < grid.shape[1] - 1:
            neighbors.append((row, col + 1))  # Right
        return neighbors

    def dfs(coord, current_object):
        visited.add(tuple(coord))
        current_object.append(coord)
        for neighbor in get_neighbors(coord):
            if tuple(neighbor) not in visited and grid[neighbor[0], neighbor[1]] == grid[coord[0], coord[1]]:
                dfs(neighbor, current_object)


    for coord in non_zero_coords:
        if tuple(coord) not in visited:
            current_object = []
            dfs(coord, current_object)
            objects.append(current_object)

    return objects

def get_object_bounds(object_coords):
    min_row = np.min(object_coords[:, 0])
    max_row = np.max(object_coords[:, 0])
    min_col = np.min(object_coords[:, 1])
    max_col = np.max(object_coords[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # 1. Find Objects.
    objects = find_objects(input_grid)

    if not objects:
        return [[]]

    output_grids = []

    for obj in objects:
        obj_arr = np.array(obj)
       # 2. Isolate with Padding.
        min_row, max_row, min_col, max_col = get_object_bounds(obj_arr)

        padded_min_row = max(0, min_row - 1)
        padded_max_row = min(input_grid.shape[0], max_row + 2)
        padded_min_col = max(0, min_col - 1)
        padded_max_col = min(input_grid.shape[1], max_col + 2)

        # 3. Extract the padded region.
        extracted_grid = input_grid[padded_min_row:padded_max_row, padded_min_col:padded_max_col]
        output_grids.append(extracted_grid)

    # 4. Combine objects horizontally.
    if len(output_grids) == 1:
        return output_grids[0].tolist()
    else:
        # Determine max height and total width.
        max_height = max(grid.shape[0] for grid in output_grids)
        total_width = sum(grid.shape[1] for grid in output_grids) + len(output_grids) - 1  # +1 for padding between each.

        combined_grid = np.zeros((max_height + 2, total_width + 2), dtype=int)  # Add padding for top and bottom.

        current_x = 1 # Start at 1 to accommodate top padding
        for grid in output_grids:
            h, w = grid.shape
            combined_grid[1:h+1, current_x:current_x+w] = grid # Add padding to top and bottom
            current_x += w + 1  # Space between objects.

        return combined_grid.tolist()