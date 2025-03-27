"""
Transforms the input grid based on the following rules:

1.  **Determine Context:** Identify the `background_color` from the top-left pixel. Based on this, determine the `trigger_color`: Azure(8)->White(0), Maroon(9)->Yellow(4), Orange(7)->Magenta(6).
2.  **Identify Regions:**
    *   `outside_region`: Flood fill (4-way) from border `background_color` pixels to find all reachable `background_color` pixels.
    *   `inside_region`: All pixels not `background_color` and not in `outside_region`.
3.  **Find Objects and Triggers:**
    *   `inside_objects`: Contiguous groups (4-way) of same-colored pixels in the `inside_region`. Note color, coordinates, and shape (line/dot or 2x2 square).
    *   `trigger_pixels`: Coordinates of all pixels with the `trigger_color`.
4.  **Apply Transformation:**
    *   Iterate through each `inside_object`.
    *   Check if the object's color/shape matches transformation rules for the `background_color`:
        *   BG=8: White(0) line/dot -> Gray(5); Red(2) 2x2 -> Green(3).
        *   BG=9: Yellow(4) line/dot -> Gray(5); Orange(7) 2x2 -> Green(3).
        *   BG=7: Magenta(6) line/dot -> Gray(5); Blue(1) 2x2 -> Green(3).
    *   If applicable, check if any pixel of the object is adjacent (8-way) to a `trigger_pixel`, AND if at least one such adjacent `trigger_pixel` is itself adjacent (4-way) to a pixel in the `outside_region`.
    *   If both conditions are met, change the color of all pixels of the object in the output grid according to the rule.
5.  Return the modified grid.
"""

import collections
import copy

def _find_outside_pixels(grid, bg_color):
    """Performs flood fill from borders to mark outside background pixels."""
    rows = len(grid)
    cols = len(grid[0])
    is_outside = [[False for _ in range(cols)] for _ in range(rows)]
    q = collections.deque()

    # Seed queue with border background pixels (4-directional adjacency check)
    for r in range(rows):
        for c in [0, cols - 1]:
            if not is_outside[r][c] and grid[r][c] == bg_color:
                is_outside[r][c] = True
                q.append((r, c))
    for c in range(1, cols - 1):
        for r in [0, rows - 1]:
            if not is_outside[r][c] and grid[r][c] == bg_color:
                is_outside[r][c] = True
                q.append((r, c))

    # Flood fill (4-directional)
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               not is_outside[nr][nc] and grid[nr][nc] == bg_color:
                is_outside[nr][nc] = True
                q.append((nr, nc))
    return is_outside

def _find_inside_objects(grid, bg_color, is_outside):
    """Finds all contiguous objects within the 'inside' region."""
    rows = len(grid)
    cols = len(grid[0])
    # Mark all background and outside pixels as visited initially
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == bg_color or is_outside[r][c]:
                 visited[r][c] = True

    objects = []
    for r in range(rows):
        for c in range(cols):
            # If not visited -> potential start of an inside object
            if not visited[r][c]:
                obj_color = grid[r][c]
                obj_coords = set()
                q = collections.deque([(r, c)])
                visited[r][c] = True

                # BFS to find all connected pixels of the same color (4-connectivity)
                while q:
                    curr_r, curr_c = q.popleft()
                    obj_coords.add((curr_r, curr_c))

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr][nc] and grid[nr][nc] == obj_color:
                            visited[nr][nc] = True
                            q.append((nr, nc))

                if obj_coords:
                   objects.append({'color': obj_color, 'coords': obj_coords})

    return objects

def _get_object_shape(obj_coords):
    """Determines if an object is a line/dot or a 2x2 square."""
    if not obj_coords:
        return False, False

    min_r = min(r for r, c in obj_coords)
    max_r = max(r for r, c in obj_coords)
    min_c = min(c for r, c in obj_coords)
    max_c = max(c for r, c in obj_coords)

    height = max_r - min_r + 1
    width = max_c - min_c + 1
    num_pixels = len(obj_coords)

    is_line_dot = (height == 1 or width == 1)
    is_2x2 = (height == 2 and width == 2 and num_pixels == 4)

    return is_line_dot, is_2x2

def _check_adjacency_to_outside_trigger(obj_coords, trigger_pixels, is_outside, rows, cols):
    """
    Checks if any pixel in obj_coords is 8-directionally adjacent to a trigger pixel,
    AND that trigger pixel is 4-directionally adjacent to an 'outside' background pixel.
    """
    # Iterate through each pixel coordinate of the object
    for r, c in obj_coords:
        # Check its 8 neighbors (including diagonals)
        for dr_obj in [-1, 0, 1]:
            for dc_obj in [-1, 0, 1]:
                if dr_obj == 0 and dc_obj == 0:
                    continue # Skip the pixel itself
                nr_trig, nc_trig = r + dr_obj, c + dc_obj

                # Check if the neighbor is within bounds and is a trigger pixel
                if 0 <= nr_trig < rows and 0 <= nc_trig < cols and (nr_trig, nc_trig) in trigger_pixels:
                    # Now check if this trigger pixel is adjacent (4-way) to an 'outside' pixel
                    for dr_trig, dc_trig in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr_out, nc_out = nr_trig + dr_trig, nc_trig + dc_trig
                        # Check bounds and if the neighbor is marked as 'outside'
                        if 0 <= nr_out < rows and 0 <= nc_out < cols and is_outside[nr_out][nc_out]:
                            return True # Found the required condition, no need to check further

    return False # No object pixel met the combined adjacency condition

def transform(input_grid):
    rows = len(input_grid)
    cols = len(input_grid[0])
    if rows == 0 or cols == 0:
        return []

    # 1. Initialize output grid
    output_grid = copy.deepcopy(input_grid)

    # 2. Determine background color
    bg_color = input_grid[0][0]

    # 3. Determine Trigger Color based on background
    trigger_color = -1 # Default value if no rule matches
    if bg_color == 8: trigger_color = 0 # white
    elif bg_color == 9: trigger_color = 4 # yellow
    elif bg_color == 7: trigger_color = 6 # magenta

    # If no trigger color rule applies, return the original grid
    if trigger_color == -1:
        return output_grid

    # 4. Find 'outside' background pixels
    is_outside = _find_outside_pixels(input_grid, bg_color)

    # 5. Find all 'inside' objects (not background, not outside)
    inside_objects = _find_inside_objects(input_grid, bg_color, is_outside)

    # 6. Identify all trigger pixels in the grid
    trigger_pixels = set()
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == trigger_color:
                trigger_pixels.add((r, c))

    # 7. Iterate through objects, check conditions, and apply transformations
    for obj in inside_objects:
        obj_color = obj['color']
        obj_coords = obj['coords']

        # Determine object shape
        is_line_dot, is_2x2 = _get_object_shape(obj_coords)

        # Check if this object matches transformation rules based on BG color
        relevant_object = False
        potential_new_color = obj_color # Default: no change
        if bg_color == 8:  # Azure background, Trigger White(0)
            if obj_color == 0 and is_line_dot: relevant_object = True; potential_new_color = 5  # white -> gray
            elif obj_color == 2 and is_2x2: relevant_object = True; potential_new_color = 3  # red -> green
        elif bg_color == 9:  # Maroon background, Trigger Yellow(4)
            if obj_color == 4 and is_line_dot: relevant_object = True; potential_new_color = 5  # yellow -> gray
            elif obj_color == 7 and is_2x2: relevant_object = True; potential_new_color = 3  # orange -> green
        elif bg_color == 7:  # Orange background, Trigger Magenta(6)
            if obj_color == 6 and is_line_dot: relevant_object = True; potential_new_color = 5  # magenta -> gray
            elif obj_color == 1 and is_2x2: relevant_object = True; potential_new_color = 3  # blue -> green

        # If the object is relevant, check the refined adjacency condition
        if relevant_object:
            should_transform = _check_adjacency_to_outside_trigger(obj_coords, trigger_pixels, is_outside, rows, cols)

            # Apply transformation if the adjacency condition is met
            if should_transform:
                for r, c in obj_coords:
                    output_grid[r][c] = potential_new_color

    # 8. Return the transformed grid
    return output_grid