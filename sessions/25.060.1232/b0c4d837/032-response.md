# b0c4d837 • 032 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all distinct objects in the input grid. An object is a contiguous region of non-zero pixels of the same color.
2.  **Find Top-Left Object:** Determine the object whose top-left corner is closest to the top-left corner of the grid (0,0).  Prioritize rows, then columns.
3.  **Create Output Grid:** Create a 3x3 output grid filled with zeros.
4.  **Place Color:** Place the color of the identified top-left object into the top-left cell (position [0, 0]) of the output grid.
"""

import numpy as np

def get_object_properties(grid):
    """
    Identifies contiguous objects within a grid and returns their properties.
    An object is a set of connected pixels.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        # Explore adjacent cells (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r][c]
                if color != 0:  # Ignore background
                    current_object = []
                    dfs(r, c, color, current_object)
                    if current_object:
                        min_r = min(pos[0] for pos in current_object)
                        max_r = max(pos[0] for pos in current_object)
                        min_c = min(pos[1] for pos in current_object)
                        max_c = max(pos[1] for pos in current_object)
                        objects.append({
                            "color": color,
                            "min_row": min_r,
                            "max_row": max_r,
                            "min_col": min_c,
                            "max_col": max_c,
                            "size": len(current_object),
                            "shape": (max_r - min_r + 1, max_c - min_c + 1),
                            "positions": current_object,
                        })

    return objects

def transform(input_grid):
    # Create a 3x3 output grid filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Get object properties
    objects = get_object_properties(input_grid)

    # Find the object with the top-left corner closest to (0, 0)
    if objects:  # Check if there are any objects
        top_left_object = min(objects, key=lambda obj: (obj["min_row"], obj["min_col"]))

        # Place the color of the top-left object in the top-left corner of the output grid.
        output_grid[0, 0] = top_left_object["color"]

    return output_grid
```
