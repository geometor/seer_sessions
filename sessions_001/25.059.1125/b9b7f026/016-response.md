# b9b7f026 • 016 • refine_coder

---
```python
"""
Counts the number of rectangles in the input grid that contain a "hole" (an inner region of a different color).
"""

import numpy as np

def find_rectangles(grid):
    """
    Finds all rectangles of uniform color in a grid.
    Returns a list of tuples, where each tuple represents a rectangle:
    ((row_start, col_start), (row_end, col_end), color)
    """
    rectangles = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, min_r, min_c, max_r, max_c):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return min_r, min_c, max_r, max_c

        visited[r, c] = True
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)

        # Check neighbors
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            min_r, min_c, max_r, max_c = dfs(nr, nc, color, min_r, min_c, max_r, max_c)

        return min_r, min_c, max_r, max_c

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                if color != 0:  # Ignore background
                    min_r, min_c, max_r, max_c = dfs(r, c, color, r, c, r, c)
                    rectangles.append(((min_r, min_c), (max_r, max_c), color))
                    # Reset visited flags within the rectangle after processing
                    for i in range(min_r, max_r + 1):
                      for j in range(min_c, max_c + 1):
                        visited[i,j] = False

    return rectangles

def has_hole(grid, rectangle):
    """
    Checks if a rectangle contains a "hole" (an inner region of a different color).
    """
    (r_start, c_start), (r_end, c_end), color = rectangle
    for r in range(r_start + 1, r_end):
        for c in range(c_start + 1, c_end):
            if grid[r, c] != color:
                return True
    return False

def transform(input_grid):
    # Find all rectangles in the input grid
    rectangles = find_rectangles(np.array(input_grid))

    # Count the number of rectangles with holes
    count = 0
    for rect in rectangles:
        if has_hole(np.array(input_grid), rect):
            count += 1

    # Output the count as a 1x1 grid
    output_grid = np.array([[count]])
    return output_grid
```
