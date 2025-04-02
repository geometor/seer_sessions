Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

"""
Identifies "cavities" - regions of background pixels bounded by a single contiguous non-background, non-red object ("container").
If a red pixel (color 2) is adjacent (including diagonals) to such a cavity, the cavity region is filled with white (color 0).
The red object that triggered the fill is then modified:
- If any pixel of the red object is edge-adjacent to the newly filled white cavity, the entire red object becomes white (0).
- Otherwise, the entire red object becomes the background color.
Red objects that are not adjacent to any valid cavity are changed to the background color.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def get_neighbors(r, c, height, width, connectivity=8):
    """Gets valid neighbor coordinates."""
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if connectivity == 4 and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_connected_component(grid, start_r, start_c, target_colors, visited_global=None):
    """
    Finds all connected pixels of target_colors starting from (start_r, start_c)
    using BFS. Updates visited_global if provided.
    """
    if grid[start_r, start_c] not in target_colors:
        return set()
    
    height, width = grid.shape
    component = set()
    q = deque([(start_r, start_c)])
    visited_local = set([(start_r, start_c)])

    if visited_global is not None:
        if (start_r, start_c) in visited_global:
            return set() # Already processed globally
        visited_global.add((start_r, start_c))


    while q:
        r, c = q.popleft()
        component.add((r, c))

        for nr, nc in get_neighbors(r, c, height, width, connectivity=8): # Use 8-connectivity for components
            neighbor_coord = (nr, nc)
            if neighbor_coord not in visited_local and grid[nr, nc] in target_colors:
                visited_local.add(neighbor_coord)
                if visited_global is not None:
                     if neighbor_coord in visited_global: continue # Already processed globally
                     visited_global.add(neighbor_coord)
                q.append(neighbor_coord)
                
    return component


def transform(input_grid):
    """
    Applies the cavity filling transformation.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    background_color = find_background_color(input_grid)
    fill_color = 0
    red_color = 2
    
    processed_red_pixels = set() # Keeps track of red pixels belonging to objects already processed
    pixels_to_change = {} # Stores final changes: {(r, c): color}
    visited_background = set() # Track visited background pixels for cavity finding efficiency
    
    cavities_found = [] # Stores tuples: (cavity_coords, bounding_container_coords, adjacent_red_coords)

    # 1. Find potential cavities (background regions bounded by single container object)
    for r in range(height):
        for c in range(width):
            # Start search from unvisited background pixels
            if input_grid[r, c] == background_color and (r, c) not in visited_background:
                # Find the full connected region of background pixels
                background_region = find_connected_component(input_grid, r, c, {background_color}, visited_global=visited_background)
                if not background_region: continue

                boundary_pixels = set()
                adjacent_red_pixels = set()
                container_boundary_pixels = set()
                
                # Analyze neighbors of the background region
                for br, bc in background_region:
                    for nr, nc in get_neighbors(br, bc, height, width, connectivity=8): # Check all 8 neighbors
                        neighbor_coord = (nr, nc)
                        # Skip if neighbor is part of the same background region
                        if neighbor_coord in background_region: 
                            continue
                            
                        neighbor_color = input_grid[nr, nc]
                        # If neighbor is non-background, it's part of the boundary
                        if neighbor_color != background_color:
                             boundary_pixels.add(neighbor_coord)
                             # Categorize boundary pixel
                             if neighbor_color == red_color:
                                 adjacent_red_pixels.add(neighbor_coord)
                             else: # It's a container pixel
                                 container_boundary_pixels.add(neighbor_coord)

                # Check if this region is a valid cavity candidate:
                # - Must have container boundary pixels
                # - Must have adjacent red pixels
                if not container_boundary_pixels or not adjacent_red_pixels:
                    continue

                # Check if all container boundary pixels belong to a single connected container object
                first_container_pixel = next(iter(container_boundary_pixels))
                container_color = input_grid[first_container_pixel]
                
---
