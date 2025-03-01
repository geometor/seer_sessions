# 5521c0d9 • 006 • refine_coder

---
```python
"""
Moves each colored rectangular block to the top of the grid, preserving their original order of appearance (top-to-bottom, then left-to-right).
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct colored rectangular blocks in the grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A list of (color, (min_row, max_row, min_col, max_col)) tuples,
        ordered by their appearance in the grid (top-to-bottom, left-to-right).
    """
    objects = []
    visited = set()

    def dfs(row, col, color, min_row, max_row, min_col, max_col):
        if (row, col) in visited or row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or grid[row, col] != color:
            return min_row, max_row, min_col, max_col

        visited.add((row, col))
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

        min_row, max_row, min_col, max_col = dfs(row + 1, col, color, min_row, max_row, min_col, max_col)
        min_row, max_row, min_col, max_col = dfs(row - 1, col, color, min_row, max_row, min_col, max_col)
        min_row, max_row, min_col, max_col = dfs(row, col + 1, color, min_row, max_row, min_col, max_col)
        min_row, max_row, min_col, max_col = dfs(row, col - 1, color, min_row, max_row, min_col, max_col)
        return min_row, max_row, min_col, max_col

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                min_row, max_row, min_col, max_col = dfs(row, col, color, row, row, col, col)
                objects.append((color, (min_row, max_row, min_col, max_col)))

    return objects
def transform(input_grid):
    """
    Transforms the input grid by moving each colored rectangle to the top,
    preserving their original order.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Calculate total width of stacked objects
    total_width = 0
    for color, (min_row, max_row, min_col, max_col) in objects:
      total_width += max_col - min_col + 1

    # determine output width
    output_width = max(input_grid.shape[1], total_width)
    output_grid = np.zeros((input_grid.shape[0], output_width), dtype=int)


    current_row = 0
    current_col = 0
    for color, (min_row, max_row, min_col, max_col) in objects:
        # Calculate height and width of the object
        height = max_row - min_row + 1
        width = max_col - min_col + 1

        # Move the object to the top
        for i in range(height):
            for j in range(width):
                output_grid[current_row + i, current_col + j] = color
        current_row += height
        current_col = 0 # Reset column to 0 for top align.
        current_row = 0 # Reset row to 0.

    return output_grid
```
