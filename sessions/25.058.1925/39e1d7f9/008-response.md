# 39e1d7f9 • 008 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all rectangular objects within the grid. A rectangular object is a contiguous block of pixels of the same color.
2.  **Identify Containing Objects:** Iterate through all objects and find ones that contain other objects by the following rule: An object A is contained within object B when every pixel of object A has coordinates within the top left and bottom right coordinates of object B.
3. **Switch Colors of Containing/Contained Objects**
    *   Iterate through each pair of containing/contained objects.
    *   Change each pixel within the contained object to the initial color of the containing object
    *   Change each pixel of the containing object within its boundary to the initial color of the contained object.
"""

import numpy as np

def find_objects(grid):
    """Finds all rectangular objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                current_object = []
                color = grid[r, c]
                dfs(r, c, color, current_object)
                if current_object:
                    min_row = min(cell[0] for cell in current_object)
                    max_row = max(cell[0] for cell in current_object)
                    min_col = min(cell[1] for cell in current_object)
                    max_col = max(cell[1] for cell in current_object)
                    objects.append({
                        'top_left': (min_row, min_col),
                        'bottom_right': (max_row, max_col),
                        'color': color,
                        'pixels': current_object
                    })
    return objects

def is_contained(inner_object, outer_object):
    """Checks if inner_object is entirely contained within outer_object."""
    inner_top, inner_left = inner_object['top_left']
    inner_bottom, inner_right = inner_object['bottom_right']
    outer_top, outer_left = outer_object['top_left']
    outer_bottom, outer_right = outer_object['bottom_right']

    return (outer_top <= inner_top and inner_bottom <= outer_bottom and
            outer_left <= inner_left and inner_right <= outer_right)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find objects
    objects = find_objects(input_grid)

    # Iterate through all pairs of objects to check for containment
    for outer_obj in objects:
        for inner_obj in objects:
            if outer_obj != inner_obj:  # Ensure we're not comparing the same object
                if is_contained(inner_obj, outer_obj):
                    # Switch colors for contained/containing objects
                    outer_color = outer_obj['color']
                    inner_color = inner_obj['color']

                    # change contained object pixels
                    for r, c in inner_obj['pixels']:
                        output_grid[r, c] = outer_color
                    # change containing object pixels
                    for r, c in outer_obj['pixels']:
                        output_grid[r, c] = inner_color

    return output_grid
```
