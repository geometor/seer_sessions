import numpy as np

"""
This transformation identifies a single non-white 'template' object in the input grid. 
It then tiles this object across a new grid, which has the same width as the input but is one row taller.

The tiling follows these rules:

1.  **Output Grid Initialization:**
    *   Create an output grid with dimensions (input_height + 1, input_width).
    *   Initialize the output grid with the background color (white, 0).

2.  **Template Identification:**
    *   Find the first contiguous non-white object in the *input* grid. Determine its top-left corner (r0, c0), height (h), width (w), color (template_color), and the relative coordinates of its pixels (pattern).

3.  **Horizontal Tiling (First Row on Output Grid):**
    *   Place the original template object at its original location (r0, c0) on the *output* grid using its original color (template_color).
    *   Generate copies horizontally to the right, starting from column `c0 + horizontal_gap`.
    *   The horizontal gap between the start columns of adjacent objects is fixed (e.g., 4 columns).
    *   The color of the copies follows a repeating pattern: [original_color, original_color, magenta (6)].
    *   Tiling continues as long as the starting column (`current_c`) of the next potential copy is less than the output grid's width. Objects may be partially placed if they extend beyond the right edge.

4.  **Vertical Tiling (Subsequent Rows on Output Grid):**
    *   Replicate patterns downwards, starting from row `r0 + vertical_gap`.
    *   The vertical gap between the start rows of adjacent patterns is fixed and equal to the template object's height plus one row (`h + 1`).
    *   Crucially, only the *magenta* colored objects from the first row's pattern are copied into the subsequent rows. The original colored objects are *not* replicated vertically.
    *   The vertically replicated objects retain the magenta color.
    *   Tiling continues as long as the starting row (`current_r`) of the next potential row of copies is less than the output grid's height. Objects may be partially placed if they extend beyond the bottom edge.

The final output grid contains the tiled pattern.
"""

def find_template_object(grid, background_color=0):
    """
    Finds the first contiguous non-background object in the input grid
    and returns its properties. Assumes there is only one such object.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color considered background (default 0).

    Returns:
        dict: A dictionary containing object properties:
              'r0', 'c0': top-left coordinates (relative to input grid)
              'h', 'w': height and width
              'color': the object's color
              'pattern': list of (dr, dc) relative coordinates of object pixels
              Returns None if no object is found.
    """
    non_bg_coords = np.argwhere(grid != background_color)
    if non_bg_coords.size == 0:
        return None # No object found

    # Find the coordinates of the first non-background pixel
    first_pixel_r, first_pixel_c = non_bg_coords[0]
    obj_color = grid[first_pixel_r, first_pixel_c]

    # Perform BFS to find all connected pixels of the same color
    q = [(first_pixel_r, first_pixel_c)]
    visited = set(q)
    obj_pixels_abs = list(q) # Store absolute coordinates

    while q:
        r, c = q.pop(0)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-connectivity
            nr, nc = r + dr, c + dc
            if (0 <= nr < grid.shape[0] and
                0 <= nc < grid.shape[1] and
                grid[nr, nc] == obj_color and
                (nr, nc) not in visited):
                visited.add((nr, nc))
                q.append((nr, nc))
                obj_pixels_abs.append((nr, nc))

    if not obj_pixels_abs:
         return None

    # Determine bounding box
    rows, cols = zip(*obj_pixels_abs)
    r0 = min(rows)
    c0 = min(cols)
    r1 = max(rows)
    c1 = max(cols)
    h = r1 - r0 + 1
    w = c1 - c0 + 1

    # Extract relative pattern pixels
    pattern_pixels_relative = sorted([(r_abs - r0, c_abs - c0) for r_abs, c_abs in obj_pixels_abs])

    return {
        "r0": r0, "c0": c0, "h": h, "w": w,
        "color": obj_color, "pattern": pattern_pixels_relative
    }


def place_pattern(grid, r_start, c_start, pattern_pixels, color):
    """
    Places the object pattern onto the grid at the specified location and color,
    handling boundary clipping.

    Args:
        grid (np.array): The target grid (modified in place).
        r_start (int): Top row for placing the pattern.
        c_start (int): Left column for placing the pattern.
        pattern_pixels (list): List of (dr, dc) relative coordinates.
        color (int): The color to draw the pattern with.
    """
    grid_height, grid_width = grid.shape
    for dr, dc in pattern_pixels:
        r, c = r_start + dr, c_start + dc
        # Check bounds before drawing
        if 0 <= r < grid_height and 0 <= c < grid_width:
            grid[r, c] = color


def transform(input_grid):
    """
    Applies the described tiling transformation to the input grid.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: The transformed 2D output grid.
    """
    # --- Step 1: Determine output grid size and initialize ---
    input_height, input_width = input_grid.shape
    output_height = input_height + 1
    output_width = input_width
    output_grid = np.zeros((output_height, output_width), dtype=int) # Default background is 0 (white)

    # --- Step 2: Find the template object in the input grid ---
    template_obj = find_template_object(input_grid)
    if template_obj is None:
        # If no object found, return the initialized (empty) output grid
        return output_grid

    r0, c0 = template_obj["r0"], template_obj["c0"] # Coordinates relative to input, used as start on output
    h, w = template_obj["h"], template_obj["w"]
    template_color = template_obj["color"]
    pattern = template_obj["pattern"]

    # --- Step 3: Define constants and parameters ---
    magenta_color = 6
    horizontal_gap = 4  # Gap between start columns
    vertical_gap = h + 1 # Gap between start rows
    color_sequence = [template_color, template_color, magenta_color]

    # --- Step 4: Generate First Row on Output Grid ---
    first_row_objects = [] # Store info for vertical tiling: (col_start, color)

    # Place the original object first
    place_pattern(output_grid, r0, c0, pattern, template_color)
    first_row_objects.append({"c": c0, "color": template_color})

    # Place horizontal copies
    current_c = c0 + horizontal_gap
    copy_index = 1 # Start counting copies from 1 (0 is the original)

    # Loop condition checks if the *start* column is within bounds
    while current_c < output_width:
        # Determine color for this copy
        copy_color = color_sequence[copy_index % len(color_sequence)]

        # Place the copy (place_pattern handles clipping)
        place_pattern(output_grid, r0, current_c, pattern, copy_color)

        # Store info for vertical tiling
        first_row_objects.append({"c": current_c, "color": copy_color})

        # Move to the next potential position
        current_c += horizontal_gap
        copy_index += 1

    # --- Step 5: Generate Subsequent Rows on Output Grid ---
    current_r = r0 + vertical_gap

    # Loop condition checks if the *start* row is within bounds
    while current_r < output_height:
        # Iterate through the objects placed in the first row
        for obj_info in first_row_objects:
            # Only copy if the object in the first row was magenta
            if obj_info["color"] == magenta_color:
                obj_c = obj_info["c"]
                # Place a magenta copy in the current row (place_pattern handles clipping)
                place_pattern(output_grid, current_r, obj_c, pattern, magenta_color)

        # Move to the next potential row position
        current_r += vertical_gap

    return output_grid