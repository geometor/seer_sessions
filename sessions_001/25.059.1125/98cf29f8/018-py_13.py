"""
1.  Identify the "red top" object: Find the contiguous region of red pixels. This serves as the anchor or reference.
2.  Identify all objects below the "red top": Find all other contiguous colored objects (non-white pixels) that are located *below* the lowest row of the "red top".
3.  Move objects: Move all the objects identified in step 2 upwards. The top row of the combined set of these moved objects should be placed directly below the bottom row of the red top object, making them vertically adjacent. The relative horizontal positions and shapes of all moved objects must be preserved. The red object should not move.
"""

import numpy as np

def find_objects(grid):
    """Identifies distinct objects based on color contiguity."""
    objects = {}
    visited = set()

    def dfs(row, col, color, obj_id):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        objects[obj_id].append((row, col))
        dfs(row + 1, col, color, obj_id)
        dfs(row - 1, col, color, obj_id)
        dfs(row, col + 1, color, obj_id)
        dfs(row, col - 1, color, obj_id)

    obj_id = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                objects[obj_id] = []
                dfs(row, col, color, obj_id)
                obj_id += 1
    return objects

def get_object_bounds(object_pixels):
    """Calculates the bounding box of an object."""
    rows = [p[0] for p in object_pixels]
    cols = [p[1] for p in object_pixels]
    return min(rows), max(rows), min(cols), max(cols)


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # find red_top object
    red_top = None
    for obj_id, pixels in objects.items():
        if input_grid[pixels[0]] == 2:  # Check color of the first pixel
            red_top = obj_id
            break
    
    if red_top is None:
        return output_grid # no red object found

    red_min_row, red_max_row, _, _ = get_object_bounds(objects[red_top])

    # identify objects to move
    objects_to_move = []
    for obj_id, pixels in objects.items():
        if obj_id != red_top:
            obj_min_row, _, _, _ = get_object_bounds(pixels)
            if obj_min_row > red_max_row:
                objects_to_move.append(obj_id)

    # calculate move delta
    if not objects_to_move:
      return output_grid
   
    all_moving_pixels = []
    for obj_id in objects_to_move:
      all_moving_pixels.extend(objects[obj_id])

    move_min_row, _, _, _ = get_object_bounds(all_moving_pixels)
    move_delta = move_min_row - (red_max_row + 1)

    # clear original object positions
    for obj_id in objects_to_move:
      for r, c in objects[obj_id]:
        output_grid[r,c] = 0

    # move and change output pixels
    for obj_id in objects_to_move:
        for r, c in objects[obj_id]:
            output_grid[r - move_delta, c] = input_grid[r, c]

    return output_grid