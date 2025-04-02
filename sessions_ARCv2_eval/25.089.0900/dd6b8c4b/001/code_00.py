import numpy as np
from collections import deque

"""
Transformation Rule:

1.  Identify the unique red (2) pixel in the grid. If none exists, return the input grid unchanged.
2.  Identify the 'core object', which consists of the red pixel and all green (3) pixels connected to it (including diagonally, potentially through other green pixels).
3.  Identify the 'border pixels': all pixels adjacent (including diagonally) to any green pixel of the core object, but which are not part of the core object themselves (i.e., not the red pixel or the connected green pixels).
4.  Analyze the border pixels:
    a.  If *all* border pixels are magenta (6):
        i.  Check if any maroon (9) pixel in the entire grid is adjacent (including diagonally) to any of the magenta (6) border pixels.
        ii. If such an adjacent maroon pixel exists, change *all* green (3) pixels within the core object to maroon (9).
        iii. Otherwise (no adjacent maroon pixel), change only those green (3) pixels in the core object that are located above the red pixel, or in the same row but to the left of the red pixel, to maroon (9).
    b.  If the border pixels are *not* all magenta (6) (e.g., contain orange (7) or other colors):
        i.  Change only those green (3) pixels in the core object that are located above the red pixel, or in the same row but to the left of the red pixel, to maroon (9).
5.  All other pixels (the red pixel, background pixels, original maroon pixels, magenta pixels not part of the border, etc.) remain unchanged.
"""

def get_neighbors(r, c, height, width, include_diagonals=True):
    """ Gets valid neighbor coordinates for a pixel (r, c). """
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if not include_diagonals and (dr != 0 and dc != 0):
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_pixel(grid, target_color):
    """ Finds the first occurrence of a pixel with the target_color. """
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color:
                return r, c
    return None

def find_core_object(grid, start_r, start_c):
    """ Finds the red pixel and all connected green pixels. """
    height, width = grid.shape
    q = deque([(start_r, start_c)])
    visited = set([(start_r, start_c)])
    core_object_coords = set([(start_r, start_c)]) # Include the red pixel itself
    green_coords = set()

    # Search starts from the red pixel to find adjacent green ones
    search_q = deque(get_neighbors(start_r, start_c, height, width, include_diagonals=True))
    initial_green_visited = set([(start_r, start_c)]) # Prevent revisiting red

    while search_q:
        r, c = search_q.popleft()
        if (r,c) in initial_green_visited:
             continue
        initial_green_visited.add((r,c))

        if grid[r, c] == 3: # Found a green pixel connected to red
            # Now perform BFS/DFS from this green pixel to find all connected greens
            component_q = deque([(r,c)])
            component_visited = set([(r,c)])
            while component_q:
                 gr, gc = component_q.popleft()
                 if grid[gr, gc] == 3: # If it's green
                     green_coords.add((gr, gc))
                     core_object_coords.add((gr, gc))
                     for nr, nc in get_neighbors(gr, gc, height, width, include_diagonals=True):
                         if (nr, nc) not in component_visited and (nr, nc) not in core_object_coords and grid[nr, nc] == 3:
                             component_visited.add((nr, nc))
                             component_q.append((nr, nc))


    return core_object_coords, green_coords


def get_border_pixels(grid, core_object_coords, green_coords):
    """ Finds pixels adjacent to the green parts of the core object, but not in it. """
    height, width = grid.shape
    border_pixels = {} # Store coords -> color

    for r_g, c_g in green_coords:
        for nr, nc in get_neighbors(r_g, c_g, height, width, include_diagonals=True):
            if (nr, nc) not in core_object_coords:
                 border_pixels[(nr, nc)] = grid[nr, nc]

    return border_pixels

def check_maroon_adjacency(grid, border_pixels):
    """ Checks if any maroon pixel is adjacent to any magenta border pixel. """
    height, width = grid.shape
    magenta_border_coords = {coord for coord, color in border_pixels.items() if color == 6}

    if not magenta_border_coords:
        return False # No magenta border pixels to be adjacent to

    for r in range(height):
        for c in range(width):
            if grid[r, c] == 9: # Found a maroon pixel
                for nr, nc in get_neighbors(r, c, height, width, include_diagonals=True):
                    if (nr, nc) in magenta_border_coords:
                        return True # Maroon pixel is adjacent to a magenta border pixel
    return False


def transform(input_grid):
    """
    Transforms the input grid based on the rules derived from examples:
    Finds a red pixel and its connected green pixels (core object).
    Analyzes the border around the green pixels.
    Conditionally changes some or all green pixels to maroon based on border color
    and proximity of external maroon pixels to a magenta border.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # 1. Find the unique red (2) pixel
    red_coord = find_pixel(input_np, 2)
    if red_coord is None:
        return input_grid # No red pixel, return original

    r_red, c_red = red_coord

    # 2. Identify the core object (red + connected green pixels)
    core_object_coords, green_coords = find_core_object(input_np, r_red, c_red)

    if not green_coords: # No green pixels connected to red
        return input_grid

    # 3. Identify the border pixels around the green part
    border_pixels = get_border_pixels(input_np, core_object_coords, green_coords)

    # 4. Analyze the border and apply rules
    all_border_magenta = True
    if not border_pixels: # Handle case with no border (e.g., object touches grid edge fully)
        all_border_magenta = False # Cannot be all magenta if empty or contains other colors
    else:
        for color in border_pixels.values():
            if color != 6:
                all_border_magenta = False
                break

    apply_rule_a = False
    apply_rule_b = False

    if all_border_magenta:
        # 4.a. Check for adjacent maroon pixels to the magenta border
        maroon_adjacent_to_magenta_border = check_maroon_adjacency(input_np, border_pixels)
        if maroon_adjacent_to_magenta_border:
            # Rule B: Change all green to maroon
            apply_rule_b = True
        else:
            # Rule A: Change specific green to maroon
            apply_rule_a = True
    else:
        # 4.b. Border is not all magenta
        # Rule A: Change specific green to maroon
        apply_rule_a = True

    # 5. Perform the transformation on the output grid
    if apply_rule_b:
        for r_g, c_g in green_coords:
            output_np[r_g, c_g] = 9 # Change all green in core object to maroon
    elif apply_rule_a:
        for r_g, c_g in green_coords:
            if r_g < r_red or (r_g == r_red and c_g < c_red):
                output_np[r_g, c_g] = 9 # Change specific green to maroon

    # Convert back to list of lists for the required output format
    return output_np.tolist()