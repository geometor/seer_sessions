"""
Extracts colored objects from a larger grid and places them into a smaller, condensed grid, discarding the background.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and extracts contiguous blocks of non-zero colored pixels.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj = []
                dfs(r, c, grid[r, c], obj)
                if obj:
                    objects.append(obj)
    return objects

def order_objects(objects):
    """
    Orders objects based on their top-left corner's row and column.
    """
    # sort by top-left corner, first by row, then by column
    return sorted(objects, key=lambda obj: (min(r for r, _ in obj), min(c for _, c in obj)))

def transform(input_grid):
    """
    Transforms the input grid by extracting and re-arranging colored objects.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Identify and Extract objects
    objects = get_objects(input_grid)

    # Order the objects
    ordered_objects = order_objects(objects)
    
    # Calculate dimensions of output grid
    total_pixels = sum(len(obj) for obj in ordered_objects)
    out_rows = int(np.floor(np.sqrt(total_pixels)))
    out_cols = int(np.ceil(total_pixels / out_rows))
    output_grid = np.zeros((out_rows, out_cols), dtype=int)
    
    # Place Objects in output grid
    current_row = 0
    current_col = 0
    
    for obj in ordered_objects:
        for r, c in obj:
            output_grid[current_row, current_col] = input_grid[r,c]
            current_col += 1
            if current_col >= out_cols:
                current_col = 0
                current_row += 1

    return output_grid.tolist()