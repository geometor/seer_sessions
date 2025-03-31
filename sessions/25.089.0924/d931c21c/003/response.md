```python
import numpy as np
from collections import deque

"""
Identifies closed loops formed by blue (1) pixels in the input grid. 
Finds the single connected region of white (0) pixels reachable from the grid boundary (exterior).
Identifies any other connected regions of white (0) pixels not reachable from the boundary (interior).
For each interior white region:
1. Fills the entire region with green (3) pixels in the output grid.
2. Identifies the blue (1) pixels immediately adjacent (orthogonally) to this interior region (the loop boundary).
3. Identifies the exterior white pixels immediately adjacent (orthogonally) to these blue boundary pixels.
4. Colors these adjacent exterior white pixels red (2) in the output grid.
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
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # --- Step 1: Identify the Exterior White Region ---
    is_exterior = np.zeros_like(input_grid_np, dtype=bool)
    q_exterior = deque()

    # Initialize queue with boundary white pixels
    for r in range(height):
        for c in [0, width - 1]:
            if input_grid_np[r, c] == 0 and not is_exterior[r, c]:
                is_exterior[r, c] = True
                q_exterior.append((r, c))
    # Ensure corners are included if width/height > 1
    for c in range(1, width - 1): 
        for r in [0, height - 1]:
            if input_grid_np[r, c] == 0 and not is_exterior[r, c]:
                is_exterior[r, c] = True
                q_exterior.append((r, c))

    # BFS to find all connected exterior white pixels
    while q_exterior:
        r, c = q_exterior.popleft()
        for nr, nc in get_neighbors(r, c, height, width):
            if input_grid_np[nr, nc] == 0 and not is_exterior[nr, nc]:
                is_exterior[nr, nc] = True
                q_exterior.append((nr, nc))
    
    # --- Step 2: Identify and Process Interior White Regions ---
    visited_interior = np.zeros_like(input_grid_np, dtype=bool)

    for r_start in range(height):
        for c_start in range(width):
            # Check if it's a potential start of an interior region
            if (input_grid_np[r_start, c_start] == 0 and 
                    not is_exterior[r_start, c_start] and 
                    not visited_interior[r_start, c_start]):
                
                # Found a new interior region, start BFS
                current_interior_region = set()
                blue_boundary = set()
                q_interior = deque([(r_start, c_start)])
                visited_interior[r_start, c_start] = True
                
                while q_interior:
                    r_int, c_int = q_interior.popleft()
                    current_interior_region.add((r_int, c_int))
                    
                    # Fill with green
                    output_grid[r_int, c_int] = 3 

                    # Check neighbors
                    for nr, nc in get_neighbors(r_int, c_int, height, width):
                        pixel_value = input_grid_np[nr, nc]
                        
                        if pixel_value == 1: # Blue pixel - part of boundary
                            blue_boundary.add((nr, nc))
                        elif (pixel_value == 0 and 
                              not is_exterior[nr, nc] and 
                              not visited_interior[nr, nc]):
                            # Unvisited interior white neighbor
                            visited_interior[nr, nc] = True
                            q_interior.append((nr, nc))

                # --- Step 3: Identify and Apply Red Border for this loop ---
                red_border_locations = set()
                for br, bc in blue_boundary:
                    for nr, nc in get_neighbors(br, bc, height, width):
                        # Check if neighbor is exterior white
                        if is_exterior[nr, nc]: 
                            red_border_locations.add((nr, nc))
                            
                # Apply the red border
                for rr, rc in red_border_locations:
                    output_grid[rr, rc] = 2 # Red

    return output_grid.tolist()
```