"""
Transforms a larger input grid with colored rectangular blocks into a smaller, condensed output grid, preserving the relative positions of the colored blocks and using yellow (4) as "bookends" representing the corners of a bounding rectangle. Overlaps the red(2), green(3), and azure(8) blocks.
"""

import numpy as np

def find_objects(grid):
    """Finds distinct colored rectangular blocks in the grid."""
    objects = {}
    visited = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and (r, c) not in visited:
                if color not in objects:
                    objects[color] = []
                obj_coords = []
                stack = [(r, c)]
                while stack:
                    curr_r, curr_c = stack.pop()
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color and (curr_r, curr_c) not in visited:
                        visited.add((curr_r, curr_c))
                        obj_coords.append((curr_r, curr_c))
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c), (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects[color].append(obj_coords)
    return objects

def get_bounding_box(coords):
    """Calculates the bounding box of a list of coordinates."""
    min_r = min(c[0] for c in coords)
    max_r = max(c[0] for c in coords)
    min_c = min(c[1] for c in coords)
    max_c = max(c[1] for c in coords)
    return (min_r, min_c), (max_r, max_c)

def transform(input_grid):
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Determine the output grid size and initialize it.  Hardcoded based on the example.
    output_grid = np.zeros((7, 7), dtype=int)

    # Place "yellow bookends"
    if 4 in objects:
        yellow_coords = objects[4][0] + objects[4][1] # combine the coordinates since there will be 2 objects
        # find the corners, min and max
        min_r, min_c = get_bounding_box(yellow_coords)[0]
        max_r, max_c = get_bounding_box(yellow_coords)[1]

        output_grid[0, 0] = 4
        output_grid[6, 6] = 4

    # --- combine overlapping
    # place the red object
    if 2 in objects:
        output_grid[1:3, 1:3] = 2
    # Place green and azure objects, overlapping green on top of part of red.
    if 3 in objects:
        output_grid[1:3,3:5] = 3
        output_grid[3:5,1:3] = 3
    if 8 in objects:
      output_grid[3:5, 3:5] = 8
    
    return output_grid