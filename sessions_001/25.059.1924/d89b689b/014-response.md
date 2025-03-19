# d89b689b • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Find all colored objects in the input grid. Ignore white pixels (the background).
2.  **Filter Objects:** From the found objects, ignore the azure colored block. Keep all the other objects which are all single pixels.
3.  **Sort and Arrange:** Sort the remaining objects by their color value, which is a single digit between 1 and 9 inclusive. Arrange the objects, sorted ascendingly, in a 2x2 block.
4. **Set position:** Place the 2x2 block at the coordinates occupied by the top left corner of the largest identified contiguous object (azure) in the input grid.
5.  **Output:** Create a new grid with the same dimensions as the input. Fill the entire grid with the background color (white, 0). Place the sorted 2x2 block, as in the step above.
"""

import numpy as np

def find_objects(grid):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, object_coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        object_coords.append((r, c))
        dfs(r + 1, c, color, object_coords)
        dfs(r - 1, c, color, object_coords)
        dfs(r, c + 1, color, object_coords)
        dfs(r, c - 1, color, object_coords)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                object_coords = []
                dfs(r, c, grid[r, c], object_coords)
                objects.append({
                    'color': grid[r, c],
                    'coords': object_coords,
                    'top_left': (r, c)
                })
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find all objects
    objects = find_objects(input_grid)

    # Find the azure object and its top-left corner
    azure_object = next((obj for obj in objects if obj['color'] == 8), None)
    azure_top_left = azure_object['top_left'] if azure_object else (0, 0)  # Default position

    # Filter out white and azure objects, and get single pixels
    filtered_objects = [obj for obj in objects if obj['color'] != 0 and obj['color'] != 8]

    # Sort remaining objects by color
    sorted_objects = sorted(filtered_objects, key=lambda x: x['color'])

    # Arrange into a 2x2 block
    for i, obj in enumerate(sorted_objects):
      row_offset = i // 2
      col_offset = i % 2
      output_grid[azure_top_left[0]+row_offset, azure_top_left[1]+col_offset] = obj['color']

    return output_grid
```
