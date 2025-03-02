# ec883f72 • 028 • refine_coder

---
```python
"""
1. Identify all objects in the input grid. An object is a contiguous region of non-zero pixels of the same color.
2. For each object in the input grid:
    - If the object's color is 2, move it to the top of the output grid, aligning its leftmost column with its original position.
    - If the object's color is not 2, keep it in the same place.
3. All other pixels in the output grid should be 0.
"""

import numpy as np
from typing import List, Dict

def get_objects(grid: np.ndarray) -> List[Dict]:
    """Identifies distinct objects within a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                neighbors.append((nr, nc))
        return neighbors
    
    def bfs(start_row, start_col, color):
        queue = [(start_row, start_col)]
        visited[start_row, start_col] = True
        min_row, min_col = start_row, start_col
        max_row, max_col = start_row, start_col
        coords = []

        while queue:
            row, col = queue.pop(0)
            coords.append((row,col))
            min_row = min(min_row, row)
            min_col = min(min_col, col)
            max_row = max(max_row, row)
            max_col = max(max_col, col)

            for nr, nc in get_neighbors(row, col):
                if not visited[nr, nc] and grid[nr, nc] == color:
                    visited[nr, nc] = True
                    queue.append((nr, nc))
        return {
            "color": int(color),
            "min_row": int(min_row),
            "min_col": int(min_col),
            "max_row": int(max_row),
            "max_col": int(max_col),
            "coords": coords,
        }

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                objects.append(bfs(row, col, grid[row, col]))
    return objects

def transform(input_grid):
    # Initialize output grid.
    output_grid = np.zeros_like(input_grid)

    # Get all objects in input
    input_objects = get_objects(input_grid)

    # Iterate over input objects
    for obj in input_objects:
      if obj["color"] == 2:
        # move to top
        height = obj["max_row"] - obj["min_row"] + 1
        width = obj["max_col"] - obj["min_col"] + 1
        output_grid[0:height, obj["min_col"]:obj["min_col"]+width] = obj["color"]
      else:
        # keep at same place
        output_grid[obj["min_row"]:obj["max_row"]+1, obj["min_col"]:obj["max_col"]+1] = obj["color"]
        

    return output_grid
```
