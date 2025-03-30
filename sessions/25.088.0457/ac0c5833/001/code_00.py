import numpy as np
from collections import deque

"""
Identifies a specific "source" red object pattern based on its adjacency to a unique, isolated yellow pixel.
Identifies all occurrences of a horizontal "target" pattern (yellow-white-yellow: 4-0-4).
Copies the source red object pattern and places it onto the output grid relative to each target pattern found.
The placement rule is: the top-left corner of the source object's bounding box is placed 2 rows below and 1 column to the right 
of the first yellow pixel of the target pattern. The copied pixels overwrite existing pixels.
Pixels not part of the source object or target patterns remain unchanged.
"""

def find_connected_components(grid, color):
    """Finds all connected components of a given color in the grid."""
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    components = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                component = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    component.add((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if component:
                    components.append(component)
    return components

def get_bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    if not pixels:
        return None
    min_r = min(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_r = max(r for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, min_c, max_r, max_c

def get_relative_pixels(pixels, min_r, min_c):
    """Converts absolute pixel coordinates to coordinates relative to a top-left corner."""
    return set((r - min_r, c - min_c) for r, c in pixels)

def get_adjacent_coords(r, c, height, width, include_diagonal=True):
    """Gets valid neighbor coordinates for a given cell."""
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if not include_diagonal and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Applies the transformation rule: copy a specific red pattern identified by an adjacent yellow pixel
    to locations marked by a yellow-white-yellow pattern.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    red_color = 2
    yellow_color = 4
    white_color = 0

    # 1. Find all red objects and map pixels to their objects
    red_objects = find_connected_components(input_grid, red_color)
    if not red_objects:
        return output_grid # No red objects, nothing to copy

    pixel_to_red_object = {
        pixel: obj_set for obj_set in red_objects for pixel in obj_set
    }

    # 2. Identify potential "isolated" yellow pixels (not part of the 4-0-4 target)
    isolated_yellows = []
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == yellow_color:
                is_target_part = False
                # Check if it's the first '4' in '4 0 4'
                if c <= width - 3 and input_grid[r, c+1] == white_color and input_grid[r, c+2] == yellow_color:
                    is_target_part = True
                # Check if it's the second '4' in '4 0 4'
                if c >= 2 and input_grid[r, c-1] == white_color and input_grid[r, c-2] == yellow_color:
                    is_target_part = True
                
                if not is_target_part:
                    isolated_yellows.append((r, c))

    # 3. Identify the source red object
    # It's the one adjacent (including diagonals) to exactly one isolated yellow pixel
    source_object_pixels = None
    source_object_found = False
    
    # Check each isolated yellow pixel for unique adjacency to a red object
    for yr, yc in isolated_yellows:
        adjacent_red_object_sets = set() # Store hashable representations of adjacent red objects
        neighbors = get_adjacent_coords(yr, yc, height, width, include_diagonal=True)

        for nr, nc in neighbors:
            if input_grid[nr, nc] == red_color:
                if (nr, nc) in pixel_to_red_object:
                    obj_set = pixel_to_red_object[(nr, nc)]
                    # Convert set to a hashable type (tuple of sorted coords)
                    adjacent_red_object_sets.add(tuple(sorted(list(obj_set))))

        # If this yellow pixel is adjacent to exactly one unique red object
        if len(adjacent_red_object_sets) == 1:
             # Check if this red object is adjacent to *only* this yellow pixel among all isolated yellows
             candidate_object_tuple = list(adjacent_red_object_sets)[0]
             candidate_object_pixels = set(candidate_object_tuple)
             
             adjacent_isolated_yellow_count = 0
             all_adj_coords = set()
             for pr, pc in candidate_object_pixels:
                 all_adj_coords.update(get_adjacent_coords(pr, pc, height, width, include_diagonal=True))
                 
             for ar, ac in all_adj_coords:
                 if (ar, ac) in isolated_yellows:
                     adjacent_isolated_yellow_count += 1
                     
             if adjacent_isolated_yellow_count == 1:
                 source_object_pixels = candidate_object_pixels
                 source_object_found = True
                 break # Found the source object

    if not source_object_found:
        # Fallback or error handling: Maybe check red objects directly
        # Find red object adjacent to exactly one isolated yellow
        for obj_pixels in red_objects:
             adjacent_yellows_count = 0
             all_adj_coords = set()
             for pr, pc in obj_pixels:
                 all_adj_coords.update(get_adjacent_coords(pr, pc, height, width, include_diagonal=True))
             
             num_adjacent_isolated_yellows = 0
             for ar, ac in all_adj_coords:
                 # Need to check if (ar,ac) is in the list of *isolated* yellows
                 if (ar,ac) in isolated_yellows:
                      num_adjacent_isolated_yellows += 1

             if num_adjacent_isolated_yellows == 1:
                 source_object_pixels = obj_pixels
                 source_object_found = True
                 break # Found source with fallback


    if not source_object_found or source_object_pixels is None:
       # print("Warning: Source red object could not be definitively identified.")
        return output_grid # Return original if source cannot be found

    # 4. Get the relative shape of the source object
    src_bb = get_bounding_box(source_object_pixels)
    if src_bb is None:
        return output_grid # Should not happen if source_object_found is True
        
    src_min_r, src_min_c, _, _ = src_bb
    relative_shape = get_relative_pixels(source_object_pixels, src_min_r, src_min_c)

    # 5. Find all target pattern locations (top-left of the first '4')
    target_coords = []
    for r in range(height):
        for c in range(width - 2): # Ensure space for pattern '4 0 4'
            if (input_grid[r, c] == yellow_color and
                input_grid[r, c+1] == white_color and
                input_grid[r, c+2] == yellow_color):
                target_coords.append((r, c))

    # 6. Place copies of the source object at target locations
    for r_target, c_target in target_coords:
        # Calculate the anchor point for the copy (top-left of the placed object)
        # Offset is +2 rows, +1 column from the *first* yellow pixel (r_target, c_target)
        anchor_r = r_target + 2
        anchor_c = c_target + 1

        # Place the object relative to the anchor point
        for dr, dc in relative_shape:
            final_r = anchor_r + dr
            final_c = anchor_c + dc

            # Check bounds before writing to the output grid
            if 0 <= final_r < height and 0 <= final_c < width:
                output_grid[final_r, final_c] = red_color

    return output_grid