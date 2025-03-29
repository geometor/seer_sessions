import numpy as np
from collections import deque

"""
Identifies hollow red (2) shapes in the input grid that contain exactly one 
disconnected internal red (2) pixel. The white (0) space enclosed within 
each such shape is then filled with a specific color based on the vertical 
position of the internal red pixel relative to the top of the shape's 
bounding box.

Transformation Steps:
1. Find all distinct connected components of red (2) pixels.
2. For each red component:
    a. Calculate its bounding box.
    b. Identify all pixels strictly inside the bounding box.
    c. Separate these internal pixels into internal red pixels and internal white pixels.
    d. Check if there is exactly one internal red pixel and at least one internal white pixel.
    e. If the conditions in (d) are met:
        i. Determine the relative row index of the internal red pixel (its row minus the bounding box's top row).
        ii. Select the fill color: Azure (8) for relative row 2, Yellow (4) for relative row 3, Green (3) for relative row 4.
        iii. Use a flood fill algorithm starting from an internal white pixel to change all connected interior white pixels to the selected fill color, stopping at the red boundary of the component.
3. Return the modified grid.
"""

def find_component_bfs(grid, start_r, start_c, target_color, visited):
    """Finds a connected component using BFS."""
    H, W = grid.shape
    component = set()
    q = deque([(start_r, start_c)])
    visited.add((start_r, start_c))
    component.add((start_r, start_c))

    while q:
        r, c = q.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and \
               grid[nr, nc] == target_color and \
               (nr, nc) not in visited:
                visited.add((nr, nc))
                component.add((nr, nc))
                q.append((nr, nc))
    return component

def get_bounding_box(component):
    """Calculates the bounding box of a component."""
    if not component:
        return None
    rows = [r for r, c in component]
    cols = [c for r, c in component]
    return min(rows), min(cols), max(rows), max(cols)

def flood_fill_interior(grid, start_r, start_c, fill_color, boundary_color):
    """Fills an interior area (initially white 0) with fill_color, stopping at boundary_color."""
    H, W = grid.shape
    target_color = 0 # We are filling the white interior
    
    if not (0 <= start_r < H and 0 <= start_c < W):
        return # Start position out of bounds
    if grid[start_r, start_c] != target_color:
        return # Start position is not the target color (e.g., already filled or is boundary)
        
    q = deque([(start_r, start_c)])
    visited_fill = set([(start_r, start_c)]) # Track visited pixels for this specific fill
    grid[start_r, start_c] = fill_color # Fill starting pixel

    while q:
        r, c = q.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and \
               (nr, nc) not in visited_fill and \
               grid[nr, nc] != boundary_color: # Stop at boundary
                
                if grid[nr, nc] == target_color: # Only fill target color
                    visited_fill.add((nr, nc))
                    grid[nr, nc] = fill_color
                    q.append((nr, nc))
                # Note: We don't add non-target, non-boundary pixels to the queue,
                # effectively containing the fill within the intended area.

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    H, W = input_grid.shape
    output_grid = np.copy(input_grid)
    visited_component = set() # Track visited red pixels for component finding

    # Iterate through each pixel to find potential starts of red components
    for r in range(H):
        for c in range(W):
            if input_grid[r, c] == 2 and (r, c) not in visited_component:
                # Found an unvisited red pixel, find its component
                component = find_component_bfs(input_grid, r, c, 2, visited_component)

                if not component:
                    continue

                # Calculate bounding box for the component
                bbox = get_bounding_box(component)
                if bbox is None:
                    continue
                min_r, min_c, max_r, max_c = bbox

                # Find internal red and white pixels (strictly inside the bbox)
                internal_red_pixels = set()
                internal_white_pixels = set()
                
                # Check only if the bounding box allows for internal pixels
                if max_r > min_r + 1 and max_c > min_c + 1:
                    for rr in range(min_r + 1, max_r):
                        for cc in range(min_c + 1, max_c):
                            # Check if the pixel is NOT part of the red component itself
                            if (rr, cc) not in component:
                                if input_grid[rr, cc] == 2:
                                    internal_red_pixels.add((rr, cc))
                                elif input_grid[rr, cc] == 0:
                                    internal_white_pixels.add((rr, cc))

                # Check conditions: exactly one internal red, at least one internal white
                if len(internal_red_pixels) == 1 and len(internal_white_pixels) > 0:
                    # Get the internal red pixel's coordinates
                    ir_r, ir_c = list(internal_red_pixels)[0]

                    # Calculate relative row
                    relative_row = ir_r - min_r

                    # Determine fill color based on relative row
                    fill_color = 0 # Default/error color
                    if relative_row == 2:
                        fill_color = 8 # Azure
                    elif relative_row == 3:
                        fill_color = 4 # Yellow
                    elif relative_row == 4:
                        fill_color = 3 # Green
                    
                    # If a valid fill color was determined, perform flood fill
                    if fill_color != 0:
                        # Pick a starting white pixel for the flood fill
                        start_wr, start_wc = list(internal_white_pixels)[0]
                        # Perform flood fill on the output grid
                        flood_fill_interior(output_grid, start_wr, start_wc, fill_color, 2) # Boundary is red (2)

    return output_grid