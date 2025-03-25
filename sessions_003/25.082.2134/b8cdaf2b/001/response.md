```python
"""
1.  **Identify Objects:** Find all distinct horizontal objects across bottom of the grid.
2.  **Select Topmost Object:** From the bottom objects select the one appearing highest in the grid..
3.  **Determine Mirror Axis:** Calculate the vertical center (midpoint) of the selected object's bounding box.
4. **Partial Mirroring**: For every pixel inside selected object, reflect about center line and find target pixel.
5. **Copy colors:** Copy target pixel color from source object, but from above/below the source object.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append(current_object)
    return objects

def find_bottom_objects(grid):
    """Identifies distinct horizontal objects at the bottom of the grid."""
    objects = find_objects(grid)
    bottom_objects = []
    bottom_row = grid.shape[0] - 1

    for obj in objects:
        # Check if the object is on the bottom row and horizontal
        rows = [r for r, _ in obj]
        cols = [c for _, c in obj]
        if max(rows) == bottom_row and len(set(rows)) == 1:
                bottom_objects.append(obj)


    return bottom_objects

def select_topmost_object(objects):
    """Selects the topmost object from a list of bottom objects."""
    if not objects:
      return []
    # Find the object with the minimum row value (highest up)
    topmost_object = min(objects, key=lambda obj: min(r for r, _ in obj))

    #remove all pixels not on same row
    row = min(r for r,_ in topmost_object)
    topmost_object = [(r,c) for (r,c) in topmost_object if r == row]

    return topmost_object


def transform(input_grid):
    """Transforms the input grid according to the mirroring rule."""
    grid = np.array(input_grid)  # Work with a NumPy array
    output_grid = np.copy(grid)
    bottom_objects = find_bottom_objects(grid)

    topmost = select_topmost_object(bottom_objects)
    if len(topmost) == 0:
        return output_grid

    #find center
    cols = [c for _,c in topmost]
    center = (min(cols) + max(cols))/2

    for r,c in topmost:
        #mirror
        delta = c - center
        
        target_c = int(center - delta)

        #find source color location
        source_r = r - 1 if delta > 0 else r + 1
      
        if 0 <= source_r < grid.shape[0] and 0 <= target_c < grid.shape[1]:
            output_grid[r,target_c] = grid[source_r, c]
        
    return output_grid.tolist()
```