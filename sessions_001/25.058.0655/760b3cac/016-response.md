# 760b3cac • 016 • refine_coder

---
```python
"""
The transformation identifies objects in the input grid and replicates them in the output grid with specific shifts. The yellow (4) object remains in its original position. The azure (8) object is replicated twice: once shifted one position to the left, and again shifted two positions to the left, with a slight vertical shift adjustment. The output is constructed by combining these transformations.
"""

import numpy as np

def find_objects(grid):
    # Find contiguous blocks of non-zero pixels
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append([r, c])
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append((grid[r, c], obj))  # Store color and object
    return objects

def transform(input_grid):
    # Initialize output grid as a zero-filled grid
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    for color, obj in objects:
        if color == 4:  # Yellow object
            # Keep yellow object unchanged
            for r, c in obj:
                output_grid[r, c] = color
        elif color == 8:  # Azure object
            for r, c in obj:
                # Shift left by 1
                if c - 1 >= 0:
                    output_grid[r, c - 1] = color
                # Shift left by 2 and adjust vertically
                if c - 2 >= 0:
                    row_offset = 0
                    if len(obj) > 1: # Check if it's a vertical line
                        row_diffs = [obj[i+1][0] - obj[i][0] for i in range(len(obj) - 1)]
                        if all(diff == 1 for diff in row_diffs) and obj[0][1] -2 > 0 :
                            #object on edges, use different logic
                            row_offset = 0 if c!= obj[0][1] else 1
                        else: #horizontal cases, including the single pixel
                            row_offset = 0
                    adjusted_r = r + row_offset
                    if adjusted_r < output_grid.shape[0]:                         
                        output_grid[adjusted_r, c - 2] = color
    return output_grid
```
