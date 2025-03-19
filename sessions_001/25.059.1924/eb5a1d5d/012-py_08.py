"""
1. Determine the Background Color: Identify the most frequent color in the input grid. This is the background color.
2. Identify the Largest Object: Find the largest contiguous region of pixels that *isn't* the background color.  "Contiguous" means connected horizontally or vertically (not diagonally).
3. Determine the Object's Color: Note the color of this largest object.
4. Create the Output Grid: Create a 3x3 grid filled entirely with the background color.
5. Set the Center Pixel: Change the color of the center pixel (at position (1,1) using 0-based indexing) of the output grid to the color of the largest object identified in step 3.
"""

import numpy as np

def find_largest_object(grid, background_color):
    # Find the largest contiguous object that is not the background color.
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_size = 0
    max_object_coords = []

    def dfs(r, c, color, coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or
                grid[r, c] != color):
            return 0
        visited[r, c] = True
        coords.append((r, c))
        size = 1
        size += dfs(r + 1, c, color, coords)
        size += dfs(r - 1, c, color, coords)
        size += dfs(r, c + 1, color, coords)
        size += dfs(r, c - 1, color, coords)
        return size

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != background_color:
                coords = []
                size = dfs(r, c, grid[r, c], coords)
                if size > max_size:
                    max_size = size
                    max_object_coords = coords

    return max_object_coords
    

def transform(input_grid):
    # Determine the background color (most frequent color).
    values, counts = np.unique(input_grid, return_counts=True)
    background_color = values[np.argmax(counts)]
    
    # Identify the largest object and its color.
    largest_object_coords = find_largest_object(input_grid, background_color)
    if not largest_object_coords:
      object_color = background_color  #If not other objects, center will be background
    else:    
      object_color = input_grid[largest_object_coords[0]]
    
    # Create the 3x3 output grid filled with the background color.
    output_grid = np.full((3, 3), background_color)

    # Set the center pixel to the object's color.
    output_grid[1, 1] = object_color

    return output_grid