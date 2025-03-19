"""
The transformation rule involves identifying contiguous blocks of non-zero pixels (colored objects) in the input grid and reflecting/expanding them across multiple axes to create a symmetrical pattern in the output grid.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous blocks of non-zero pixels.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                objects.append({'color': grid[r, c], 'pixels': obj_pixels})
    return objects

def reflect_point(point, rows, cols):
    """
    Reflects a point across horizontal, vertical, and diagonal axes.
    """
    r, c = point
    reflected_points = []
    
    #horizontal
    reflected_points.append((r, cols - 1 - c))
    
    #vertical
    reflected_points.append((rows - 1 - r, c))

    # both horizontal and vertical
    reflected_points.append((rows-1-r, cols-1-c))
    
    # diagonal (\)
    reflected_points.append((c, r))

    # diagonal (/)
    reflected_points.append((cols - 1- c, rows -1 - r))

    # reflect diagonals of diagonals
    reflected_points.append((cols - 1- r, rows -1 - c))
    reflected_points.append((rows -1 - c, cols - 1- r))

    return reflected_points
    

def transform(input_grid):
    """
    Transforms the input grid by reflecting objects across multiple axes.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)
    
    # Reflect/expand each object
    for obj in objects:
        color = obj['color']
        pixels = obj['pixels']
        all_reflected_pixels = set()

        for pixel in pixels:
          all_reflected_pixels.update(reflect_point(pixel, rows, cols))

        # add original object's pixels
        all_reflected_pixels.update(pixels)
        
        # Place reflected pixels onto the output grid
        for r, c in all_reflected_pixels:
            if 0 <= r < rows and 0 <= c < cols:
                output_grid[r, c] = color

    return output_grid.tolist()