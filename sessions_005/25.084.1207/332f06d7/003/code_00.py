"""
Transformation Rule:
1. Identify the single contiguous White object (W) and its dimensions.
2. Identify the single contiguous Red object (R) and its dimensions.
3. Identify all contiguous Blue objects (B_list) and their dimensions.
4. Create an output grid, initially a copy of the input.
5. Change the pixels of W to Blue in the output grid.
6. Check if any Blue object in B_list has dimensions matching R's dimensions.
7. If a match exists: Change the pixels of R to White in the output grid.
8. If no match exists: Find the first Blue object (B_match_W) in B_list with dimensions matching W's dimensions. If found, change the pixels of B_match_W to White in the output grid.
9. Return the modified output grid.
"""

import numpy as np
from collections import deque

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (a set of (row, col) tuples) and
              'dims' (a tuple of (height, width)). Returns an empty list if no
              objects of the specified color are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start BFS to find a new object
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-directional: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Calculate bounding box dimensions
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                objects.append({'coords': obj_coords, 'dims': (height, width)})

    return objects

def transform(input_grid):
    """
    Applies the transformation rule based on White, Red, and Blue object dimensions.
    """
    # 4. Create an output grid, initially a copy of the input.
    output_grid = np.copy(input_grid)

    # 1. Identify the single white_object (W).
    white_objects = find_objects(input_grid, 0)
    if not white_objects:
        return output_grid # Should not happen based on examples, but safe check
    white_object = white_objects[0] # Assume exactly one
    white_coords = white_object['coords']
    white_dims = white_object['dims']

    # 2. Identify the single red_object (R).
    red_objects = find_objects(input_grid, 2)
    if not red_objects:
        return output_grid # Should not happen based on examples
    red_object = red_objects[0] # Assume exactly one
    red_coords = red_object['coords']
    red_dims = red_object['dims']

    # 3. Identify all blue_objects (B_list).
    blue_objects = find_objects(input_grid, 1)

    # 5. Change the pixels of W to Blue in the output grid.
    for r, c in white_coords:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
             output_grid[r, c] = 1

    # 6. Check if any Blue object in B_list has dimensions matching R's dimensions.
    found_blue_matching_red = False
    for blue_obj in blue_objects:
        if blue_obj['dims'] == red_dims:
            found_blue_matching_red = True
            break

    # 7. If a match exists: Change the pixels of R to White in the output grid.
    if found_blue_matching_red:
        for r, c in red_coords:
             if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                output_grid[r, c] = 0
    # 8. If no match exists: Find the first Blue object (B_match_W) matching W's dimensions.
    else:
        found_blue_matching_white = None
        for blue_obj in blue_objects:
            if blue_obj['dims'] == white_dims:
                found_blue_matching_white = blue_obj
                break # Found the first match

        # If found, change the pixels of B_match_W to White in the output grid.
        if found_blue_matching_white:
            for r, c in found_blue_matching_white['coords']:
                 if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                    output_grid[r, c] = 0

    # 9. Return the modified output grid.
    return output_grid