import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1. Identify all distinct contiguous objects composed of blue (1) pixels in the input grid.
2. For each identified blue object, determine if it completely encloses one or more white (0) pixels (forms a "hole"). A hole is defined as a region of white pixels where none of the pixels in the region can reach the border of the grid by only traversing adjacent white pixels.
3. Create an output grid, initially identical to the input grid.
4. If a blue object encloses at least one white pixel (has a hole), change the color of all pixels belonging to that object from blue (1) to red (2) in the output grid.
5. Leave all other pixels (original red pixels, white pixels, and blue pixels belonging to objects without holes) unchanged.
"""

def find_objects(grid, color):
    """Finds all contiguous objects of a specific color."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def has_hole(grid, obj_pixels, background_reachable_mask):
    """Checks if a blue object borders any unreachable white pixels (holes)."""
    height, width = grid.shape
    # Use a set for faster lookup of object pixels
    obj_pixel_set = set(obj_pixels) 
    
    for r, c in obj_pixels:
        # Check all 4 neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is white (0) AND was NOT reached by the background flood fill
                if grid[nr, nc] == 0 and not background_reachable_mask[nr, nc]:
                    # We found a white pixel adjacent to the object that is part of a hole
                    return True
                    
    return False # No adjacent hole pixels found

def flood_fill_background(grid):
    """Performs a flood fill from the border white pixels."""
    height, width = grid.shape
    reachable_mask = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add all border white pixels to the queue and mark as reachable
    for r in range(height):
        if grid[r, 0] == 0:
            q.append((r, 0))
            reachable_mask[r, 0] = True
        if grid[r, width - 1] == 0:
            q.append((r, width - 1))
            reachable_mask[r, width - 1] = True
    for c in range(width): # Avoid double-adding corners
        if grid[0, c] == 0 and not reachable_mask[0,c]:
            q.append((0, c))
            reachable_mask[0, c] = True
        if grid[height - 1, c] == 0 and not reachable_mask[height-1,c]:
            q.append((height - 1, c))
            reachable_mask[height - 1, c] = True
            
    # Perform BFS
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and not reachable_mask[nr, nc]:
                reachable_mask[nr, nc] = True
                q.append((nr, nc))
                
    return reachable_mask


def transform(input_grid):
    """
    Transforms the input grid by changing blue objects (color 1) to red (color 2) 
    if they enclose any white pixels (color 0).
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # 1. Identify all white pixels reachable from the background (border)
    background_reachable_mask = flood_fill_background(input_grid_np)
    
    # 2. Find all distinct blue objects
    blue_objects = find_objects(input_grid_np, 1) # Color 1 is blue
    
    # 3. Check each blue object for holes and update output grid
    for obj_pixels in blue_objects:
        # Check if the object borders any unreachable white pixel (a hole)
        if has_hole(input_grid_np, obj_pixels, background_reachable_mask):
            # If it has a hole, change all its pixels to red (2) in the output grid
            for r, c in obj_pixels:
                output_grid[r, c] = 2 # Color 2 is red

    # Convert back to list of lists if necessary for the environment
    return output_grid.tolist()