import numpy as np
from collections import deque

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Red (2) pixels remain unchanged.
    2. Identify connected regions (components) of white (0) pixels.
    3. Determine which white pixels are 'border-reachable' by performing a flood fill (BFS)
       starting from all white pixels on the grid's border, treating red pixels as barriers.
    4. For each white component:
       a. Check if it's adjacent (4-directionally) to any red pixel.
       b. If not adjacent to red, it remains white (0).
       c. If adjacent to red:
          i. Check if any pixel in the component is 'border-reachable'.
          ii. If border-reachable, fill the entire component with blue (1).
          iii. If not border-reachable (enclosed by red), fill the entire component with azure (8).
    """
    
    # Convert input_list to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # Initialize arrays to track visited pixels during BFS and border reachability
    visited_border = np.zeros_like(input_grid_np, dtype=bool)
    border_reachable = np.zeros_like(input_grid_np, dtype=bool)
    
    # --- Step 1: Determine border-reachable white pixels ---
    q = deque()
    
    # Add all white border pixels to the queue and mark them
    for r in range(height):
        for c in [0, width - 1]: # Left and Right borders
            if input_grid_np[r, c] == 0 and not visited_border[r, c]:
                q.append((r, c))
                visited_border[r, c] = True
                border_reachable[r, c] = True
    for c in range(width):
        for r in [0, height - 1]: # Top and Bottom borders (avoid double-adding corners)
             if input_grid_np[r, c] == 0 and not visited_border[r, c]:
                q.append((r, c))
                visited_border[r, c] = True
                border_reachable[r, c] = True

    # Perform BFS for border reachability
    while q:
        r, c = q.popleft()
        
        # Check 4-directional neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds, if white, and not visited
            if 0 <= nr < height and 0 <= nc < width and \
               input_grid_np[nr, nc] == 0 and not visited_border[nr, nc]:
                visited_border[nr, nc] = True
                border_reachable[nr, nc] = True
                q.append((nr, nc))

    # --- Step 2: Identify white components, check adjacency & reachability, and fill ---
    visited_component = np.zeros_like(input_grid_np, dtype=bool)
    
    for r in range(height):
        for c in range(width):
            # If it's a white pixel and hasn't been visited as part of a component yet
            if input_grid_np[r, c] == 0 and not visited_component[r, c]:
                
                component_pixels = []
                is_adj_to_red = False
                is_reachable_from_border = False
                
                comp_q = deque([(r, c)])
                visited_component[r, c] = True
                
                # BFS to find the current white component and its properties
                while comp_q:
                    cr, cc = comp_q.popleft()
                    component_pixels.append((cr, cc))
                    
                    # Check if this specific pixel is border-reachable
                    if border_reachable[cr, cc]:
                        is_reachable_from_border = True
                        
                    # Check neighbors for adjacency to red and other white pixels
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = cr + dr, cc + dc
                        
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check for adjacent red pixel
                            if input_grid_np[nr, nc] == 2:
                                is_adj_to_red = True
                                
                            # Check for adjacent white pixel for component expansion
                            elif input_grid_np[nr, nc] == 0 and not visited_component[nr, nc]:
                                visited_component[nr, nc] = True
                                comp_q.append((nr, nc))
                
                # --- Step 3: Fill the component based on its properties ---
                if is_adj_to_red:
                    fill_color = 1 if is_reachable_from_border else 8
                    for pr, pc in component_pixels:
                        output_grid[pr, pc] = fill_color
                # Else: component is not adjacent to red, leave it white (already is in output_grid)

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()