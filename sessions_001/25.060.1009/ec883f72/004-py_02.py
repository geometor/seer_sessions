"""
1.  **Identify Objects:** Find each contiguous region of non-background (non-zero) colored pixels. Consider each of these an "object".
2.  **Find Boundary Pixels:** For the all objects combined, consider only the pixels that are adjacent to the background (value 0).
3.  **Expansion:** Replace all background pixels (value 0) that are adjacent to any object with the color of the object it is adjacent to.
4. The output grid will be the same size as the input grid.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-background pixels."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append(obj_pixels)
    return objects

def find_boundary_pixels(grid, objects):
    """Finds pixels adjacent to the background for all objects."""
    boundary_pixels = []
    for obj in objects:
        for row, col in obj:
            neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
            for nr, nc in neighbors:
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr, nc] == 0:
                    boundary_pixels.append( (row,col) ) #append the object pixel
                    break  # Move to the next pixel in the object
    return boundary_pixels

def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = grid.copy()

    # Find objects
    objects = find_objects(grid)

    # Find boundary pixels
    boundary_pixels = find_boundary_pixels(grid, objects)
    
    #change output pixels - expansion
    for r, c in boundary_pixels:
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for nr, nc in neighbors:
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr,nc] == 0:
                output_grid[nr,nc] = grid[r,c]

    return output_grid.tolist()