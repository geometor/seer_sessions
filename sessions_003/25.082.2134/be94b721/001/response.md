```python
"""
1.  **Identify Objects:** Scan the input grid to identify all distinct objects. An object is a group of one or more contiguous pixels of the same color, excluding color 0 (white, which is the background).
2.  **Select Target Object:** From the identified objects, select the object that is farthest to the right and bottom, using the last occurance of that color.
3.  **Determine Bounding Box:** Find the minimum and maximum row and column indices of the selected object. This defines the bounding box.
4.  **Extract Object:** Create a new grid with dimensions equal to the bounding box.
5.  **Copy Pixels:** Copy the pixels of the selected object from the input grid to the corresponding positions in the output grid, maintaining their original color.
6. output grid will be filled with selected object, with cells outside the contiguous block set to 0.
"""

import numpy as np

def find_objects(grid):
    """Finds all distinct objects in a grid."""
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj_id):
        """Depth-first search to find contiguous pixels of the same color."""
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                (r, c) in visited or grid[r, c] != color):
            return []

        visited.add((r, c))
        coords = [(r, c)]

        coords.extend(dfs(r + 1, c, color, obj_id))
        coords.extend(dfs(r - 1, c, color, obj_id))
        coords.extend(dfs(r, c + 1, color, obj_id))
        coords.extend(dfs(r, c - 1, color, obj_id))
        return coords

    obj_count = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                color = grid[r, c]
                obj_id = obj_count + 1
                objects[obj_id] = {
                    'color': color,
                    'coords': dfs(r, c, color, obj_id)
                }
                obj_count += 1

    return objects

def select_target_object(objects):
    """Selects the object that is farthest to the right and bottom."""
    if not objects:
      return None

    target_object = None
    max_row_sum_col = -1

    for obj_id, obj_data in objects.items():
        # prioritize by last occurance, sum of row + col
        row_sum_col = 0
        for r,c in obj_data['coords']:
            row_sum_col = max(row_sum_col, r + c) # sum for last effect
        if row_sum_col >= max_row_sum_col:
            max_row_sum_col = row_sum_col
            target_object = obj_data
    return target_object

def get_bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    min_row = min(r for r, _ in coords)
    max_row = max(r for r, _ in coords)
    min_col = min(c for _, c in coords)
    max_col = max(c for _, c in coords)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # convert to numpy for convenience
    grid = np.array(input_grid)

    # find objects
    objects = find_objects(grid)

    # select target object
    target_object = select_target_object(objects)

    # handle edge case
    if target_object is None:
      return []

    # get bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(target_object['coords'])

    # init output grid
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    # copy object pixels to output grid
    for r, c in target_object['coords']:
        output_grid[r - min_row, c - min_col] = target_object['color']

    return output_grid.tolist()
```