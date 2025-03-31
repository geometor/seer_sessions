```python
import numpy as np
from collections import deque

"""
Identifies closed loops formed by blue (1) pixels. 
1. Finds the single connected region of white (0) pixels reachable from the grid boundary (exterior).
2. Identifies any other connected regions of white (0) pixels not reachable from the boundary (interior).
3. For each interior white region found:
    a. Fills the entire region with green (3) pixels in the output grid.
    b. Identifies the blue (1) pixels immediately adjacent (orthogonally) to this interior region (the loop boundary).
    c. Identifies the exterior white pixels immediately adjacent (orthogonally) to these blue boundary pixels.
    d. Colors these adjacent exterior white pixels red (2) in the output grid.
Blue shapes that do not enclose an interior white region, and the exterior white region itself (unless adjacent to a loop), remain unchanged.
"""

def get_neighbors(r, c, height, width):
    """Yields valid orthogonal neighbors for a given cell (r, c)."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def transform(input_grid):
    """
    Applies the fill (green) and border (red) transformation to closed blue loops.
    
    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy() # Initialize output_grid as a copy
    height, width = input_grid_np.shape

    # --- Step 1: Identify the Exterior White Region ---
    # 'is_exterior' marks white pixels connected to the boundary
    is_exterior = np.zeros_like(input_grid_np, dtype=bool) 
    q_exterior = deque()

    # Initialize queue with boundary white pixels
    for r in range(height):
        for c in [0, width - 1]: # Left and right edges
            if input_grid_np[r, c] == 0 and not is_exterior[r, c]:
                is_exterior[r, c] = True
                q_exterior.append((r, c))
    for c in range(1, width - 1): # Top and bottom edges (excluding corners already checked)
        for r in [0, height - 1]:
            if input_grid_np[r, c] == 0 and not is_exterior[r, c]:
                is_exterior[r, c] = True
                q_exterior.append((r, c))

    # BFS to find all connected exterior white pixels
    while q_exterior:
        r, c = q_exterior.popleft()
        for nr, nc in get_neighbors(r, c, height, width):
            # If neighbor is white and not yet marked as exterior
            if input_grid_np[nr, nc] == 0 and not is_exterior[nr, nc]:
                is_exterior[nr, nc] = True
                q_exterior.append((nr, nc))
    
    # --- Step 2: Identify and Process Interior White Regions ---
    # 'visited_interior' prevents reprocessing pixels belonging to already found interior regions
    visited_interior = np.zeros_like(input_grid_np, dtype=bool)

    # Iterate through every pixel to find potential starting points for interior regions
    for r_start in range(height):
        for c_start in range(width):
            # Check if it's a potential start: white(0), not exterior, and not already visited
            if (input_grid_np[r_start, c_start] == 0 and 
                    not is_exterior[r_start, c_start] and 
                    not visited_interior[r_start, c_start]):
                
                # Found a new interior region, start BFS
                current_interior_region = set() # Pixels in this specific region
                blue_boundary = set() # Blue pixels directly touching this region
                q_interior = deque([(r_start, c_start)])
                visited_interior[r_start, c_start] = True # Mark as visited
                
                # BFS to find all connected white pixels in this interior region
                while q_interior:
                    r_int, c_int = q_interior.popleft()
                    current_interior_region.add((r_int, c_int))
                    
                    # Check neighbors of the current interior pixel
                    for nr, nc in get_neighbors(r_int, c_int, height, width):
                        pixel_value = input_grid_np[nr, nc]
                        
                        # If neighbor is blue(1), it's part of the boundary for this region
                        if pixel_value == 1: 
                            blue_boundary.add((nr, nc))
                        # If neighbor is white(0), not exterior, and not visited, add to queue
                        elif (pixel_value == 0 and 
                              not is_exterior[nr, nc] and 
                              not visited_interior[nr, nc]):
                            visited_interior[nr, nc] = True
                            q_interior.append((nr, nc))

                # --- Step 3a: Apply Green Fill for this interior region ---
                for ir, ic in current_interior_region:
                    output_grid[ir, ic] = 3 # Change to Green

                # --- Step 3b: Identify and Apply Red Border for this loop ---
                red_border_locations = set() # Exterior white pixels to turn red
                # Check neighbors of all blue boundary pixels found for this region
                for br, bc in blue_boundary:
                    for nr, nc in get_neighbors(br, bc, height, width):
                        # If neighbor is an exterior white pixel (marked in step 1)
                        if is_exterior[nr, nc]: 
                            # Check original color was white before marking red
                            # This prevents overwriting other colors if logic expands later
                            if input_grid_np[nr,nc] == 0: 
                                red_border_locations.add((nr, nc))
                            
                # Apply the red border
                for rr, rc in red_border_locations:
                    output_grid[rr, rc] = 2 # Change to Red

    return output_grid.tolist()
```