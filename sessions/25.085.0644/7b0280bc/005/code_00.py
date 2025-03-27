"""
Transforms the input grid based on the following rules:

1.  **Identify Background and Inside Regions:**
    *   The background color (`bg_color`) is determined from the top-left pixel.
    *   A flood fill is performed starting from all `bg_color` pixels on the grid borders. All reachable `bg_color` pixels are marked as 'outside'.
    *   Pixels that are not `bg_color` and not marked 'outside' are considered 'inside'.

2.  **Determine Trigger Color:**
    *   Based on the `bg_color`, a specific `trigger_color` is identified:
        *   If `bg_color` is Azure (8), `trigger_color` is White (0).
        *   If `bg_color` is Maroon (9), `trigger_color` is Yellow (4).
        *   If `bg_color` is Orange (7), `trigger_color` is Magenta (6).
        *   Otherwise, no trigger color is defined.

3.  **Identify Inside Objects:**
    *   Contiguous groups of pixels within the 'inside' region that share the same color (using 4-directional adjacency) are identified as objects. Each object stores its color and the set of coordinates it occupies.

4.  **Identify Trigger Pixels:**
    *   All pixels in the input grid having the `trigger_color` are identified.

5.  **Check and Transform Objects:**
    *   For each 'inside' object:
        a.  **Adjacency Check:** Determine if the object is adjacent (including diagonals, i.e., 8-directional adjacency) to *any* pixel identified as a `trigger_pixel`.
        b.  **Shape Check:** If adjacent to a trigger pixel, determine the shape of the object by calculating its bounding box dimensions (height, width) and the number of pixels it contains. Check if it's a line/dot (height=1 or width=1) or a 2x2 square (height=2, width=2, and 4 pixels).
        c.  **Transformation Rules:** Apply color changes to *all* pixels of the object if it meets the adjacency condition AND its color and shape match the rules defined by the `bg_color`:
            *   **BG=8 (Azure), Trigger=0 (White):**
                *   White(0) line/dot object -> Gray(5)
                *   Red(2) 2x2 object -> Green(3)
            *   **BG=9 (Maroon), Trigger=4 (Yellow):**
                *   Yellow(4) line/dot object -> Gray(5)
                *   Orange(7) 2x2 object -> Green(3)
            *   **BG=7 (Orange), Trigger=6 (Magenta):**
                *   Magenta(6) line/dot object -> Gray(5)
                *   Blue(1) 2x2 object -> Green(3)
        d.  **Update Output:** If a transformation rule applies, update the corresponding pixels in the output grid with the new color.

6.  **Return Output Grid:** The final modified grid is returned.
"""

import collections
import copy

def _find_outside_pixels(grid, bg_color):
    """Performs flood fill from borders to mark outside background pixels."""
    rows = len(grid)
    cols = len(grid[0])
    is_outside = [[False for _ in range(cols)] for _ in range(rows)]
    q = collections.deque()

    # Seed queue with border background pixels
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

    # Flood fill
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
    visited = copy.deepcopy(is_outside) # Start visited with outside pixels
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If not visited and not background -> potential start of an inside object
            if not visited[r][c] and grid[r][c] != bg_color:
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

def _is_adjacent(obj_coords, trigger_pixels, rows, cols):
    """Checks if any pixel in obj_coords is 8-directionally adjacent to a trigger pixel."""
    for r, c in obj_coords:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in trigger_pixels:
                    return True
    return False

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

def transform(input_grid):
    """
    Transforms the input grid by identifying inside objects, checking their adjacency
    to trigger pixels, analyzing their shape, and applying specific color changes.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    if rows == 0 or cols == 0:
        return []

    # 1. Determine background color
    bg_color = input_grid[0][0]

    # 2. Determine Trigger Color based on background
    trigger_color = -1 # Default value if no rule matches
    if bg_color == 8: trigger_color = 0 # white
    elif bg_color == 9: trigger_color = 4 # yellow
    elif bg_color == 7: trigger_color = 6 # magenta

    # 3. Create the output grid
    output_grid = copy.deepcopy(input_grid)

    # 4. Find 'outside' background pixels
    is_outside = _find_outside_pixels(input_grid, bg_color)

    # 5. Find all 'inside' objects
    inside_objects = _find_inside_objects(input_grid, bg_color, is_outside)

    # 6. Identify all trigger pixels in the grid
    trigger_pixels = set()
    if trigger_color != -1:
        for r in range(rows):
            for c in range(cols):
                if input_grid[r][c] == trigger_color:
                    trigger_pixels.add((r, c))

    # 7. Iterate through objects, check conditions, and apply transformations
    for obj in inside_objects:
        obj_color = obj['color']
        obj_coords = obj['coords']

        # Check adjacency to any trigger pixel (8-connectivity)
        is_adj = _is_adjacent(obj_coords, trigger_pixels, rows, cols)

        if is_adj:
            # Determine object shape
            is_line_dot, is_2x2 = _get_object_shape(obj_coords)

            # Apply transformation rules
            new_color = obj_color # Default: no change
            if bg_color == 8:  # Azure background, Trigger White(0)
                if obj_color == 0 and is_line_dot: new_color = 5  # white -> gray
                elif obj_color == 2 and is_2x2: new_color = 3  # red -> green
            elif bg_color == 9:  # Maroon background, Trigger Yellow(4)
                if obj_color == 4 and is_line_dot: new_color = 5  # yellow -> gray
                elif obj_color == 7 and is_2x2: new_color = 3  # orange -> green
            elif bg_color == 7:  # Orange background, Trigger Magenta(6)
                if obj_color == 6 and is_line_dot: new_color = 5  # magenta -> gray
                elif obj_color == 1 and is_2x2: new_color = 3  # blue -> green

            # Update the output grid if the color changed
            if new_color != obj_color:
                for r, c in obj_coords:
                    output_grid[r][c] = new_color

    # 8. Return the transformed grid
    return output_grid