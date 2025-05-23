# 1-3aa6fb7a • 004 • refine_code - CODE

---
```python
"""
1.  **Find Azure Lines:** Identify all contiguous lines of azure (8) colored pixels in the input grid. A line is defined as a sequence of adjacent azure pixels either horizontally or vertically.

2.  **Locate Insertion Point:** For each identified azure line:
    *   Find the left-most pixel in the line.

3.  **Insert Blue Pixel:**
    *   Insert a blue (1) pixel immediately to the right of this left-most pixel. Ensure the insertion stays within the grid boundaries.
"""

import numpy as np

def find_lines(grid, color):
    lines = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_line):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_line.append((r, c))

        # Explore adjacent cells
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_line)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_line = []
                dfs(r, c, current_line)
                if current_line:
                    lines.append(current_line)
    return lines

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    lines = find_lines(input_grid, 8) # Find all azure lines

    for line in lines:
        # Find the left-most pixel
        left_most = min(line, key=lambda p: p[1])

        # Calculate insertion point (to the right of the left-most pixel)
        insert_point = (left_most[0], left_most[1] + 1)

        # Insert blue pixel if within bounds
        if 0 <= insert_point[0] < output_grid.shape[0] and 0 <= insert_point[1] < output_grid.shape[1]:
            output_grid[insert_point] = 1

    return output_grid
```

