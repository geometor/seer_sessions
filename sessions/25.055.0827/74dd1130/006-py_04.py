"""
Transforms the input grid based on observed patterns. The transformation involves identifying objects, checking for grid uniformity, and applying a conditional rotation or transposition to non-black objects based on their size and position.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects within the grid.  Returns a list of objects,
    where each object is a dictionary containing 'color', 'pixels', and 'shape'.
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    objects = []

    def dfs(r, c, color, pixels):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                (r, c) in visited or grid[r][c] != color):
            return
        visited.add((r, c))
        pixels.append((r, c))
        dfs(r + 1, c, color, pixels)
        dfs(r - 1, c, color, pixels)
        dfs(r, c + 1, color, pixels)
        dfs(r, c - 1, color, pixels)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r][c]
                pixels = []
                dfs(r, c, color, pixels)
                if pixels:
                    # Determine shape
                    min_r, min_c = min(pixels, key=lambda x: (x[0], x[1]))
                    max_r, max_c = max(pixels, key=lambda x: (x[0], x[1]))
                    height = max_r - min_r + 1
                    width = max_c - min_c + 1
                    shape = f"{height}x{width}"

                    objects.append({'color': color, 'pixels': pixels, 'shape': shape, 'min_row':min_r, 'min_col':min_c})
    return objects

def rotate_point(point, rows, cols):
    """Rotates a single point 90 degrees clockwise within a grid."""
    r, c = point
    return c, rows - 1 - r

def transpose_pixels(pixels, min_row, min_col):
    """Transposes a list of pixel coordinates (for 90-degree rotation)."""
      # Determine dimensions of the object's bounding box.
    height = max(p[0] for p in pixels) - min_row + 1
    width = max(p[1] for p in pixels) - min_col + 1
    
    transposed_pixels = []
    for r, c in pixels:
      new_r = min_row + (c-min_col)
      new_c = min_col + (r - min_row) #was: (height-1) - (r-min_row)
      transposed_pixels.append((new_r,new_c))

    return transposed_pixels

def transform(input_grid):
    # 1. Identify Objects
    objects = find_objects(input_grid)

    # 2. Check for Uniformity
    if len(objects) == 1 and objects[0]['color'] != 0:
        return input_grid

    # Initialize output grid with black (0)
    rows, cols = len(input_grid), len(input_grid[0])
    output_grid = [[0] * cols for _ in range(rows)]

    # 3. Conditional Rotation/Transformation and Output
    for obj in objects:
        if obj['color'] != 0:  # Non-black object
            if len(obj['pixels']) == 1:  # Single-pixel object
                # Rotate the position of the single pixel
                rotated_r, rotated_c = rotate_point(obj['pixels'][0], rows, cols)
                output_grid[rotated_r][rotated_c] = obj['color']
            else: #rotate just object, maintain overall location
                rotated_pixels = transpose_pixels(obj['pixels'], obj['min_row'], obj['min_col'])
                for r, c in rotated_pixels:
                    if 0 <= r < rows and 0<= c < cols:
                        output_grid[r][c] = obj['color']
        else:
            for r,c in obj['pixels']:
                output_grid[r][c] = obj['color']


    return output_grid