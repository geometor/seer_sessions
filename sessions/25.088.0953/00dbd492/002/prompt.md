
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies closed shapes formed by red (2) pixels in the input grid.
These shapes resemble either a digit '5' or a letter 'H'.
The transformation involves filling the area enclosed by these red shapes with a specific color, 
while leaving the red outline and the exterior background (white - 0) unchanged. 
The fill color depends on the shape type ('5' or 'H') and whether the shape contains an internal 
red pixel (2) in the input grid.

Rules:
1. Find all connected components of red (2) pixels.
2. For each component, determine the set of enclosed white (0) pixels (interior).
3. If an interior exists:
    a. Classify the red shape boundary as '5' or 'H'.
    b. Check if any red (2) pixel exists within the interior region in the *input* grid.
    c. Determine the fill color:
        - If shape is '5', fill color is azure (8).
        - If shape is 'H' and has internal red, fill color is yellow (4).
        - If shape is 'H' and has no internal red, fill color is green (3).
    d. Fill the interior white (0) pixels in the *output* grid with the determined fill color.
4. Pixels not part of an enclosed interior remain unchanged.
"""

def find_connected_component(grid, start_coord, target_color, visited):
    """Finds all coordinates of a connected component of target_color using BFS."""
    height, width = grid.shape
    q = deque([start_coord])
    component_coords = set()
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
    Finds interior white (0) pixels enclosed by boundary_coords.
    Uses BFS starting from white neighbors of the boundary to identify exterior white pixels.
    Any remaining white pixels not reachable from the outside are interior.
    """
    height, width = grid.shape
    exterior_white = set()
    q = deque()
    visited_flood = set()

    # Find initial white pixels adjacent to the boundary or grid edges
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 0:
                is_boundary_neighbor = False
                is_edge_pixel = (r == 0 or r == height - 1 or c == 0 or c == width - 1)
                
                # Check adjacency to boundary_coords
                if not is_edge_pixel:
                     for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1,-1)]: # Check diagonals too for safety
                         nr, nc = r + dr, c + dc
                         if (nr, nc) in boundary_coords:
                             is_boundary_neighbor = True
                             break
                
                # Start BFS from edge white pixels or white pixels adjacent to the *current* boundary
                if (is_edge_pixel or is_boundary_neighbor) and (r, c) not in visited_flood:
                    q.append((r, c))
                    visited_flood.add((r,c))
                    exterior_white.add((r,c))

    # Perform BFS to find all reachable exterior white pixels
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and neighbor not in boundary_coords and \
               neighbor not in visited_flood:
                 visited_flood.add(neighbor)
                 exterior_white.add(neighbor)
                 q.append(neighbor)

    # Identify interior pixels: white pixels not in exterior_white and not on the boundary
    interior_coords = set()
    for r in range(height):
        for c in range(width):
            coord = (r, c)
            if grid[r, c] == 0 and coord not in exterior_white and coord not in boundary_coords:
                # Double check it's truly enclosed by *this* boundary
                # Perform a quick check: are all non-zero, non-boundary neighbours part of this boundary?
                is_truly_interior = True
                q_check = deque([coord])
                visited_check = {coord}
                component_check = {coord}
                connected_to_outside_or_other_shape = False

                while q_check:
                    cr,cc = q_check.popleft()
                    is_near_target_boundary = False
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nr, nc = cr + dr, cc + dc
                         neighbor = (nr, nc)

                         if not (0 <= nr < height and 0 <= nc < width):
                             connected_to_outside_or_other_shape = True
                             break
                         
                         if neighbor in boundary_coords:
                             is_near_target_boundary = True
                         elif grid[nr, nc] == 0 and neighbor not in visited_check:
                             q_check.append(neighbor)
                             visited_check.add(neighbor)
                             component_check.add(neighbor)
                         elif grid[nr, nc] != 0 and neighbor not in boundary_coords: # Hits another color/shape
                            connected_to_outside_or_other_shape = True
                            break
                    if connected_to_outside_or_other_shape:
                        break
                
                # If the flood fill from this point stayed within white cells OR hit only the target boundary, it's interior
                if not connected_to_outside_or_other_shape and is_near_target_boundary:
                     interior_coords.update(component_check) # Add the whole component found

    # Refine: Ensure interior pixels are contiguous and actually bounded by the specific boundary_coords.
    # The above check is an attempt, but might still incorrectly identify interiors if shapes are complex/adjacent.
    # A truly robust method often involves winding numbers or point-in-polygon tests on the boundary.
    # Given ARC constraints, the BFS from exterior might be sufficient if shapes are well-separated.
    
    # Let's retry the simple definition: White cells not reachable from the outside.
    all_interior = set()
    for r in range(height):
        for c in range(width):
             coord = (r,c)
             if grid[r,c] == 0 and coord not in exterior_white and coord not in boundary_coords:
                 all_interior.add(coord)
                 
    # Now, verify these potential interior points are connected and adjacent only to the boundary or other interior points
    final_interior = set()
    visited_final = set()
    for r_start, c_start in all_interior:
        if (r_start, c_start) in visited_final:
            continue

        current_component = set()
        q_final = deque([(r_start, c_start)])
        visited_final.add((r_start, c_start))
        is_bounded_by_current_shape = True
        
        while q_final:
            r,c = q_final.popleft()
            current_component.add((r,c))

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                 nr, nc = r + dr, c + dc
                 neighbor = (nr, nc)
                 
                 if not (0 <= nr < height and 0 <= nc < width): # Should not happen if exterior fill worked
                     is_bounded_by_current_shape = False
                     break

                 if neighbor in boundary_coords:
                     continue # It's bounded by the shape, that's okay.
                 elif neighbor in all_interior and neighbor not in visited_final:
                     visited_final.add(neighbor)
                     q_final.append(neighbor)
                 elif neighbor not in all_interior and grid[nr,nc] == 0: # Hits exterior white
                     is_bounded_by_current_shape = False
                     break
                 elif grid[nr,nc] != 0 and neighbor not in boundary_coords: # Hits another shape/color
                      is_bounded_by_current_shape = False
                      break
            if not is_bounded_by_current_shape:
                 break # This component is not validly interior to this boundary
        
        if is_bounded_by_current_shape:
             final_interior.update(current_component)


    return final_interior


def classify_shape(boundary_coords):
    """Classifies the shape as '5' or 'H' based on structure."""
    if not boundary_coords:
        return None

    rows = [r for r, c in boundary_coords]
    cols = [c for r, c in boundary_coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Heuristic for 'H': Look for a horizontal bar near the middle row
    # that is not the top or bottom edge and connects points near min_c and max_c.
    mid_r_area = range(min_r + height // 3, max_r - height // 3 + 1)
    
    has_mid_horizontal_bar = False
    for r in mid_r_area:
         # Check if row 'r' contains red pixels spanning a significant width
         row_pixels = {c for br, bc in boundary_coords if br == r}
         if not row_pixels:
             continue
         
         min_c_row, max_c_row = min(row_pixels), max(row_pixels)
         # Check for continuity across the middle
         is_continuous = True
         for c in range(min_c_row, max_c_row + 1):
             if (r, c) not in boundary_coords:
                 is_continuous = False
                 break
         # Check if it spans a good portion of the width and isn't top/bottom boundary element
         if is_continuous and (max_c_row - min_c_row + 1) > width / 2 and r != min_r and r != max_r:
             has_mid_horizontal_bar = True
             break
             
    if has_mid_horizontal_bar:
        # Further check: Does it connect two vertical segments?
        # Look for vertical segments above and below the bar near min_c and max_c
        has_left_vertical = any((r_check, min_c_row) in boundary_coords for r_check in range(min_r, r)) and \
                            any((r_check, min_c_row) in boundary_coords for r_check in range(r + 1, max_r + 1))
        has_right_vertical = any((r_check, max_c_row) in boundary_coords for r_check in range(min_r, r)) and \
                             any((r_check, max_c_row) in boundary_coords for r_check in range(r + 1, max_r + 1))
        
        if has_left_vertical and has_right_vertical:
             return 'H'

    # If not clearly 'H', assume '5' based on the examples provided
    return '5'


def check_internal_red(input_grid, interior_coords):
    """Checks if any red (2) pixel exists within the interior coordinates."""
    for r, c in interior_coords:
        if input_grid[r, c] == 2:
            return True
    return False


def transform(input_grid):
    """
    Transforms the input grid by finding red shapes ('5' or 'H'), 
    determining their interior, and filling the interior based on shape type 
    and presence of internal red pixels.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    visited_shapes = set() # Keep track of red pixels already processed as part of a shape

    # Iterate through the grid to find potential starting points for red shapes
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 2 and (r, c) not in visited_shapes:
                # Found a potential start of a red shape, find its connected component
                boundary_coords = find_connected_component(input_grid, (r, c), 2, visited_shapes)

                # Find the interior pixels enclosed by this boundary
                # Pass the original grid and the found boundary
                interior_coords = find_interior_coords(input_grid, boundary_coords)

                # If interior pixels exist, process this shape
                if interior_coords:
                    # Classify the shape based on the boundary
                    shape_type = classify_shape(boundary_coords)
                    
                    # Check if the *input* grid had red pixels in the interior area
                    internal_red_present = check_internal_red(input_grid, interior_coords)
                    
                    # Determine the fill color based on the rules
                    fill_color = 0 # Default to white (shouldn't happen if interior_coords exist)
                    if shape_type == '5':
                        fill_color = 8 # Azure
                    elif shape_type == 'H':
                        if internal_red_present:
                            fill_color = 4 # Yellow
                        else:
                            fill_color = 3 # Green
                    else:
                        # Should not happen for valid inputs based on examples
                        # If classification failed, maybe leave interior as is or use a default?
                        # Let's skip filling if classification fails.
                        continue 

                    # Fill the interior white pixels in the output grid
                    for ir, ic in interior_coords:
                        # Only fill if the pixel is currently white (0)
                        # This preserves any original internal red pixels
                        if output_grid[ir, ic] == 0: 
                            output_grid[ir, ic] = fill_color

    return output_grid.tolist() # Return as list of lists per ARC standard
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 2 2 2 2 0 0
2 0 0 0 2 0 0
2 0 2 0 2 0 0
2 0 0 0 2 0 0
2 2 2 2 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Expected Output:
```
2 2 2 2 2 0 0
2 8 8 8 2 0 0
2 8 2 8 2 0 0
2 8 8 8 2 0 0
2 2 2 2 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Transformed Output:
```
2 2 2 2 2 0 0
2 0 0 0 2 0 0
2 0 2 0 2 0 0
2 0 0 0 2 0 0
2 2 2 2 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 32.65306122448979

## Example 2:
Input:
```
2 2 2 2 2 2 2 0 0
2 0 0 0 0 0 2 0 0
2 0 0 0 0 0 2 0 0
2 0 0 2 0 0 2 0 0
2 0 0 0 0 0 2 0 0
2 0 0 0 0 0 2 0 0
2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 2 2 2 2 2 2 0 0
2 4 4 4 4 4 2 0 0
2 4 4 4 4 4 2 0 0
2 4 4 2 4 4 2 0 0
2 4 4 4 4 4 2 0 0
2 4 4 4 4 4 2 0 0
2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
2 2 2 2 2 2 2 0 0
2 0 0 0 0 0 2 0 0
2 0 0 0 0 0 2 0 0
2 0 0 2 0 0 2 0 0
2 0 0 0 0 0 2 0 0
2 0 0 0 0 0 2 0 0
2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 59.25925925925927

## Example 3:
Input:
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 2 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0 0 0
0 2 0 2 0 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 2 3 3 3 3 3 3 3 2
0 0 0 0 0 0 2 3 3 3 3 3 3 3 2
0 0 0 0 0 0 2 3 3 3 3 3 3 3 2
0 0 0 0 0 0 2 3 3 3 2 3 3 3 2
0 0 0 0 0 0 2 3 3 3 3 3 3 3 2
0 0 0 0 0 0 2 3 3 3 3 3 3 3 2
0 0 0 0 0 0 2 3 3 3 3 3 3 3 2
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 2 8 8 8 2 0 0 0 0 0 0 0 0 0
0 2 8 2 8 2 0 0 0 0 0 0 0 0 0
0 2 8 8 8 2 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 2 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0 0 0
0 2 0 2 0 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 56
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 49.7777777777778

## Example 4:
Input:
```
0 2 2 2 2 2 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0
0 2 0 2 0 2 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0
0 0 0 0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 2 0 0 2 0 0 2 0
0 0 0 0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 2 2 2 2 2 2 2 0
```
Expected Output:
```
0 2 2 2 2 2 0 0 0 0 0 0 0
0 2 8 8 8 2 0 0 0 0 0 0 0
0 2 8 2 8 2 0 0 0 0 0 0 0
0 2 8 8 8 2 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0
0 0 0 0 0 2 4 4 4 4 4 2 0
0 0 0 0 0 2 4 4 4 4 4 2 0
0 0 0 0 0 2 4 4 2 4 4 2 0
0 0 0 0 0 2 4 4 4 4 4 2 0
0 0 0 0 0 2 4 4 4 4 4 2 0
0 0 0 0 0 2 2 2 2 2 2 2 0
```
Transformed Output:
```
0 2 2 2 2 2 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0
0 2 0 2 0 2 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0
0 0 0 0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 2 0 0 2 0 0 2 0
0 0 0 0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 2 2 2 2 2 2 2 0
```
Match: False
Pixels Off: 32
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 37.869822485207095
