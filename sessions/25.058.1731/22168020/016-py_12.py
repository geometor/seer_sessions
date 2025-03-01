"""
Identifies two distinct colored regions (magenta and azure) in the input grid. 
Expands the magenta region horizontally to the right within its original rows.
Expands the azure region horizontally to the left within its original rows.
"""

import numpy as np

def get_objects(grid):
    # Find distinct colored regions
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)
    
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                color = grid[r, c]
                object_pixels = []
                queue = [(r, c)]
                visited[r, c] = True
                
                while queue:
                    curr_r, curr_c = queue.pop(0)
                    object_pixels.append((curr_r, curr_c))
                    
                    # Check adjacent cells
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_r, new_c = curr_r + dr, curr_c + dc
                        if (0 <= new_r < grid.shape[0] and 0 <= new_c < grid.shape[1] and
                            not visited[new_r, new_c] and grid[new_r, new_c] == color):
                            queue.append((new_r, new_c))
                            visited[new_r, new_c] = True
                
                if color not in objects:
                    objects[color] = []
                objects[color].append(object_pixels)
                
    return objects

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)
    objects = get_objects(input_grid)


    # Expand magenta region (color 6)
    if 6 in objects:
        for magenta_object in objects[6]:
            min_row = min(pixel[0] for pixel in magenta_object)
            max_row = max(pixel[0] for pixel in magenta_object)
            for row in range(min_row, max_row + 1):
               for col in range(input_grid.shape[1]):
                if any(pixel[0] == row and pixel[1] <= col for pixel in magenta_object ):
                    output_grid[row,col] = 6

    # Expand azure region (color 8)
    if 8 in objects:
      for azure_object in objects[8]:
        min_row = min(pixel[0] for pixel in azure_object)
        max_row = max(pixel[0] for pixel in azure_object)
        for row in range(min_row, max_row + 1):
           for col in reversed(range(input_grid.shape[1])):
            if any(pixel[0] == row and pixel[1] >= col for pixel in azure_object ):
                output_grid[row,col] = 8

    return output_grid