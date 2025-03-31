import numpy as np
from collections import deque

"""
Transforms an input grid based on the following rules:

1.  Preserve Original Objects: Any maroon (9) pixels in the input grid are kept in the same position in the output grid.
2.  Create Green Frames: Any white (0) pixel in the input grid that is adjacent (including diagonally, 8-way connectivity) to at least one maroon (9) pixel becomes green (3) in the output grid. If multiple maroon blocks are close, their green frames merge.
3.  Identify Remaining White Regions: After placing the maroon pixels and generating the green frames, identify the connected components of the remaining white (0) pixels using 8-way connectivity.
4.  Fill Rectangular White Regions with Blue: For each connected component of white pixels identified in step 3, determine if the shape of the component forms a perfect rectangle. If it does, fill all pixels within that component with blue (1) in the output grid. If the component is not a perfect rectangle, its pixels remain white (0).
5.  Precedence: Maroon pixels take precedence over green. Green pixels take precedence over potential blue or remaining white pixels. Blue pixels take precedence over remaining white pixels.
"""

def get_neighbors(r, c, height, width):
    """Generates valid 8-way neighbor coordinates for a given cell."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_connected_component(grid, start_r, start_c, target_color, visited):
    """Finds a connected component using BFS."""
    height, width = grid.shape
    if not (0 <= start_r < height and 0 <= start_c < width) or \
       visited[start_r, start_c] or \
       grid[start_r, start_c] != target_color:
        return None

    component = set()
    q = deque([(start_r, start_c)])
    visited[start_r, start_c] = True

    while q:
        r, c = q.popleft()
        component.add((r, c))

        for nr, nc in get_neighbors(r, c, height, width):
            if not visited[nr, nc] and grid[nr, nc] == target_color:
                visited[nr, nc] = True
                q.append((nr, nc))
    
    return component

def is_rectangle(component_coords):
    """Checks if a set of coordinates forms a solid rectangle."""
    if not component_coords:
        return False
        
    rows = [r for r, c in component_coords]
    cols = [c for r, c in component_coords]
    
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    expected_height = max_r - min_r + 1
    expected_width = max_c - min_c + 1
    expected_size = expected_height * expected_width
    
    return len(component_coords) == expected_size

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    output_grid = np.copy(input_grid_np) # Start with maroon pixels

    # 1. Create Green Frames
    maroon_pixels = set(tuple(coord) for coord in np.argwhere(input_grid_np == 9))
    
    for r in range(height):
        for c in range(width):
            # Only consider original white pixels
            if input_grid_np[r, c] == 0:
                is_neighbor_to_maroon = False
                for nr, nc in get_neighbors(r, c, height, width):
                    if (nr, nc) in maroon_pixels:
                        is_neighbor_to_maroon = True
                        break
                if is_neighbor_to_maroon:
                    output_grid[r, c] = 3 # Turn white pixel green

    # 2. Find and Fill Blue Rectangles
    visited = np.zeros_like(output_grid, dtype=bool)
    
    for r in range(height):
        for c in range(width):
            # Look for unvisited white pixels in the *current* output grid
            if output_grid[r, c] == 0 and not visited[r, c]:
                # Find the connected component of white pixels starting from here
                component = find_connected_component(output_grid, r, c, 0, visited)
                
                if component:
                    # Check if the component forms a perfect rectangle
                    if is_rectangle(component):
                        # If it's a rectangle, color it blue
                        for cr, cc in component:
                            output_grid[cr, cc] = 1
                    # If not a rectangle, it remains white (0), and visited is already marked

    return output_grid.tolist()
