"""
Transform the input grid by removing the background and top five rows, expanding azure regions, and preserving other colored regions in the lower part of the grid.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of the specified color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] == color:
                object_pixels = []
                queue = [(r, c)]
                visited[r, c] = True

                while queue:
                    curr_r, curr_c = queue.pop(0)
                    object_pixels.append((curr_r, curr_c))

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_r, new_c = curr_r + dr, curr_c + dc
                        if 0 <= new_r < rows and 0 <= new_c < cols and not visited[new_r, new_c] and grid[new_r, new_c] == color:
                            queue.append((new_r, new_c))
                            visited[new_r, new_c] = True
                objects.append(object_pixels)
    return objects

def transform(input_grid):
    # Initialize output_grid as an empty grid (all zeros)
    output_grid = np.zeros_like(input_grid)

    # 1. Remove background (gray - 5) - implicitly handled by starting with an all-zero grid.

    # 2. Remove top five rows and all colors (0, 1, 2, 4, 6)
    rows, _ = input_grid.shape

    # 3. Expand Azure (8)
    azure_objects = find_objects(input_grid, 8)
    for obj in azure_objects:
        for r, c in obj:
            output_grid[r,c] = 8
            # Expand downwards and slightly upwards
            for row in range(rows):
                if input_grid[row,c] != 8 and row > 4 :
                        output_grid[row,c] = 8


    # 4. Preserve Lower Colors (copy remaining colors, excluding those removed in step 2)
    for r in range(5, rows):
        for c in range(input_grid.shape[1]):
          if input_grid[r,c] != 5 and input_grid[r,c] !=0 :
            output_grid[r,c] = input_grid[r,c]
    return output_grid