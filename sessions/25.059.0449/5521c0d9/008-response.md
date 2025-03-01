# 5521c0d9 • 008 • refine_coder

---
```python
"""
Moves each colored rectangular block to the top of the grid, preserving their original order of appearance (top-to-bottom, then left-to-right), and arranging them horizontally.
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
    preserving their original order, and arranging them horizontally.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)

    # Determine output grid dimensions
    max_height = 0
    total_width = 0
    for color, (min_row, max_row, min_col, max_col) in objects:
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        max_height = max(max_height, height)
        total_width += width

    # Create output grid
    output_grid = np.zeros((max_height, total_width), dtype=int)

    # Place objects
    current_col = 0
    for color, (min_row, max_row, min_col, max_col) in objects:
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        # Copy the object's pixels to the output grid
        for i in range(height):
            for j in range(width):
                output_grid[i, current_col + j] = color
        current_col += width  # Increment column for next object

    return output_grid
```
