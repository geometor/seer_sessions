"""
Transforms a 2D grid based on a multi-step process derived from Examples 1 and 3:
1.  Identify 'bridge' locations: Input cells with value 0 that are flanked horizontally or vertically by identical non-zero neighbors.
2.  Analyze connectivity: Determine connected components of non-zero cells in the input grid using 8-directional adjacency. Identify 'main' components as those containing at least one cell with value 2 or 3.
3.  Construct output grid:
    - Bridge locations become 1.
    - Input cells with value 1 remain 1 if they belong to a 'main' component, otherwise they become 0.
    - All other input cells retain their original values.
This rule accurately describes Examples 1 and 3 but is not expected to work for Example 2.
"""

import copy
from collections import deque

def _is_valid(r, c, rows, cols):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # --- Step 1: Identify Bridge Locations ---
    bridge_locations = set()
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 0:
                # Check horizontal flanking
                if c > 0 and c < cols - 1:
                    left_val = input_grid[r][c-1]
                    right_val = input_grid[r][c+1]
                    if left_val != 0 and left_val == right_val:
                        bridge_locations.add((r, c))
                        continue # Found bridge, skip vertical check
                # Check vertical flanking
                if r > 0 and r < rows - 1:
                    top_val = input_grid[r-1][c]
                    bottom_val = input_grid[r+1][c]
                    if top_val != 0 and top_val == bottom_val:
                        bridge_locations.add((r, c))

    # --- Step 2: Analyze Connectivity ---
    visited = set()
    # Map cell coordinates to whether their component contains a 2 or 3
    component_is_main = {} 
    
    for r in range(rows):
        for c in range(cols):
            # Start BFS from unvisited non-zero cells
            if input_grid[r][c] != 0 and (r, c) not in visited:
                component_cells = []
                q = deque([(r, c)])
                visited.add((r, c))
                current_component_is_main = False
                
                while q:
                    curr_r, curr_c = q.popleft()
                    component_cells.append((curr_r, curr_c))
                    
                    # Check if this cell makes the component 'main'
                    if input_grid[curr_r][curr_c] in [2, 3]:
                        current_component_is_main = True
                        
                    # Explore 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc
                            
                            # If neighbor is valid, non-zero, and not visited
                            if _is_valid(nr, nc, rows, cols) and \
                               input_grid[nr][nc] != 0 and \
                               (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                
                # Mark all cells in the found component
                for comp_r, comp_c in component_cells:
                    component_is_main[(comp_r, comp_c)] = current_component_is_main

    # --- Step 3: Construct Output Grid ---
    output_grid = copy.deepcopy(input_grid)

    for r in range(rows):
        for c in range(cols):
            # Rule 1: Bridge location
            if (r, c) in bridge_locations:
                output_grid[r][c] = 1
            # Rule 2: Original value was 1
            elif input_grid[r][c] == 1:
                # Check component status (default to False if cell wasn't part of any component - shouldn't happen for non-zero)
                is_main = component_is_main.get((r, c), False) 
                if is_main:
                    output_grid[r][c] = 1 # Keep 1 if in main component
                else:
                    output_grid[r][c] = 0 # Change to 0 if not in main component
            # Rule 3: Other cells (original 0s not bridged, 2s, 3s, 4s, etc.)
            # Keep original value (already handled by deepcopy)
            # No 'else' block needed explicitly
            
    return output_grid