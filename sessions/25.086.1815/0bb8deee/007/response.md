```python
import numpy as np
from collections import deque # Using deque for efficiency in BFS

"""
Identifies the unique non-black color forming complete horizontal and vertical 
dividing lines in the input grid. These lines partition the grid into four 
quadrants. Within each quadrant, locates the single contiguous object whose color 
is neither the background (black, 0) nor the divider line color. Extracts the 
3x3 minimal bounding box of each of these four objects. Assembles a 6x6 output 
grid by placing the extracted 3x3 regions into the corresponding quadrants 
of the output grid (e.g., input Top-Left object -> output Top-Left 3x3 section).
"""

def _find_divider_lines(grid):
    """
    Finds the unique non-black color forming exactly one complete horizontal line
    and exactly one complete vertical line, and returns the color and indices.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (divider_color, h_row_index, v_col_index)
               Returns (-1, -1, -1) if no such unique divider is found.
    """
    H, W = grid.shape
    h_lines = {} # color -> list of row indices
    v_lines = {} # color -> list of col indices

    # Find potential horizontal lines (must be uniform and not black)
    for r in range(H):
        row = grid[r, :]
        unique_colors = np.unique(row)
        if len(unique_colors) == 1:
            color = unique_colors[0]
            # Ensure color is treated as a standard int and is not black (0)
            color_int = int(color)
            if color_int != 0:
                if color_int not in h_lines:
                    h_lines[color_int] = []
                h_lines[color_int].append(r)

    # Find potential vertical lines (must be uniform and not black)
    for c in range(W):
        col = grid[:, c]
        unique_colors = np.unique(col)
        if len(unique_colors) == 1:
            color = unique_colors[0]
            # Ensure color is treated as a standard int and is not black (0)
            color_int = int(color)
            if color_int != 0:
                if color_int not in v_lines:
                    v_lines[color_int] = []
                v_lines[color_int].append(c)

    # Find the unique color present in both and ensure exactly one line each
    divider_color = -1
    h_row = -1
    v_col = -1

    common_colors = set(h_lines.keys()) & set(v_lines.keys())

    # Expect exactly one color to form both lines
    valid_dividers = []
    for color in common_colors:
        # Expect exactly one horizontal line and one vertical line of that color
        if len(h_lines.get(color, [])) == 1 and len(v_lines.get(color, [])) == 1:
             valid_dividers.append(color)

    # Ensure only ONE such color exists
    if len(valid_dividers) == 1:
        divider_color = valid_dividers[0]
        h_row = h_lines[divider_color][0]
        v_col = v_lines[divider_color][0]
        return divider_color, h_row, v_col
    else:
        # print(f"Warning: Expected exactly one common divider color with single H/V lines, found {len(valid_dividers)}: {valid_dividers}")
        return -1, -1, -1 # Indicate failure


def _bfs_find_object(grid, start_r, start_c, target_color, r_start, r_end, c_start, c_end, visited):
    """
    Performs BFS to find all connected pixels of target_color within quadrant bounds.

    Args:
        grid (np.array): The full input grid.
        start_r, start_c (int): Starting coordinates for BFS.
        target_color (int): The color of the object to find.
        r_start, r_end (int): Row boundaries of the quadrant (exclusive end).
        c_start, c_end (int): Column boundaries of the quadrant (exclusive end).
        visited (set): A set of (r, c) tuples already visited during the search
                       within the parent function's quadrant scan. Modified in place.

    Returns:
        list: A list of (r, c) tuples representing the pixels of the found object.
              Returns an empty list if the start pixel itself is invalid or already visited.
    """
    # Check if starting point is valid and within bounds and has the right color
    if not (r_start <= start_r < r_end and c_start <= start_c < c_end and \
            grid[start_r, start_c] == target_color and (start_r, start_c) not in visited):
        return []

    q = deque([(start_r, start_c)])
    object_pixels = []
    visited.add((start_r, start_c)) # Mark start as visited for this BFS traversal

    while q:
        r, c = q.popleft()
        object_pixels.append((r, c))

        # Check neighbors (4-connectivity: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within quadrant bounds
            if r_start <= nr < r_end and c_start <= nc < c_end:
                # Check if neighbor has the target color and hasn't been visited yet in this specific object search
                if grid[nr, nc] == target_color and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
                    
    return object_pixels


def _find_and_extract(grid, r_start, r_end, c_start, c_end, excluded_colors):
    """
    Finds the single non-excluded object in the specified quadrant region
    of the grid and extracts its 3x3 minimal bounding box.

    Args:
        grid (np.array): The full input grid.
        r_start, r_end (int): Row boundaries of the quadrant (exclusive end).
        c_start, c_end (int): Column boundaries of the quadrant (exclusive end).
        excluded_colors (set): Set of colors to ignore (e.g., background, divider).

    Returns:
        np.array: The 3x3 extracted region.

    Raises:
        ValueError: If no suitable object is found, more than one is found,
                    or if the object's bounding box is not exactly 3x3.
    """
    # Check for invalid quadrant dimensions
    if r_start >= r_end or c_start >= c_end:
        raise ValueError(f"Invalid quadrant dimensions: rows {r_start}-{r_end}, cols {c_start}-{c_end}")

    quadrant_visited = set() # Track visited cells *within this quadrant* to avoid re-processing pixels as starting points
    found_object_region = None
    object_found = False

    for r in range(r_start, r_end):
        for c in range(c_start, c_end):
            current_color = grid[r, c]
            # Check if the pixel is a potential start of our target object
            if current_color not in excluded_colors and (r, c) not in quadrant_visited:
                # Perform BFS to find the whole object connected to (r, c)
                # Pass a copy of visited to BFS if you don't want BFS to modify the outer loop's visited set directly,
                # but here it's intended to mark all pixels of the found object as visited for the outer loop.
                object_pixels = _bfs_find_object(grid, r, c, current_color,
                                                 r_start, r_end, c_start, c_end, quadrant_visited)

                # If BFS found a valid object starting at (r, c)
                if object_pixels:
                    # Ensure only one object is found per quadrant
                    if object_found:
                         raise ValueError(f"Found more than one suitable object in quadrant ({r_start}:{r_end}, {c_start}:{c_end}) "
                                          f"excluding colors {excluded_colors}.")
                    object_found = True

                    # Calculate the minimal bounding box based on absolute coordinates
                    min_r = min(p[0] for p in object_pixels)
                    max_r = max(p[0] for p in object_pixels)
                    min_c = min(p[1] for p in object_pixels)
                    max_c = max(p[1] for p in object_pixels)

                    # Check if the bounding box is exactly 3x3
                    height = max_r - min_r + 1
                    width = max_c - min_c + 1
                    if height != 3 or width != 3:
                        raise ValueError(f"Found object in quadrant ({r_start}:{r_end}, {c_start}:{c_end}) "
                                         f"with color {current_color}, but its bounding box "
                                         f"({min_r}:{max_r+1}, {min_c}:{max_c+1}) size is {height}x{width}, not 3x3.")

                    # Extract the 3x3 region from the original grid
                    found_object_region = grid[min_r : max_r + 1, min_c : max_c + 1]
                    # Don't return immediately; continue scanning to ensure only one object exists.
                    # The object pixels are already marked in quadrant_visited by BFS.

    # After checking the entire quadrant, if exactly one object was found, return its region
    if object_found:
        return found_object_region
    else:
        # If the loops complete without finding any object
        raise ValueError(f"No suitable object found in quadrant ({r_start}:{r_end}, {c_start}:{c_end}) "
                         f"excluding colors {excluded_colors}.")


def transform(input_grid):
    """
    Transforms the input grid by finding divider lines, identifying objects
    in the resulting quadrants, extracting their 3x3 bounding boxes, and
    assembling them into a 6x6 output grid.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed 6x6 grid.

    Raises:
        ValueError: If divider lines are invalid, no object is found in a quadrant,
                    more than one object is found, or an object's bounding box isn't 3x3.
    """
    # Convert input list of lists to a numpy array
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape

    # 1. Identify the divider lines and their color
    divider_color, h_row, v_col = _find_divider_lines(grid)
    if divider_color == -1:
        raise ValueError("Could not find unique horizontal and vertical divider lines.")

    # Define colors to exclude when searching for objects
    excluded_colors = {0, divider_color} # Black (background) and the divider color

    # 2. Create a new 6x6 output grid initialized with black (0).
    output_grid = np.zeros((6, 6), dtype=int)

    # 3. Define quadrant boundaries (exclusive end indices)
    # Top-Left (TL)
    tl_r_start, tl_r_end = 0, h_row
    tl_c_start, tl_c_end = 0, v_col
    # Top-Right (TR)
    tr_r_start, tr_r_end = 0, h_row
    tr_c_start, tr_c_end = v_col + 1, W
    # Bottom-Left (BL)
    bl_r_start, bl_r_end = h_row + 1, H
    bl_c_start, bl_c_end = 0, v_col
    # Bottom-Right (BR)
    br_r_start, br_r_end = h_row + 1, H
    br_c_start, br_c_end = v_col + 1, W

    # 4. Find object, extract 3x3 region, and place in output grid for each quadrant
    # Errors during extraction (ValueError) will propagate up.

    # Process Top-Left Quadrant
    region_tl = _find_and_extract(grid, tl_r_start, tl_r_end, tl_c_start, tl_c_end, excluded_colors)
    output_grid[0:3, 0:3] = region_tl

    # Process Top-Right Quadrant
    region_tr = _find_and_extract(grid, tr_r_start, tr_r_end, tr_c_start, tr_c_end, excluded_colors)
    output_grid[0:3, 3:6] = region_tr

    # Process Bottom-Left Quadrant
    region_bl = _find_and_extract(grid, bl_r_start, bl_r_end, bl_c_start, bl_c_end, excluded_colors)
    output_grid[3:6, 0:3] = region_bl

    # Process Bottom-Right Quadrant
    region_br = _find_and_extract(grid, br_r_start, br_r_end, br_c_start, br_c_end, excluded_colors)
    output_grid[3:6, 3:6] = region_br

    # 5. Return the resulting 6x6 grid as a list of lists.
    return output_grid.tolist()
```