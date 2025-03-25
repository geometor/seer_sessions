"""
The transformation identifies objects of color azure(8) and other colors within a background of white(1) and azure(8).
It then modifies the azure(8) objects to include cells that had object colors, leaving the cells of the other colors unchanged.
"""

import numpy as np

def find_objects(grid, background_colors):
    # Find contiguous regions of non-background color
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_locations = []

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] not in background_colors:
                obj, locs = flood_fill(grid, r, c, visited, background_colors)
                objects.append(obj)
                object_locations.append(locs)
    return objects, object_locations

def flood_fill(grid, r, c, visited, background_colors):
    rows, cols = grid.shape
    color = grid[r, c]
    object_pixels = []
    locations = []
    stack = [(r, c)]
    visited[r, c] = True

    while stack:
        row, col = stack.pop()
        object_pixels.append(grid[row,col])
        locations.append((row,col))


        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc] and grid[nr, nc] == color:
                visited[nr, nc] = True
                stack.append((nr, nc))

    return object_pixels, locations

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    background_colors = [1, 8]
    
    # Find objects and their locations
    objects, object_locations = find_objects(input_grid, background_colors)
    
    azure_locations = []
    other_color_locations = {}

    # Process input grid: find azure and other colors
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 8:
                azure_locations.append((r,c))
            elif input_grid[r,c] not in background_colors:
                if input_grid[r,c] not in other_color_locations:
                    other_color_locations[input_grid[r,c]] = []
                other_color_locations[input_grid[r,c]].append((r,c))
    
    # Create output: first set azure locations, then overwrite with original other colors
    for r, c in azure_locations:
        output_grid[r,c] = 8
    for color in other_color_locations:
        for r, c in other_color_locations[color]:
            output_grid[r,c] = color
    
    return output_grid