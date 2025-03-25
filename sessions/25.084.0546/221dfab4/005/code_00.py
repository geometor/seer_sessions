"""
The transformation identifies objects of different colors and modifies their colors based on adjacency. Specifically, objects of color '8' (azure) that are adjacent to objects of color '4' (yellow) will have their color changed based on a flood-fill like expansion into the '4' regions, potentially influenced by nearby objects of colors '1' (blue), '2' (red) and '3'(green).
"""

import numpy as np

def find_all_objects(grid):
    # Find contiguous regions of *any* color, including what might be considered background
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_locations = []

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                obj, locs = flood_fill(grid, r, c, visited)
                objects.append(obj)
                object_locations.append(locs)
    return objects, object_locations

def flood_fill(grid, r, c, visited):
    # Standard flood fill, but without excluding any colors
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

def get_neighbors(grid, r, c):
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc, grid[nr, nc]))
    return neighbors

def transform(input_grid):
    # Initialize output grid with a copy of the input grid
    output_grid = input_grid.copy()

    # Find all objects
    _, input_object_locations = find_all_objects(input_grid)
    
    # Iterate over the objects to apply color changing rules
    for obj_locs in input_object_locations:
        first_r, first_c = obj_locs[0]
        obj_color = input_grid[first_r, first_c]
        
        # Apply rules for changing azure (8)
        if obj_color == 8:
          for r,c in obj_locs:
            neighbors = get_neighbors(input_grid, r, c)
            for nr, nc, ncolor in neighbors:
              if ncolor == 4:
                #check if there is 1, 2, 3 around 4 to choose
                four_neighbors = get_neighbors(input_grid, nr, nc)
                neighbor_colors = [c for _,_,c in four_neighbors]
                
                if 1 in neighbor_colors:
                    output_grid[nr,nc] = 3
                elif 2 in neighbor_colors:
                    output_grid[nr,nc] = 4
                elif 3 in neighbor_colors:
                    output_grid[nr,nc] = 3
                else:
                    output_grid[nr,nc] = 4 #default to 4
    return output_grid