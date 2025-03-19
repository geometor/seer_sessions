# 7b6016b9 • 008 • refine_coder

---
```python
"""
1.  **Identify Background:** Determine the background color by reading the pixel
    value at coordinate (0, 0) of the input grid.
2.  **Replace Background:** Change all pixels in the grid that match the
    background color to green (3).
3.  **Preserve Outline:** Ensure that all pixels with the color azure (8) remain
    unchanged throughout the process.
4.  **Identify Interior:** Perform a constrained flood fill starting from all
    edge pixels of the grid.  The constraint is that the flood fill cannot pass
    through any azure (8) pixel.  Any pixel *not* reached by this constrained
    flood fill is considered part of the interior.
5.  **Fill Interior:** Change all interior pixels (identified in step 4) to red
    (2).
"""

import numpy as np

def constrained_flood_fill(grid, start_row, start_col, outline_color, visited):
    """
    Performs a constrained flood fill, avoiding the outline color.
    Marks visited cells in the 'visited' array.
    """
    rows, cols = grid.shape
    if (start_row < 0 or start_row >= rows or
        start_col < 0 or start_col >= cols or
        visited[start_row, start_col] or
        grid[start_row, start_col] == outline_color):
        return

    visited[start_row, start_col] = True
    queue = [(start_row, start_col)]

    while queue:
        row, col = queue.pop(0)

        neighbors = [
            (row - 1, col),  # Up
            (row + 1, col),  # Down
            (row, col - 1),  # Left
            (row, col + 1)   # Right
        ]

        for n_row, n_col in neighbors:
            if (0 <= n_row < rows and 0 <= n_col < cols and
                not visited[n_row, n_col] and
                grid[n_row, n_col] != outline_color):
                visited[n_row, n_col] = True
                queue.append((n_row, n_col))

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify Background
    background_color = input_grid[0, 0]

    # 2. Replace Background
    output_grid[output_grid == background_color] = 3

    # 3. Preserve Outline (already done by copying)

    # 4. Identify Interior
    visited = np.zeros((rows, cols), dtype=bool)
    outline_color = 8  # Azure

    # Constrained flood fill from all edges
    for r in range(rows):
        constrained_flood_fill(output_grid, r, 0, outline_color, visited)
        constrained_flood_fill(output_grid, r, cols - 1, outline_color, visited)
    for c in range(cols):
        constrained_flood_fill(output_grid, 0, c, outline_color, visited)
        constrained_flood_fill(output_grid, rows - 1, c, outline_color, visited)

    # 5. Fill Interior
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and output_grid[r, c] != outline_color:
                output_grid[r, c] = 2

    return output_grid
```
