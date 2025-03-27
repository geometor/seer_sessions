```python
"""
The transformation identifies objects of different colors and modifies their colors based on adjacency and context. Specifically, objects of color '8' (azure) are affected.  If an '8' object is adjacent to a '4' (yellow) object, the '4' object may change color based on neighboring colors '1', '2', or '3'. If an '8' object touches a '1' (blue) object, portions of the '1' object may become '3' (green) near the '8' object. Similarly, portions of a '2' (red) object can become yellow if adjacent to an 8.
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

    # Find all objects in the input grid
    _, input_object_locations = find_all_objects(input_grid)
    
    # Iterate over the object locations
    for obj_locs in input_object_locations:
        first_r, first_c = obj_locs[0]
        obj_color = input_grid[first_r, first_c]
        
        # Apply rules for changing azure (8)
        if obj_color == 8:
            for r, c in obj_locs:
                neighbors = get_neighbors(input_grid, r, c)
                for nr, nc, ncolor in neighbors:
                    # If an '8' is adjacent to a '4', check the '4's neighbors.
                    if ncolor == 4:
                        four_neighbors = get_neighbors(input_grid, nr, nc)
                        neighbor_colors = [c for _,_,c in four_neighbors]
                        
                        if 1 in neighbor_colors:
                            output_grid[nr, nc] = 4
                        elif 2 in neighbor_colors :
                            output_grid[nr,nc] = 4
                        elif 3 in neighbor_colors:
                            output_grid[nr, nc] = 4
                        else:
                            output_grid[nr,nc] = 4
                    if ncolor == 1:
                       one_neighbors = get_neighbors(input_grid,nr,nc)
                       if 4 in [c for _,_,c in one_neighbors]:
                            output_grid[nr,nc] = 3 #turn blue next to yellow and azure into green
                       
                    if ncolor == 2:
                       two_neighbors = get_neighbors(input_grid,nr,nc)

                       if 4 in [c for _,_,c in two_neighbors]:
                            output_grid[nr,nc] = 4
                       
    
    # Iterate over the object locations again, looking for 1's next to 8's
    for obj_locs in input_object_locations:
        first_r, first_c = obj_locs[0]
        obj_color = input_grid[first_r, first_c]
        
        if obj_color == 1:
            for r,c in obj_locs:
               neighbors = get_neighbors(input_grid, r, c)
               for nr, nc, ncolor in neighbors:
                   if ncolor == 8:
                       #If the 8 has yellow next to it
                       eight_neighbors = get_neighbors(input_grid,nr,nc)
                       if 4 in [c for _,_,c in eight_neighbors]:
                            output_grid[r,c] = 3

    # Iterate over the object locations again, looking for 2's next to 8's
    for obj_locs in input_object_locations:
        first_r, first_c = obj_locs[0]
        obj_color = input_grid[first_r, first_c]
        if obj_color == 2:
            for r, c in obj_locs:
                neighbors = get_neighbors(input_grid, r, c)
                for nr,nc, ncolor in neighbors:
                    if ncolor == 8:
                        eight_neighbors = get_neighbors(input_grid,nr,nc)
                        if 4 in [c for _,_, c in eight_neighbors]:
                            output_grid[r,c]=4

    return output_grid
```