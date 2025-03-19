# e21d9049 • 002 • example_2 • investigate_coder

---
```python
"""
The transformation rule identifies a connected object of non-zero pixels in the input grid.
It then replicates this object horizontally across a specific row in the output grid.
Also extracts a vertical bar of the shape and creates the bar with corresponding x coordinates in the output grid.
"""

import numpy as np

def find_object(grid):
    """Finds the bounding box of the largest connected non-zero object in the grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_object_coords = []

    def dfs(r, c, current_object):
        """Depth-first search to find connected components."""
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or grid[r, c] == 0):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                if len(current_object) > len(max_object_coords):
                    max_object_coords = current_object

    return max_object_coords

def extract_vertical_bar(grid, object_coords):
    """ Extracts the vertical bar from object """
    if not object_coords:
        return []
    
    min_r = min(r for r, _ in object_coords)
    max_r = max(r for r, _ in object_coords)
    min_c = min(c for _, c in object_coords)
    max_c = max(c for _, c in object_coords)
    
    center_c = (min_c + max_c) // 2
    
    vertical_bar_coords = []
        
    for r in range(grid.shape[0]):
        if grid[r,center_c] !=0:
            vertical_bar_coords.append((r,center_c))

    return vertical_bar_coords

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)  # Ensure it's a NumPy array
    output_grid = np.zeros_like(input_grid)
    object_coords = find_object(input_grid)

    # Find the vertical bar and copy to the output grid.
    vertical_bar = extract_vertical_bar(input_grid, object_coords)
    for r, c in vertical_bar:
        output_grid[r,c] = input_grid[r,c]

    if not object_coords:
        return output_grid

    # Determine bounding box of the object.
    min_r = min(r for r, _ in object_coords)
    max_r = max(r for r, _ in object_coords)
    min_c = min(c for _, c in object_coords)
    max_c = max(c for _, c in object_coords)
    
    center_r = (min_r + max_r) // 2


    # Replicate the object horizontally.
    object_width = max_c - min_c + 1
    for i in range(output_grid.shape[1] // object_width ):
        for r, c in object_coords:
            new_c = min_c + (i * object_width) + (c - min_c)
            if 0 <= new_c < output_grid.shape[1]:
                output_grid[center_r, new_c] = input_grid[r, c]

    return output_grid
```
