"""
1.  **Background Transformation:** Change all pixels of color white (0) in the input grid to red (2).
2.  **Object Preservation:** Identify all contiguous regions (objects) of non-white (non-0) and non-red (non-2) pixels *in the original input grid*. Maintain the color, shape, and position of those objects in the output grid.
"""

import numpy as np

def find_objects(grid, ignore_colors):
    """Finds contiguous objects of non-ignored colors."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, obj_coords):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col] and grid[row, col] not in ignore_colors:
                obj_coords = []
                dfs(row, col, grid[row, col], obj_coords)
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid.
    output_grid = input_grid.copy()

    # Change all white (0) pixels to red (2).
    output_grid[output_grid == 0] = 2
    
    # Identify Sub-Objects in the *original* input grid.
    ignore_colors = [0, 2]  # Ignore white and red.
    sub_objects = find_objects(input_grid, ignore_colors)

    # Preserve Sub-Object Colors (this step is redundant but kept for clarity with prev. iterations)
    for obj_coords in sub_objects:
        for row, col in obj_coords:
            # Copy the original color from the input to the output (already done implicitly).
            output_grid[row, col] = input_grid[row, col]

    return output_grid