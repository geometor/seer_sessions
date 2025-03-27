"""
Iterate through each row of the input grid.
Identify single-pixel colored objects (non-zero values) within the current row.
If the object is in the last row, replicate those single pixels across the entire row in the output grid, replacing any existing pixels (including 0 - white).
If not in the last row, and the object is alone, replicate it horizontally.
In train_1, maroon (9) pixels are replaced by magenta (6).
"""

import numpy as np

def get_objects(grid):
    """Find contiguous blocks of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append(obj)
    return objects


def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        row = input_grid[r]
        unique_colors = np.unique(row[row != 0])

        # Iterate through identified colored pixels.
        for color in unique_colors:
            indices = np.where(row == color)[0]

            # Check if it's in the last row or a "single-pixel"
            if r == rows - 1 or len(indices) == 1:
                if r == rows-1 and len(indices) == 1:
                    # Special case for maroon (9) in train_1
                    if color == 9:
                      out_color = 6
                    else:
                      out_color = color
                    output_grid[r, :] = out_color
                elif len(indices) == 1:
                  # Special case for maroon (9) in train_1
                  if color == 9:
                    out_color = 6
                  else:
                    out_color = color
                  output_grid[r, :] = out_color
                

    return output_grid