import numpy as np
from collections import deque

"""
The transformation identifies the outermost continuous non-zero border region of the input grid. 
It then finds all solid, rectangular blocks of non-zero color within the grid. 
Rectangles that are part of the border region or are adjacent (including diagonally) to any cell of the border region are filtered out.
From the remaining valid rectangles, the one with the largest area is selected. 
If there's a tie in area, the rectangle with the top-most row index is chosen. 
If there's still a tie, the one with the left-most column index is chosen.
The selected rectangular block is then extracted and returned as the output grid.
"""

def _is_valid(r, c, H, W):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < H and 0 <= c < W

def _bfs_find_region(grid, start_r, start_c, H, W):
    """
    Performs Breadth-First Search to find all connected cells 
    of the same color starting from (start_r, start_c).
    Returns a set of (r, c) coordinates for the connected region.
    """
    target_color = grid[start_r, start_c]
    if target_color == 0:
        return set()
        
    q = deque([(start_r, start_c)])
    visited = set([(start_r, start_c)])
    region_coords = set([(start_r, start_c)])
    
    while q:
        r, c = q.popleft()
        
        # Check 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                
                if _is_valid(nr, nc, H, W) and (nr, nc) not in visited and grid[nr, nc] == target_color:
                    visited.add((nr, nc))
                    q.append((nr, nc))
                    region_coords.add((nr, nc))
                    
    return region_coords

def _find_border_region(grid, H, W):
    """
    Identifies the coordinates of the outermost connected non-zero region (border).
    Starts BFS from the first non-zero cell found on the grid edges.
    """
    border_coords = set()
    start_node = None
    
    # Find the first non-zero cell on the edges
    for r in range(H):
        if grid[r, 0] != 0:
            start_node = (r, 0)
            break
        if grid[r, W-1] != 0:
             start_node = (r, W-1)
             break
    if start_node is None:
        for c in range(W):
            if grid[0, c] != 0:
                start_node = (0, c)
                break
            if grid[H-1, c] != 0:
                start_node = (H-1, c)
                break
                
    # If a non-zero edge cell is found, perform BFS
    if start_node:
        border_coords = _bfs_find_region(grid, start_node[0], start_node[1], H, W)
        
    return border_coords

def _find_solid_rectangles(grid, H, W):
    """
    Finds all maximal solid rectangles of non-zero colors in the grid.
    Returns a list of dictionaries, each describing a rectangle.
    """
    rectangles = []
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(H):
        for c in range(W):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                
                # Find max width for the starting row
                current_w = 0
                while c + current_w < W and grid[r, c + current_w] == color:
                    current_w += 1
                
                # Find max height for this width
                current_h = 1
                possible = True
                while r + current_h < H and possible:
                    for k in range(current_w):
                        if c + k >= W or grid[r + current_h, c + k] != color:
                            possible = False
                            break
                    if possible:
                        current_h += 1
                        
                # Now we have a potential rectangle (r, c, current_w, current_h)
                # Check if it's maximal (cannot be extended further up/left while maintaining rect shape)
                # This simple approach finds rectangles starting from top-left corners.
                # We need to mark all cells within the found rectangle as visited.
                
                rectangles.append({
                    'r': r, 
                    'c': c, 
                    'w': current_w, 
                    'h': current_h, 
                    'color': color, 
                    'area': current_w * current_h
                })
                
                # Mark cells as visited
                for rr in range(r, r + current_h):
                    for cc in range(c, c + current_w):
                        if _is_valid(rr, cc, H, W):
                             visited[rr, cc] = True
                             
    return rectangles


def transform(input_grid):
    """
    Identifies and extracts the largest solid non-zero rectangle within the input grid 
    that does not touch the outermost border region. Ties are broken by top-most, 
    then left-most position.
    """
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape
    
    if H == 0 or W == 0:
        return []

    # 1. Find the coordinates of the border region
    border_coords = _find_border_region(grid, H, W)

    # 2. Find all solid non-zero rectangles
    all_rects = _find_solid_rectangles(grid, H, W)

    # 3. Filter rectangles that touch the border
    valid_rects = []
    for rect in all_rects:
        touches_border = False
        # Check every cell within the rectangle
        for rr in range(rect['r'], rect['r'] + rect['h']):
            for cc in range(rect['c'], rect['c'] + rect['w']):
                # Check if the cell itself is part of the border
                if (rr, cc) in border_coords:
                    touches_border = True
                    break
                # Check if any neighbor of the cell is part of the border
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = rr + dr, cc + dc
                        if _is_valid(nr, nc, H, W) and (nr, nc) in border_coords:
                             touches_border = True
                             break
                    if touches_border: break # optimization
            if touches_border: break # optimization
        
        # Add to valid list if it doesn't touch the border
        if not touches_border:
            valid_rects.append(rect)

    # Handle cases where no valid rectangles are found (shouldn't happen based on examples)
    if not valid_rects:
        # As a fallback maybe return the largest rect overall? Or empty?
        # Based on task, assuming a valid one always exists. If not:
         if all_rects: # If no border or border filtering failed, pick largest overall
             all_rects.sort(key=lambda x: (-x['area'], x['r'], x['c']))
             target_rect = all_rects[0]
             output_np = grid[target_rect['r']:target_rect['r']+target_rect['h'], target_rect['c']:target_rect['c']+target_rect['w']]
             return output_np.tolist()
         else:
             return [] # Return empty if no rectangles found at all


    # 4. Select the largest valid rectangle (with tie-breaking)
    # Sort by area (desc), then row (asc), then col (asc)
    valid_rects.sort(key=lambda x: (-x['area'], x['r'], x['c']))
    
    target_rect = valid_rects[0]

    # 5. Extract the output subgrid
    output_np = grid[target_rect['r']:target_rect['r']+target_rect['h'], 
                     target_rect['c']:target_rect['c']+target_rect['w']]

    return output_np.tolist()