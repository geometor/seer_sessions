import numpy as np
from collections import deque

"""
Identifies closed shapes formed by red (2) pixels in the input grid, resembling either a digit '5' or a letter 'H'.
The transformation involves filling the area enclosed by these red shapes with a specific color, 
while leaving the red outline and the exterior background (white - 0) unchanged. 
The fill color depends on the shape type ('5' or 'H') and whether the shape originally contained an internal 
red pixel (2) within its enclosed area in the input grid.

Rules:
1. Find all distinct connected components of red (2) pixels (boundaries).
2. For each boundary component:
    a. Find the set of enclosed white (0) pixels (interior).
    b. Classify the red shape boundary as '5' or 'H'.
    c. Check if any red (2) pixel existed within the interior region in the *input* grid.
    d. Determine the fill color based on shape and internal red presence:
        - If shape is '5', fill color is azure (8).
        - If shape is 'H' and has internal red, fill color is yellow (4).
        - If shape is 'H' and has no internal red, fill color is green (3).
    e. Fill the white interior pixels in the *output* grid with the determined fill color. Original red pixels within the interior remain unchanged.
3. Pixels not part of a boundary or an enclosed interior remain unchanged.
"""

def find_connected_component(grid, start_coord, target_color, visited):
    """Finds all coordinates of a connected component of target_color using BFS."""
    height, width = grid.shape
    q = deque([start_coord])
    component_coords = set()
    # Add start_coord to visited *before* starting BFS for this component
    visited.add(start_coord)
    component_coords.add(start_coord)

    while q:
        r, c = q.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == target_color and neighbor not in visited:
                visited.add(neighbor)
                component_coords.add(neighbor)
                q.append(neighbor)
                
    return component_coords

def find_interior_coords(grid, boundary_coords):
    """
    Finds interior white (0) pixels enclosed by boundary_coords using border flood fill.
    Identifies all white pixels reachable from the grid border without crossing the boundary.
    Any remaining white pixels are considered interior to *some* shape.
    We then verify these potential interior points are adjacent only to the given boundary.
    """
    height, width = grid.shape
    
    # visited_exterior includes the boundary itself to prevent crossing
    visited_exterior = set(boundary_coords) 
    exterior_white = set()
    q = deque()

    # Start BFS from all border white pixels
    for r in range(height):
        for c in [0, width - 1]: # Left and Right borders
            if grid[r, c] == 0 and (r, c) not in visited_exterior:
                visited_exterior.add((r, c))
                q.append((r, c))
    for c in range(width):
         for r in [0, height-1]: # Top and bottom borders (avoid adding corners twice)
             if grid[r,c] == 0 and (r,c) not in visited_exterior:
                 visited_exterior.add((r,c))
                 q.append((r,c))


    # Flood fill to find all exterior white pixels
    while q:
        r, c = q.popleft()
        exterior_white.add((r, c))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and neighbor not in visited_exterior:
                visited_exterior.add(neighbor)
                q.append(neighbor)

    # Potential interior = all white pixels not reached by the exterior flood fill
    potential_interior = set()
    for r in range(height):
        for c in range(width):
            coord = (r, c)
            # Must be white, not part of the boundary itself, and not reachable from outside
            if grid[r, c] == 0 and coord not in boundary_coords and coord not in exterior_white:
                potential_interior.add(coord)

    # Verification step: Ensure potential interior points are contiguous and truly bounded 
    # *only* by the current boundary_coords or other interior points of the same region.
    # This handles cases where potential_interior might span multiple shapes if they are close.
    final_interior = set()
    visited_potential = set()

    for start_r, start_c in potential_interior:
        if (start_r, start_c) in visited_potential or (start_r, start_c) in final_interior:
            continue

        component_q = deque([(start_r, start_c)])
        current_component = set([(start_r, start_c)])
        visited_potential.add((start_r, start_c))
        is_bounded_by_current = True

        while component_q:
            r, c = component_q.popleft()

            # Check neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                neighbor = (nr, nc)

                if not (0 <= nr < height and 0 <= nc < width):
                    # Should not happen if exterior fill was correct, but safety check
                    is_bounded_by_current = False
                    break 
                
                if neighbor in boundary_coords:
                    continue # Neighbor is the correct boundary, OK.
                elif neighbor in potential_interior and neighbor not in visited_potential:
                    visited_potential.add(neighbor)
                    current_component.add(neighbor)
                    component_q.append(neighbor)
                elif neighbor in exterior_white:
                     # This component touches the outside, not interior to this boundary
                     is_bounded_by_current = False
                     break
                elif grid[nr, nc] != 0 and neighbor not in boundary_coords:
                     # This component touches another shape/color, not purely interior to this boundary
                     is_bounded_by_current = False
                     break
                # If neighbor is already visited_potential or part of final_interior, ignore.
            
            if not is_bounded_by_current:
                break # Stop exploring this component

        if is_bounded_by_current:
            # This component is validly interior to the current boundary
            final_interior.update(current_component)
            
    return final_interior


def classify_shape(boundary_coords):
    """Classifies the shape as '5' or 'H' based on structure using heuristics."""
    if not boundary_coords:
        return None

    rows = [r for r, c in boundary_coords]
    cols = [c for r, c in boundary_coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    center_r = min_r + height // 2

    # Heuristic for 'H': Look for a horizontal bar near the middle row
    # and check for vertical segments above and below it.
    
    # Check for roughly continuous horizontal segment near the center row
    has_mid_horizontal_bar = False
    mid_row_pixels = {c for br, bc in boundary_coords if abs(br - center_r) <= height // 4} # Allow some deviation
    if mid_row_pixels:
        min_c_mid = min(mid_row_pixels)
        max_c_mid = max(mid_row_pixels)
        
        # Check if there's a reasonably solid horizontal line near the center
        # Find a row near the center with good horizontal extent
        best_mid_r = -1
        max_span = 0
        for r_check in range(min_r + 1, max_r): # Exclude top/bottom boundary rows
             row_pixels = {c for br, bc in boundary_coords if br == r_check}
             if not row_pixels: continue
             r_min_c, r_max_c = min(row_pixels), max(row_pixels)
             span = r_max_c - r_min_c
             is_connected = all((r_check, c) in boundary_coords for c in range(r_min_c, r_max_c + 1))
             
             # Check if this row is near the center and has decent span and connection
             if abs(r_check - center_r) <= height // 4 and span >= width * 0.5 and is_connected:
                  has_mid_horizontal_bar = True
                  best_mid_r = r_check
                  break # Found a plausible bar

    if has_mid_horizontal_bar:
         # Further check for H: vertical segments above and below the bar near edges
         bar_row_pixels = {c for br, bc in boundary_coords if br == best_mid_r}
         bar_min_c, bar_max_c = min(bar_row_pixels), max(bar_row_pixels)

         # Check for vertical connection near the left end of the bar
         left_connected_above = any((r, bar_min_c) in boundary_coords for r in range(min_r, best_mid_r))
         left_connected_below = any((r, bar_min_c) in boundary_coords for r in range(best_mid_r + 1, max_r + 1))
         
         # Check for vertical connection near the right end of the bar
         right_connected_above = any((r, bar_max_c) in boundary_coords for r in range(min_r, best_mid_r))
         right_connected_below = any((r, bar_max_c) in boundary_coords for r in range(best_mid_r + 1, max_r + 1))

         if (left_connected_above and left_connected_below) and \
            (right_connected_above and right_connected_below):
             return 'H'

    # If the structure doesn't match 'H' heuristics strongly, default to '5' based on examples.
    # A more robust classifier might analyze topology (number of holes) or match templates.
    return '5'


def check_internal_red(input_grid, interior_coords):
    """Checks if any red (2) pixel exists within the interior coordinates in the input grid."""
    for r, c in interior_coords:
        # Need to check bounds just in case interior_coords calculation had edge cases
        if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]:
             if input_grid[r, c] == 2:
                 return True
    return False


def transform(input_grid_list):
    """
    Transforms the input grid by finding red shapes ('5' or 'H'), 
    determining their interior, and filling the interior based on shape type 
    and presence of internal red pixels in the original input.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    visited_shapes = set() # Keep track of red pixels already processed as part of a shape boundary

    # Iterate through the grid to find potential starting points for red shapes
    for r in range(height):
        for c in range(width):
            # If it's a red pixel and hasn't been assigned to a shape boundary yet
            if input_grid[r, c] == 2 and (r, c) not in visited_shapes:
                
                # Find the complete connected component for this red shape boundary
                boundary_coords = find_connected_component(input_grid, (r, c), 2, visited_shapes)

                # Find the interior white pixels enclosed by this specific boundary
                interior_coords = find_interior_coords(input_grid, boundary_coords)

                # Only proceed if we found a non-empty interior for this boundary
                if interior_coords:
                    # Classify the shape based on the boundary's geometry
                    shape_type = classify_shape(boundary_coords)
                    
                    # Check if the *original input grid* had red pixels within this interior area
                    internal_red_present = check_internal_red(input_grid, interior_coords)
                    
                    # Determine the fill color based on the rules
                    fill_color = 0 # Default initialization, will be overwritten
                    apply_fill = True
                    if shape_type == '5':
                        fill_color = 8 # Azure
                    elif shape_type == 'H':
                        if internal_red_present:
                            fill_color = 4 # Yellow
                        else:
                            fill_color = 3 # Green
                    else:
                        # If classification failed (returned None or unexpected value)
                        apply_fill = False 

                    # Fill the identified interior white pixels in the output grid
                    if apply_fill:
                        for ir, ic in interior_coords:
                             # Check bounds again for safety
                             if 0 <= ir < height and 0 <= ic < width:
                                 # IMPORTANT: Only fill if the target pixel in the OUTPUT is currently white (0)
                                 # This preserves any original non-white pixels (like internal red)
                                 if output_grid[ir, ic] == 0: 
                                     output_grid[ir, ic] = fill_color

    # Return the final grid as a list of lists
    return output_grid.tolist()