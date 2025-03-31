```python
import numpy as np
from collections import deque

"""
Identifies closed loops formed by blue (1) pixels in the input grid.
For each closed loop found:
1. Fills the area enclosed by the loop with green (3) pixels.
2. Creates a one-pixel thick border of red (2) pixels immediately outside the loop, replacing adjacent white (0) pixels.
If a blue shape does not form a closed loop, it remains unchanged.
The background is white (0).
"""

def get_neighbors(r, c, height, width):
    """Yields valid orthogonal neighbors for a given cell."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def find_regions(grid, target_color):
    """
    Finds connected regions of a specific color using BFS.
    Returns a list of sets, where each set contains the (r, c) coordinates of a region.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start BFS for a new region
                current_region = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_region.add((r, c))

                while q:
                    row, col = q.popleft()
                    for nr, nc in get_neighbors(row, col, height, width):
                        if grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            current_region.add((nr, nc))
                            q.append((nr, nc))
                regions.append(current_region)
    return regions


def transform(input_grid):
    """
    Identifies closed blue loops, fills their interior with green, 
    and borders them externally with red.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # 1. Identify all white regions and classify them as exterior or interior
    white_regions = [] # List to store tuples: (region_pixels, is_interior)
    visited_white = np.zeros_like(input_grid_np, dtype=bool)
    exterior_white_pixels = set()

    q = deque()
    # Initialize queue with boundary white pixels
    for r in range(height):
        for c in [0, width - 1]:
             if input_grid_np[r, c] == 0 and not visited_white[r,c]:
                 q.append((r,c))
                 visited_white[r,c] = True
                 exterior_white_pixels.add((r,c))
    for c in range(width): # Use range(width) instead of range(1, width-1) to include corners
        for r in [0, height -1]:
             if input_grid_np[r, c] == 0 and not visited_white[r,c]:
                 q.append((r,c))
                 visited_white[r,c] = True
                 exterior_white_pixels.add((r,c))
                 
    # BFS for exterior white region(s)
    while q:
        r, c = q.popleft()
        for nr, nc in get_neighbors(r, c, height, width):
            if input_grid_np[nr, nc] == 0 and not visited_white[nr, nc]:
                visited_white[nr, nc] = True
                exterior_white_pixels.add((nr,nc))
                q.append((nr, nc))

    if exterior_white_pixels: # Check if there are any exterior white pixels found
         white_regions.append((exterior_white_pixels, False)) # Add the combined exterior region

    # Find interior white regions (those not visited yet)
    for r in range(height):
        for c in range(width):
            if input_grid_np[r, c] == 0 and not visited_white[r, c]:
                # Start BFS for a new interior region
                current_interior_region = set()
                q_interior = deque([(r, c)])
                visited_white[r, c] = True
                current_interior_region.add((r, c))

                while q_interior:
                    row, col = q_interior.popleft()
                    for nr, nc in get_neighbors(row, col, height, width):
                        if input_grid_np[nr, nc] == 0 and not visited_white[nr, nc]:
                            visited_white[nr, nc] = True
                            current_interior_region.add((nr, nc))
                            q_interior.append((nr, nc))
                
                if current_interior_region: # Ensure we found something
                     white_regions.append((current_interior_region, True))


    # 2. Process interior white regions (these define the closed loops)
    for region_pixels, is_interior in white_regions:
        if is_interior:
            adjacent_blue_pixels = set()
            adjacent_exterior_white_for_border = set()

            # Fill the interior region with green
            for r, c in region_pixels:
                output_grid[r, c] = 3 # Green
                # While iterating interior pixels, find adjacent blue pixels
                for nr, nc in get_neighbors(r, c, height, width):
                    if input_grid_np[nr, nc] == 1: # Blue
                        adjacent_blue_pixels.add((nr, nc))

            # Find exterior white pixels adjacent to the identified blue border
            for br, bc in adjacent_blue_pixels:
                 for nr, nc in get_neighbors(br, bc, height, width):
                     # Check if neighbor is white AND belongs to the exterior set
                     if (nr, nc) in exterior_white_pixels: 
                         adjacent_exterior_white_for_border.add((nr,nc))

            # Color the adjacent exterior white pixels red
            for r, c in adjacent_exterior_white_for_border:
                 output_grid[r, c] = 2 # Red

    return output_grid.tolist()
```