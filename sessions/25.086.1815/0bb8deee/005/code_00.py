import numpy as np
from collections import deque # Using deque for efficiency in BFS

"""
Identifies horizontal and vertical dividing lines of a unique color in the input grid. 
These lines partition the grid into four quadrants. Within each quadrant, 
locates a single contiguous object whose color is not the background (black, 0) 
and not the divider line color. Extracts the 3x3 minimal bounding box of each 
of these four objects. Assembles a 6x6 output grid by placing the extracted 
3x3 regions into the corresponding quadrants of the output grid (TL input -> TL output, etc.).
"""

def _find_divider_lines(grid):
    """
    Finds the unique color forming complete horizontal and vertical lines
    and their indices.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (divider_color, h_row_index, v_col_index)
               Returns (-1, -1, -1) if not found.
    """
    H, W = grid.shape
    h_lines = {} # color -> list of row indices
    v_lines = {} # color -> list of col indices

    # Find potential horizontal lines (must not be black)
    for r in range(H):
        first_color = grid[r, 0]
        if first_color != 0 and np.all(grid[r, :] == first_color):
            if first_color not in h_lines:
                h_lines[first_color] = []
            h_lines[first_color].append(r)

    # Find potential vertical lines (must not be black)
    for c in range(W):
        first_color = grid[0, c]
        if first_color != 0 and np.all(grid[:, c] == first_color):
            if first_color not in v_lines:
                v_lines[first_color] = []
            v_lines[first_color].append(c)

    # Find the unique color present in both and ensure exactly one line each
    divider_color = -1
    h_row = -1
    v_col = -1

    common_colors = set(h_lines.keys()) & set(v_lines.keys())

    # Expect exactly one color to form both lines
    if len(common_colors) != 1:
        # print(f"Warning: Expected exactly one common divider color, found {len(common_colors)}: {common_colors}")
        return -1, -1, -1 # Indicate failure

    divider_color = list(common_colors)[0]

    # Expect exactly one horizontal line of that color
    if len(h_lines[divider_color]) != 1:
         # print(f"Warning: Expected exactly one horizontal line of color {divider_color}, found {len(h_lines[divider_color])}")
         return -1, -1, -1 # Indicate failure
    h_row = h_lines[divider_color][0]

    # Expect exactly one vertical line of that color
    if len(v_lines[divider_color]) != 1:
         # print(f"Warning: Expected exactly one vertical line of color {divider_color}, found {len(v_lines[divider_color])}")
         return -1, -1, -1 # Indicate failure
    v_col = v_lines[divider_color][0]

    return divider_color, h_row, v_col

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
                       within the parent function's quadrant scan.

    Returns:
        list: A list of (r, c) tuples representing the pixels of the found object.
              Returns an empty list if the start pixel itself is invalid.
    """
    if not (r_start <= start_r < r_end and c_start <= start_c < c_end and \
            grid[start_r, start_c] == target_color and (start_r, start_c) not in visited):
        return [] # Should not happen if called correctly, but safety check

    q = deque([(start_r, start_c)])
    object_pixels = []
    visited.add((start_r, start_c)) # Mark start as visited

    while q:
        r, c = q.popleft()
        object_pixels.append((r, c))

        # Check neighbors (4-connectivity: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within quadrant bounds
            if r_start <= nr < r_end and c_start <= nc < c_end:
                # Check if neighbor has the target color and hasn't been visited
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
        ValueError: If no suitable object is found or if the object's
                    bounding box is not exactly 3x3.
    """
    visited = set() # Track visited cells within this quadrant to avoid re-processing

    for r in range(r_start, r_end):
        for c in range(c_start, c_end):
            current_color = grid[r, c]
            # Check if the pixel is a potential start of our target object
            if current_color not in excluded_colors and (r, c) not in visited:
                # Perform BFS to find the whole object connected to (r, c)
                object_pixels = _bfs_find_object(grid, r, c, current_color,
                                                 r_start, r_end, c_start, c_end, visited)

                # If BFS found an object starting at (r, c)
                if object_pixels:
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
                    extracted_region = grid[min_r : max_r + 1, min_c : max_c + 1]
                    # Since we expect only one object per quadrant, return immediately
                    return extracted_region

    # If the loops complete without finding and returning an object
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
    """
    # Convert input list of lists to a numpy array
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape

    # 1. Identify the divider lines and their color
    divider_color, h_row, v_col = _find_divider_lines(grid)
    if divider_color == -1:
        raise ValueError("Could not find unique horizontal and vertical divider lines.")

    # Define colors to exclude when searching for objects
    excluded_colors = {0, divider_color} # Black and the divider color

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
    try:
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

    except ValueError as e:
        print(f"Error during processing: {e}")
        # Depending on requirements, might return empty/original grid or re-raise
        # For now, let's return an empty 6x6 grid on error during extraction
        return np.zeros((6, 6), dtype=int).tolist()


    # 5. Return the resulting 6x6 grid as a list of lists.
    return output_grid.tolist()