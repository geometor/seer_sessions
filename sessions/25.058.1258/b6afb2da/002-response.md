# b6afb2da • 002 • example_2 • investigate_coder

---
```python
"""
The program detects filled grey rectangles and replaces each solid grey rectangle with an outlined, three-colored version, consisting of blue corners, yellow edges, and a red interior.
"""

import numpy as np

def find_rectangles(grid):
    # Find all contiguous regions of gray (color 5) pixels.
    rectangles = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_rectangle):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != 5:
            return

        visited[r, c] = True
        current_rectangle.append((r, c))

        dfs(r + 1, c, current_rectangle)
        dfs(r - 1, c, current_rectangle)
        dfs(r, c + 1, current_rectangle)
        dfs(r, c - 1, current_rectangle)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 5 and not visited[r, c]:
                current_rectangle = []
                dfs(r, c, current_rectangle)
                # Check if the current region forms a rectangle
                if current_rectangle:
                  min_r = min(p[0] for p in current_rectangle)
                  max_r = max(p[0] for p in current_rectangle)
                  min_c = min(p[1] for p in current_rectangle)
                  max_c = max(p[1] for p in current_rectangle)

                  if len(current_rectangle) == (max_r - min_r + 1) * (max_c - min_c + 1):
                      rectangles.append(current_rectangle)
    return rectangles

def transform(input_grid):
    # Initialize output grid with the same dimensions and background color (0).
    output_grid = np.zeros_like(input_grid)

    # Find all gray rectangles in the input grid.
    rectangles = find_rectangles(input_grid)

    # Process each rectangle.
    for rectangle in rectangles:
        # Find the boundaries of the rectangle.
        min_r = min(p[0] for p in rectangle)
        max_r = max(p[0] for p in rectangle)
        min_c = min(p[1] for p in rectangle)
        max_c = max(p[1] for p in rectangle)

        # Outline and fill the rectangle in the output grid.
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if (r == min_r or r == max_r) and (c == min_c or c == max_c):
                    # Corner pixels: blue (1)
                    output_grid[r, c] = 1
                elif r == min_r or r == max_r or c == min_c or c == max_c:
                    # Edge pixels (excluding corners): yellow (4)
                    output_grid[r, c] = 4
                else:
                    # Interior pixels: red (2)
                    output_grid[r, c] = 2

    return output_grid
```
