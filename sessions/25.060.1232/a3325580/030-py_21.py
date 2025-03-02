"""
1.  **Identify Objects:** Examine the input grid and identify all contiguous regions of the same color, which represent distinct objects.
2.  **Check for Single Color:** Determine if there is exactly one color present in the grid, excluding black (0).
3.  **Conditional Vertical Line Extraction:**
    *   If a single, non-black color exists, find a vertical line object of that color.
    *   If a vertical line object of the specified color is found, extract it. The extracted line becomes a new grid containing only the vertical line.
4.  **No Output:** If there is no single, non-black color or if no vertical line of that color is present, the output is an empty grid.
"""

import numpy as np

def find_objects(grid):
    # Find contiguous regions of non-zero pixels
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not visited[i, j] and grid[i, j] != 0:
                obj = []
                dfs(i, j, grid[i, j], obj)
                objects.append(obj)
    return objects

def is_vertical_line(obj, grid):
    # Check if an object is a vertical line
    if not obj:
        return False

    rows, cols = zip(*obj)
    min_col, max_col = min(cols), max(cols)
    min_row, max_row = min(rows), max(rows)

    if max_col - min_col == 0 and max_row - min_row +1 == len(obj):
      return True
    else:
      return False


def transform(input_grid):
    # Find all objects in the grid
    objects = find_objects(input_grid)

    # Check for single non-zero color
    colors = set(input_grid.flatten())
    colors.discard(0)  # Remove black (background)
    
    if len(colors) == 1:
        target_color = colors.pop()

        # Find vertical line of the target color
        selected_object = None
        for obj in objects:
            if is_vertical_line(obj, input_grid) and input_grid[obj[0][0], obj[0][1]] == target_color:
                selected_object = obj
                break
        
        if selected_object:
            rows, _ = zip(*selected_object)
            min_row, max_row = min(rows), max(rows)
            output_grid = np.full((max_row - min_row + 1, 1), target_color)
        else:
          output_grid = np.empty((0, 0), dtype=int) # return empty grid

    else:
        output_grid = np.empty((0, 0), dtype=int) # return empty grid

    return output_grid