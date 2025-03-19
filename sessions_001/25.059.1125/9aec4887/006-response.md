# 9aec4887 • 006 • refine_coder

---
```python
"""
Transforms a larger grid into a smaller one by representing specific colored regions.

1.  **Identify Objects:** Locate all contiguous regions (objects) of azure (8), yellow (4), red (2), blue (1), and green (3) within the input grid.

2.  **Create Output Grid:** Create a 6x6 output grid filled with zeros.

3.  **Place Yellow:** Place a horizontal line of yellow (4) pixels across the top row of the output grid, leaving one empty cell (0) at each end.

4.  **Outline Azure:** Trace the outline of the azure (8) object in the input grid. Start from the top-leftmost pixel of the azure object. Proceed clockwise around the *outer* boundary of the azure shape, placing an 8 in the corresponding cell in the output grid. *Do not* trace internal connections within the azure shape. *Skip* any azure pixels that do not form part of the outer boundary.

5.  **Place Red:** Place a vertical line of red (2) pixels in the leftmost column of the output grid. The red line should extend from the second row to the second-to-last row.

6.  **Place Blue:** Place a vertical line of blue (1) pixels in the rightmost column of the output grid. The blue line should extend from the second row to the second-to-last row.

7.  **Place Green:** Place a horizontal line of green (3) pixels across the bottom row of the output grid, leaving one empty cell (0) at each end.

8.  **Fill Remaining:** Ensure that the corner cells and any other cells not occupied by the placed objects are filled with zeros (0).
"""

import numpy as np

def find_objects(grid, color):
    """Finds coordinates of objects with a specific color."""
    coords = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                coords.append((i, j))
    return coords

def trace_outline(grid, start):
    """Traces the outline of an object starting from a given point."""
    outline = []
    visited = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Clockwise: Right, Down, Left, Up

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y):
        if (x, y) in visited or not is_valid(x, y) or grid[x, y] != 8:
            return

        visited.add((x, y))

        # Check neighbors to determine if it's an outline pixel
        is_outline = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not is_valid(nx, ny) or grid[nx, ny] != 8:
                is_outline = True
                break

        if is_outline:
            outline.append((x, y))
            
        # Continue DFS in clockwise order
        for dx, dy in directions:
            dfs(x + dx, y + dy)

    dfs(start[0], start[1])
    return outline

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.zeros((6, 6), dtype=int)

    # 1. Identify Objects
    azure_coords = find_objects(input_grid, 8)
    yellow_coords = find_objects(input_grid, 4)
    red_coords = find_objects(input_grid, 2)
    blue_coords = find_objects(input_grid, 1)
    green_coords = find_objects(input_grid, 3)

    # 2. Create Output Grid (already done)

    # 3. Place Yellow
    if yellow_coords:
        output_grid[0, 1:5] = 4

    # 4. Outline Azure
    if azure_coords:
        top_left_azure = min(azure_coords, key=lambda t: (t[0], t[1]))
        outline = trace_outline(input_grid, top_left_azure)

        # Scale and shift outline coordinates to fit within the 6x6 grid
        if outline:
          min_row = min(outline, key=lambda t:t[0])[0]
          min_col = min(outline, key=lambda t:t[1])[1]

          for r, c in outline:
            # simple scaling for now
            out_r = int((r-min_row) * (4 / (input_grid.shape[0] if input_grid.shape[0] > 0 else 1)) ) + 1
            out_c = int((c - min_col) * (4 / (input_grid.shape[1] if input_grid.shape[1] > 0 else 1)) ) + 1

            if 0 < out_r < 5 and 0 < out_c < 5:
              output_grid[out_r,out_c] = 8

    # 5. Place Red
    if red_coords:
        output_grid[1:5, 0] = 2

    # 6. Place Blue
    if blue_coords:
        output_grid[1:5, 5] = 1

    # 7. Place Green
    if green_coords:
        output_grid[5, 1:5] = 3

    # 8. Fill Remaining (already done by initialization)

    return output_grid
```
