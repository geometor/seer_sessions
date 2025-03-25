```python
"""
1.  **Identify Objects:** Find all contiguous regions (objects) of non-zero colored pixels in the input grid. Each object has a color and a size (number of pixels).
2. **Target Color and Object:**
    -   In example 1 and 4 the output color is 2
    -   In example 2 the output color is 4
    -   In example 3 the output color is 8.
    -   Find the largest object for each of these colors
3.  **Select Largest Object:** From previous step select largest object
4.  **Create Output Grid:** Create a new grid with the dimensions of the bounding box of the selected object.
5.  **Copy Pixels:** Copy the pixels of the selected object from the input grid to the output grid, preserving its color. Fill the remaining (empty) cells in the output grid with 0 (background color).
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
                    'coords': dfs(r, c, color, obj_id),
                    'size': len(dfs(r,c,color,obj_id))
                }
                obj_count += 1

    return objects

def get_bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    min_row = min(r for r, _ in coords)
    max_row = max(r for r, _ in coords)
    min_col = min(c for _, c in coords)
    max_col = max(c for _, c in coords)
    return min_row, max_row, min_col, max_col

def select_largest_object(objects, colors):
    """
    Select largest object among specified colors
    """

    max_size = -1
    target_object = None

    for obj_id, obj_data in objects.items():
        if obj_data['color'] in colors:
            if obj_data['size'] > max_size:
                max_size = obj_data['size']
                target_object = obj_data
    return target_object
    

def transform(input_grid):
    # convert to numpy for convenience
    grid = np.array(input_grid)

    # find objects
    objects = find_objects(grid)

    # target colors
    target_colors = [2,4,8]

    # select largest object among target colors
    target_object = select_largest_object(objects, target_colors)
    
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