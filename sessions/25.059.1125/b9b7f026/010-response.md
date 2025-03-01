# b9b7f026 • 010 • example_2 • investigate_coder

---
```python
"""
The program detects the gray rectangle and returns its color, which in the integer / color mapping is 5.
"""

import numpy as np

def find_rectangles(grid):
    """
    Finds all distinct rectangular regions in a grid.
    """
    rectangles = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_rectangle):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_rectangle.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_rectangle)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                current_rectangle = []
                dfs(r, c, color, current_rectangle)
                if current_rectangle:
                    # Check if it forms a rectangle
                    min_r = min(x[0] for x in current_rectangle)
                    max_r = max(x[0] for x in current_rectangle)
                    min_c = min(x[1] for x in current_rectangle)
                    max_c = max(x[1] for x in current_rectangle)
                    if len(current_rectangle) == (max_r - min_r + 1) * (max_c - min_c + 1):
                        rectangles.append((color, current_rectangle))
    return rectangles

def transform(input_grid):
    """
    Finds the gray rectangle in the input grid and returns its color value (5).
    """
    # Find all rectangles in the grid.
    rectangles = find_rectangles(np.array(input_grid))

    # Find the gray rectangle.
    gray_rectangle = None
    for color, coords in rectangles:
        if color == 5:
            gray_rectangle = color
            break

    # Return the color value of gray (5)
    return np.array([[gray_rectangle]])
```
