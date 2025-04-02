import numpy as np
from collections import deque

"""
Keep only the target-colored pixels that belong to connected regions of 
non-boundary-colored pixels which do not touch the grid border. All other 
pixels, including the boundary color itself and target pixels in regions 
connected to the border, become background color (0).

The boundary color is identified as the non-background color with the highest 
pixel count. Target colors are all other non-background colors.

A connected component search (BFS) is performed starting from each unvisited, 
non-boundary pixel. If a component is found to not touch the border, any 
target-colored pixels within that component are placed onto the output grid.
"""

def find_colors(input_grid_np):
    """
    Identifies background, boundary (most frequent non-0), and target 
    (other non-0) colors.
    """
    unique_colors, counts = np.unique(input_grid_np, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))
    
    background_color = 0
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    
    boundary_color = None
    target_colors = set()
    
    if not non_background_colors:
        return background_color, boundary_color, target_colors
        
    boundary_color = max(non_background_colors, key=non_background_colors.get)
    target_colors = set(non_background_colors.keys()) - {boundary_color}
    
    return background_color, boundary_color, target_colors

def transform(input_grid):
    """
    Transforms the input grid based on the border-connected component rule.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # 1. Identify colors
    background_color, boundary_color, target_colors = find_colors(input_grid_np)

    # Initialize output grid with background color
    output_grid_np = np.full_like(input_grid_np, background_color)

    # Handle edge cases: If no boundary or no targets, return background grid
    if boundary_color is None: # No boundary means everything non-bg is target
        target_colors = set(np.unique(input_grid_np)) - {background_color}
        # If no targets either, result is all background anyway
        if not target_colors:
             return output_grid_np.tolist()
        # Treat the problem as if there's a dummy boundary - effectively check connectivity to border for all non-bg pixels
        # Or simplify: if no boundary, maybe keep all targets? Let's stick to component logic.
        # If no boundary color identified (e.g. only bg and one other color)
        # consider all non-bg colors as targets and proceed, boundary effectively doesn't block anything.
        boundary_color = -1 # Use a dummy value not in 0-9
    
    if not target_colors: # Only background and boundary exist
         return output_grid_np.tolist()


    # 2. Initialize visited grid
    visited = np.zeros_like(input_grid_np, dtype=bool)

    # 3. Process Components
    for r in range(height):
        for c in range(width):
            # Start BFS from unvisited non-boundary cells
            if not visited[r, c] and input_grid_np[r, c] != boundary_color:
                q = deque([(r, c)])
                visited[r, c] = True
                component_pixels = []
                component_targets = []
                touches_border = False
                
                while q:
                    curr_r, curr_c = q.popleft()
                    component_pixels.append((curr_r, curr_c))
                    pixel_color = input_grid_np[curr_r, curr_c]

                    if pixel_color in target_colors:
                        component_targets.append((curr_r, curr_c, pixel_color)) # Store color too

                    # Check border contact
                    if not touches_border and (curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1):
                        touches_border = True
                        
                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        if 0 <= nr < height and 0 <= nc < width:
                            if not visited[nr, nc] and input_grid_np[nr, nc] != boundary_color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                # After BFS for component is done, check border contact
                if not touches_border:
                    # Place targets from this component onto the output grid
                    for tr, tc, t_color in component_targets:
                        output_grid_np[tr, tc] = t_color

    # Convert back to list of lists and return
    return output_grid_np.tolist()