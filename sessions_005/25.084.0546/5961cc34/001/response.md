```python
"""
1.  **Identify Input Signals:** Locate all contiguous blocks of pixels that are blue (1), green (3) or yellow(4).

2. **Identify Targets**: Locate all red (2) pixels

3. **Background**: Ignore all azure (8) pixels.

4. **Transformation**:
    - Iterate through each object found in the original grid which are a color other than azure(8) or red(2)
    - Create new object(s) where:
      - all pixels of the original object are changed to color red(2)

5.  **Output:** Construct the output grid with the transformed red objects and the existing red pixels. All other pixels are filled with azure (8).
"""

import numpy as np

def find_objects(grid):
    # Find contiguous regions of the same color, excluding azure (8)
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, obj_coords):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col] and grid[row, col] != 8:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if obj_coords:  # Ensure the object is not empty
                    objects.append((color, obj_coords))
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.full(input_grid.shape, 8, dtype=int)

    # Find objects, excluding azure (8)
    objects = find_objects(input_grid)

    # change output pixels 
    for color, coords in objects:
        if color != 2:  # If the object is not already red
            for row, col in coords:
               output_grid[row, col] = 2  # convert the object to color red(2)
        else: # original red(2) objects
            for row, col in coords:
               output_grid[row, col] = 2  # keep it red


    return output_grid
```