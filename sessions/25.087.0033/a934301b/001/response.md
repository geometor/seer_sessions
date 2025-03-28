```python
import numpy as np
from collections import deque

"""
The transformation rule identifies connected components (shapes) of non-white pixels (pixels with values 1-9, specifically 1 and 8 in the examples). 
For each shape, it examines every azure pixel (value 8) within it.
If any azure pixel within a shape is 'enclosed' - meaning its 3x3 neighborhood (including itself) consists entirely of non-white pixels (1 or 8) - then the entire shape is removed (turned into white pixels, value 0) in the output grid.
If a shape contains no azure pixels, or if all of its azure pixels have at least one white pixel (value 0) in their 3x3 neighborhood, the shape is kept unchanged in the output grid.
White background pixels remain white.
"""

def get_neighbors(r, c, height, width):
    """ Get valid neighbor coordinates within grid bounds """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def get_3x3_neighborhood(grid, r, c):
    """ Get the 3x3 neighborhood values, handling boundaries """
    height, width = grid.shape
    neighborhood = []
    all_non_white = True
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            count += 1
            if 0 <= nr < height and 0 <= nc < width:
                val = grid[nr, nc]
                neighborhood.append(val)
                if val == 0: # white pixel
                    all_non_white = False
            else:
                # Treat out-of-bounds as not non-white
                all_non_white = False
                neighborhood.append(-1) # Placeholder for out-of-bounds

    # Need exactly 9 cells in the neighborhood check to be considered fully surrounded within the grid
    if count != 9:
        all_non_white = False
        
    return neighborhood, all_non_white


def find_shape(grid, start_r, start_c, visited):
    """ Find a connected component (shape) using BFS """
    height, width = grid.shape
    q = deque([(start_r, start_c)])
    shape_pixels = set()
    azure_pixels = []
    
    while q:
        r, c = q.popleft()
        
        if not (0 <= r < height and 0 <= c < width) or visited[r, c] or grid[r, c] == 0:
            continue
            
        visited[r, c] = True
        shape_pixels.add((r, c))
        if grid[r,c] == 8: # azure
             azure_pixels.append((r,c))

        # Check 8 neighbors (cardinal + diagonal)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < height and 0 <= nc < width and not visited[nr, nc] and grid[nr, nc] != 0:
                    q.append((nr, nc))
                    
    return list(shape_pixels), azure_pixels

def transform(input_grid):
    """
    Applies the transformation rule: removes shapes containing any 'enclosed' azure pixel.
    An azure pixel is enclosed if its 3x3 neighborhood is entirely non-white.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # Initialize output grid with white pixels
    output_grid = np.zeros_like(input_grid_np)
    
    # Keep track of visited pixels to avoid processing shapes multiple times
    visited = np.zeros_like(input_grid_np, dtype=bool)
    
    # Iterate through each pixel to find shapes
    for r in range(height):
        for c in range(width):
            # If pixel is non-white and not yet visited, start finding its shape
            if input_grid_np[r, c] != 0 and not visited[r, c]:
                shape_pixels, azure_pixels = find_shape(input_grid_np, r, c, visited)
                
                # Determine if the shape should be kept or removed
                remove_shape = False
                if not azure_pixels:
                    # If shape has no azure pixels, keep it (this case may not occur based on examples)
                    remove_shape = False
                else:
                    # Check each azure pixel in the shape
                    for az_r, az_c in azure_pixels:
                        _, all_non_white = get_3x3_neighborhood(input_grid_np, az_r, az_c)
                        # If any azure pixel is enclosed, mark shape for removal and break
                        if all_non_white:
                            remove_shape = True
                            break
                            
                # If the shape is not marked for removal, copy it to the output grid
                if not remove_shape:
                    for pix_r, pix_c in shape_pixels:
                        output_grid[pix_r, pix_c] = input_grid_np[pix_r, pix_c]

    return output_grid.tolist()
```