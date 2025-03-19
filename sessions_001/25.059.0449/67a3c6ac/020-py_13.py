"""
The transformation rule involves identifying contiguous regions (objects) of the same color and replacing objects of color 0 (black) with the color of another object present in the input. If no black objects are present, the output is identical to the input.
"""

import numpy as np
from collections import Counter

def get_objects(grid):
    """Identifies contiguous objects of the same color in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj_pixels):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                obj_pixels = []
                dfs(row, col, color, obj_pixels)
                if obj_pixels:
                    objects.append({
                        'color': color,
                        'pixels': obj_pixels,
                        'size': len(obj_pixels),
                        'bbox': (min(p[0] for p in obj_pixels), min(p[1] for p in obj_pixels),
                                 max(p[0] for p in obj_pixels), max(p[1] for p in obj_pixels))
                    })
    return objects

def transform(input_grid):
    """
    Replaces objects of color 0 with the color of another object present in the input.
    """
    # initialize output_grid
    output_grid = input_grid.copy()
    objects = get_objects(input_grid)
    
    # Find objects with color 0
    black_objects = [obj for obj in objects if obj['color'] == 0]

    # If there are no black objects, return the original grid
    if not black_objects:
        return output_grid

    # Find other colors present
    other_colors = [obj['color'] for obj in objects if obj['color'] != 0]

    #If no other colors, return original
    if not other_colors:
        return output_grid
    
    replacement_color = other_colors[0]

    # Replace color 0 pixels with the replacement color
    for obj in black_objects:
        for row, col in obj['pixels']:
            output_grid[row, col] = replacement_color
            
    return output_grid