"""
1.  **Identify Target Object:** Find the *first* non-zero colored object encountered when scanning the grid from top-to-bottom, left-to-right. Consider this object and it's color.
2.  **Determine Extension Direction:**
    *   If the object is a single pixel or a vertical line, extend vertically downwards.
    *   If the object is a horizontal line, extend horizontally.
3.  **Extend:**
    *   **Vertical Extension:** Extend the object downwards, creating a vertical line of the same color. The new line should occupy the same column(s) as the original object, extending to the bottom edge of the grid (if extending down), unless obstructed by another object. If the object has more than one pixel, extend all pixels to the bottom of the grid.
    *   **Horizontal Extension:** Extend the object, creating a horizontal line of the same color across the entire row.
4. **Other Objects** Any objects below the first encountered object remain unchanged.
"""

import numpy as np

def find_first_object(grid):
    """Finds the first non-zero object in the grid, scanning top-to-bottom, left-to-right."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def dfs(r, c, color, current_object):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                return current_object, grid[r,c] # Return the object and its color
    return [], 0

def is_horizontal_line(shape):
    """Checks if the shape is a horizontal line."""
    if not shape:
        return False
    rows = [r for r, _ in shape]
    return len(set(rows)) == 1 and len(shape) > 1

def is_vertical_line(shape):
    """Checks if a shape is a vertical line."""
    if not shape:
        return False
    cols = [c for _, c in shape]
    return len(set(cols)) == 1 and len(shape) > 1

def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Identify Target Object
    target_object, color = find_first_object(grid)

    if not target_object:  # Handle cases where there are no objects
        return output_grid.tolist()

     # Determine Extension Direction and Extend
    if is_horizontal_line(target_object):
        # Horizontal Extension
        row_index = target_object[0][0]
        for c in range(cols):
            output_grid[row_index, c] = color

    elif is_vertical_line(target_object) or len(target_object) == 1:
       # Vertical Extension (Downwards)
        for r, c in target_object:
            for row_below in range(r, rows):
                output_grid[row_below, c] = color

    return output_grid.tolist()