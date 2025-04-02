import numpy as np
from collections import deque

"""
This transformation rule processes a grid containing a background color (yellow, 4) and one or more shapes made of blue pixels (1).

The rule performs the following steps:
1. Initialize the output grid as a copy of the input grid.
2. Identify all distinct contiguous regions (shapes) of blue pixels in the input grid.
3. For each identified blue shape:
    a. Find all yellow pixels immediately adjacent (including diagonals) to the blue shape. Change these pixels to red (2) in the output grid, forming a border.
    b. Determine if the original blue shape encloses any regions of yellow pixels (holes). This is done by finding all yellow pixels not reachable from the grid's outer border.
    c. If the shape encloses holes:
        i. Change all pixels corresponding to the original blue shape to azure (8) in the output grid.
        ii. Change all yellow pixels determined to be within holes enclosed by this shape to magenta (6) in the output grid.
    d. If the shape does not enclose any holes:
        i. Leave the pixels corresponding to the original blue shape as blue (1) in the output grid.
4. Yellow pixels that are part of the exterior background and are not turned into border pixels remain yellow (4).
"""

def get_neighbors(r, c, height, width, connectivity=8):
    """Gets valid neighbor coordinates."""
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if connectivity == 4 and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_connected_components(grid, target_color):
    """Finds all connected components of a specific color."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []
    pixel_to_component_id = {}
    component_id_counter = 0

    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and not visited[r, c]:
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_id = component_id_counter
                
                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.add((curr_r, curr_c))
                    pixel_to_component_id[(curr_r, curr_c)] = component_id
                    
                    # Use 4-connectivity for finding components of the same color
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width, connectivity=4):
                        if grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if component_coords:
                    components.append(component_coords)
                    component_id_counter += 1
                    
    return components, pixel_to_component_id

def find_exterior_pixels(grid, background_color):
    """Finds all background pixels reachable from the border."""
    height, width = grid.shape
    exterior_pixels = set()
    q = deque()
    visited_flood = np.zeros_like(grid, dtype=bool)

    # Add border background pixels to the queue
    for r in range(height):
        for c in [0, width - 1]:
            if grid[r, c] == background_color and not visited_flood[r,c]:
                q.append((r, c))
                visited_flood[r,c] = True
                exterior_pixels.add((r, c))
    for c in range(width):
        for r in [0, height - 1]:
             if grid[r, c] == background_color and not visited_flood[r,c]:
                q.append((r, c))
                visited_flood[r,c] = True
                exterior_pixels.add((r, c))

    # Flood fill from the border
    while q:
        curr_r, curr_c = q.popleft()
        # Use 4-connectivity for flood fill within background
        for nr, nc in get_neighbors(curr_r, curr_c, height, width, connectivity=4):
            if grid[nr, nc] == background_color and not visited_flood[nr, nc]:
                visited_flood[nr, nc] = True
                exterior_pixels.add((nr, nc))
                q.append((nr, nc))
                
    return exterior_pixels


def transform(input_grid):
    """
    Transforms the input grid based on bordering and filling blue shapes.
    Holes within shapes are filled with magenta, and the shape itself becomes azure.
    Solid shapes remain blue. Borders become red.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    
    background_color = 4
    shape_color = 1
    border_color = 2
    hole_fill_color = 6
    shape_with_hole_color = 8

    # 1. Find all blue shapes
    blue_shapes, pixel_to_shape_id = find_connected_components(input_np, shape_color)

    if not blue_shapes: # No blue shapes, return original grid
        return output_grid.tolist()

    # 2. Find all exterior yellow pixels
    exterior_yellow = find_exterior_pixels(input_np, background_color)

    # 3. Identify all hole pixels (yellow pixels not reachable from outside)
    all_hole_pixels = set()
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == background_color and (r, c) not in exterior_yellow:
                all_hole_pixels.add((r, c))

    # 4. Determine which shapes have holes and find border pixels
    shape_has_holes = [False] * len(blue_shapes)
    all_border_pixels = set()
    shape_borders = [set() for _ in blue_shapes]
    shape_adjacent_holes = [set() for _ in blue_shapes]

    for shape_id, shape_coords in enumerate(blue_shapes):
        current_border = set()
        for r, c in shape_coords:
            # Check 8 neighbors for border potential
            for nr, nc in get_neighbors(r, c, height, width, connectivity=8):
                if input_np[nr, nc] == background_color:
                    current_border.add((nr, nc))
                
                # Check if this blue pixel is adjacent to a hole pixel
                if (nr, nc) in all_hole_pixels:
                    shape_has_holes[shape_id] = True
                    # Associate this hole pixel with the current shape
                    shape_adjacent_holes[shape_id].add((nr,nc)) 

        shape_borders[shape_id] = current_border
        all_border_pixels.update(current_border)
        
        # Also need to check if any border pixel is adjacent to a hole pixel
        # This covers cases where hole pixels don't touch the main shape body directly
        for br, bc in current_border:
             for nr, nc in get_neighbors(br, bc, height, width, connectivity=8):
                 if (nr,nc) in all_hole_pixels:
                     # Check if this hole pixel is *only* reachable via this shape's area
                     # This check is complex. Let's assume adjacency implies belonging for now.
                     # A more robust check might involve flood-filling the hole and seeing which shape(s) surround it.
                     # Simplification: if a shape's border touches a hole pixel, we associate the hole pixel with the shape.
                     shape_has_holes[shape_id] = True
                     shape_adjacent_holes[shape_id].add((nr,nc))


    # 5. Create the output grid based on findings
    
    # Process shapes and their associated holes
    for shape_id, shape_coords in enumerate(blue_shapes):
        fill_color = shape_with_hole_color if shape_has_holes[shape_id] else shape_color
        for r, c in shape_coords:
            output_grid[r, c] = fill_color
            
        # Fill the holes associated with this shape
        if shape_has_holes[shape_id]:
            # Find *all* connected hole pixels starting from those adjacent to the shape
            visited_holes = set()
            hole_q = deque(list(shape_adjacent_holes[shape_id]))
            all_connected_hole_pixels_for_shape = set()

            while hole_q:
                hr, hc = hole_q.popleft()
                if (hr, hc) not in all_hole_pixels or (hr, hc) in visited_holes:
                    continue
                
                visited_holes.add((hr, hc))
                all_connected_hole_pixels_for_shape.add((hr, hc))
                
                # Explore neighbors within the hole region (4-connectivity is usually sufficient for filling)
                for nr, nc in get_neighbors(hr, hc, height, width, connectivity=4):
                    if (nr, nc) in all_hole_pixels and (nr, nc) not in visited_holes:
                        hole_q.append((nr, nc))
                        
            # Now fill these identified hole pixels
            for hr, hc in all_connected_hole_pixels_for_shape:
                 output_grid[hr, hc] = hole_fill_color


    # Place the borders (do this last to overwrite any mis-filled holes if logic was imperfect)
    for br, bc in all_border_pixels:
         # Only draw border over original background or holes that might have been adjacent
         if input_np[br, bc] == background_color or (br, bc) in all_hole_pixels:
             output_grid[br, bc] = border_color


    return output_grid.tolist()