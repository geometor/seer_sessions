# 27a28665 • 034 • refine_coder

---
```python
"""
1.  **Identify the Solid Shape:** Examine the input grid and find the largest contiguous "interior" region of pixels that all share the same color. This means excluding any pixels that form a border (adjacent to pixels of a different color).
2.  **Determine Output Color:** Note the color of the solid shape identified in step 1.
3.  **Create Output:** Create a 1x1 output grid. The single pixel in this grid should have the color determined in step 2.

In short: Find the largest interior solid shape and output its color as a 1x1 grid.
"""

import numpy as np

def _is_border_pixel(grid, row, col):
    """Checks if a pixel is on the border of a shape."""
    rows, cols = grid.shape
    color = grid[row, col]

    # Check adjacent pixels (up, down, left, right)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row, new_col] != color:
                return True
    return False

def _find_solid_shape_color(grid):
    """Finds the color of the largest solid shape, excluding border pixels."""
    rows, cols = grid.shape
    color_counts = {}
    visited = set()

    def _dfs(row, col, color):
        """Depth-first search to find contiguous regions."""
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color or _is_border_pixel(grid,row,col):
            return 0

        visited.add((row, col))
        count = 1
        count += _dfs(row + 1, col, color)
        count += _dfs(row - 1, col, color)
        count += _dfs(row, col + 1, color)
        count += _dfs(row, col - 1, color)
        return count

    for r in range(rows):
        for c in range(cols):
            if not _is_border_pixel(grid, r, c):  # Start DFS from non-border
                color = grid[r,c]
                if (r,c) not in visited:
                    count = _dfs(r, c, color)
                    if color not in color_counts:
                        color_counts[color] = 0
                    color_counts[color] += count

    # find largest color
    if not color_counts:
        return None

    largest_color = max(color_counts, key=color_counts.get)
    return largest_color

def transform(input_grid):
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # Find solid shape color
    solid_shape_color = _find_solid_shape_color(input_array)

    # Create a 1x1 output grid with solid shape color
    if solid_shape_color is not None:
        output_grid = np.array([[solid_shape_color]])
    else:
        # handle case where no solid shape
        output_grid = np.array([[0]])

    return output_grid.tolist()
```
