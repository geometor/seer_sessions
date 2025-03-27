import numpy as np
from collections import deque

"""
1. Initialize an empty output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2. Identify all pixels in the input grid whose color is *not* white (0) and *not* azure (8). These are the 'source pixels'.
3. If no source pixels are found, return the initial empty output grid.
4. Determine the minimum bounding box that encloses *all* identified source pixels. Find the minimum row (`min_r`), minimum column (`min_c`), maximum row (`max_r`), and maximum column (`max_c`) among all source pixels.
5. Create the 'composite template' pattern:
    a. Create a new grid (the template) with height `max_r - min_r + 1` and width `max_c - min_c + 1`, initially filled with the background color (white, 0).
    b. Iterate through all the original source pixels identified in step 2. For each source pixel at coordinate (`r`, `c`) with color `col`, set the pixel at `(r - min_r, c - min_c)` in the template grid to `col`.
6. Identify all distinct connected groups of azure (8) pixels in the input grid. These are the 'markers'.
7. If no markers are found, return the initial empty output grid.
8. For each identified marker:
    a. Determine the coordinate (row, column) of its top-leftmost pixel. This is the 'stamp location'.
    b. Copy ('stamp') the 'composite template' onto the output grid, aligning the template's top-left corner with the 'stamp location'.
    c. Pixels from the template (other than the background color 0) overwrite the corresponding pixels in the output grid. Ensure the template is clipped if it extends beyond the output grid's boundaries.
9. Return the final modified output grid.
"""


# Helper function to find connected components (corrected version)
def find_connected_components_no_scipy(grid, target_colors=None):
    """
    Finds all connected components for specified colors or all non-background colors
    using BFS, without relying on scipy.

    Args:
        grid (np.array): The input grid.
        target_colors (list or set, optional): A collection of integer colors
            to find objects for. If None, finds objects for all colors except 0.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (list of (r, c) tuples),
              'bbox' (tuple: (min_r, min_c, max_r, max_c)), 'top_left' (r, c).
              Returns empty list if no objects found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    valid_target_colors = set()
    if target_colors is None:
        present_colors = np.unique(grid)
        valid_target_colors = {c for c in present_colors if c != 0}
    else:
        valid_target_colors = set(target_colors)

    if not valid_target_colors:
        return objects # Return empty list if no valid colors to search for

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in valid_target_colors and not visited[r, c]:
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                if component_pixels:
                    objects.append({
                        'color': color,
                        'pixels': component_pixels,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'top_left': (min_r, min_c)
                    })

    # Sort objects only if there are objects to sort
    if objects:
        objects.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))
    return objects

# Helper function to stamp a pattern onto the grid (reused)
def stamp_pattern(output_grid, pattern, top_left_coord):
    """
    Overlays the non-background pixels of the pattern onto the output grid
    at the specified coordinate, handling clipping.
    """
    r_start, c_start = top_left_coord
    p_h, p_w = pattern.shape
    g_h, g_w = output_grid.shape

    # Calculate the intersection bounds for stamping
    r_end = min(r_start + p_h, g_h)
    c_end = min(c_start + p_w, g_w)

    # Adjust start coordinates if they are negative (shouldn't happen often with valid markers, but defensive)
    p_r_offset = 0
    p_c_offset = 0
    if r_start < 0:
        p_r_offset = -r_start
        r_start = 0
    if c_start < 0:
        p_c_offset = -c_start
        c_start = 0

    # Calculate slices for pattern and grid based on intersection and potential negative offset
    p_r_slice = slice(p_r_offset, p_r_offset + (r_end - r_start))
    p_c_slice = slice(p_c_offset, p_c_offset + (c_end - c_start))
    g_r_slice = slice(r_start, r_end)
    g_c_slice = slice(c_start, c_end)

    # Ensure slices are valid (have positive range) and dimensions match before assignment
    if g_r_slice.start < g_r_slice.stop and g_c_slice.start < g_c_slice.stop and \
       (p_r_slice.stop - p_r_slice.start) == (g_r_slice.stop - g_r_slice.start) and \
       (p_c_slice.stop - p_c_slice.start) == (g_c_slice.stop - g_c_slice.start):

        # Get the relevant slice of the pattern
        pattern_slice = pattern[p_r_slice, p_c_slice]
        # Create a mask for non-zero (non-background) pixels in the pattern slice
        mask = pattern_slice != 0

        # Apply the pattern slice to the output grid using the mask
        # This ensures only non-background parts of the template overwrite the output
        output_grid[g_r_slice, g_c_slice][mask] = pattern_slice[mask]


def transform(input_grid):
    """
    Transforms the input grid by creating a composite template from all non-background,
    non-marker pixels and stamping it at locations indicated by marker pixels.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # 1. Initialize output_grid
    output_grid = np.zeros_like(input_grid_np) # Filled with background (0)

    # Define marker and background colors
    marker_color = 8
    background_color = 0

    # 2. Identify source pixels (not background, not marker)
    source_mask = (input_grid_np != background_color) & (input_grid_np != marker_color)
    source_rows, source_cols = np.where(source_mask)
    source_pixels = list(zip(source_rows, source_cols))

    # 3. If no source pixels, return the initial white grid
    if not source_pixels:
        return output_grid.tolist()

    # 4. Determine the combined bounding box for source pixels
    min_r = np.min(source_rows)
    min_c = np.min(source_cols)
    max_r = np.max(source_rows)
    max_c = np.max(source_cols)

    # 5. Create the 'composite template' pattern
    template_h = max_r - min_r + 1
    template_w = max_c - min_c + 1
    composite_template = np.zeros((template_h, template_w), dtype=int)

    # 5b. Populate the template
    for r, c in source_pixels:
        color = input_grid_np[r, c]
        composite_template[r - min_r, c - min_c] = color

    # 6. Find marker objects (color 8)
    marker_objects = find_connected_components_no_scipy(input_grid_np, target_colors=[marker_color])

    # 7. If no markers, return the initial white grid
    if not marker_objects:
        return output_grid.tolist()

    # 8. Stamp the template for each marker
    for marker in marker_objects:
        stamp_location = marker['top_left'] # Get the top-left coordinate
        # 8b & 8c. Stamp the template using the helper function
        stamp_pattern(output_grid, composite_template, stamp_location)

    # 9. Return the final grid as a list of lists
    return output_grid.tolist()