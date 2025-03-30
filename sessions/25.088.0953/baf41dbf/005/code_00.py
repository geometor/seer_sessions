import numpy as np
from collections import deque

"""
Transforms the input grid by extending green shapes towards associated magenta markers, 
filling the extended area with green while preserving magenta markers and original 
white spaces within the initial bounds of the green shapes.

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct, contiguous green (3) shapes and their initial bounding 
    boxes (min_row, max_row, min_col, max_col).
3.  Identify the coordinates of all magenta (6) marker pixels.
4.  For each identified green shape:
    a.  Calculate its corresponding "extended bounding box" based on marker alignment:
        i.  Start with the initial bounding box dimensions.
        ii. Check each magenta marker for horizontal or vertical alignment with the 
            *initial* bounding box.
        iii. If a marker is aligned and outside the initial box, expand the 
             corresponding edge of the bounding box towards the marker, stopping 
             one pixel short. Use min/max to handle multiple markers extending 
             the same edge.
    b.  Iterate through all pixel coordinates (row `r`, column `c`) within this 
        calculated extended bounding box.
    c.  For each pixel (r, c) inside the extended bounding box:
        i.  If the pixel in the *input* grid `input_grid[r, c]` is magenta (6), 
            do nothing (it's preserved).
        ii. Else if the pixel (r, c) falls *within* the *initial* bounding box of 
            the current green shape AND the pixel `input_grid[r, c]` is white (0), 
            do nothing (preserve internal "hole").
        iii. Else (pixel is not a marker and not an internal white hole), set 
             the pixel in the `output_grid[r, c]` to green (3).
5.  Return the modified output grid.
"""

import numpy as np
from collections import deque

# --- Helper Functions ---

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
              - 'pixels': A set of (row, col) tuples for the object's pixels.
              - 'bbox': The bounding box (min_row, max_row, min_col, max_col).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                obj_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, max_r = r, r
                min_c, max_c = c, c
                while q:
                    curr_r, curr_c = q.popleft()
                    obj_pixels.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                if obj_pixels:
                    objects.append({'pixels': obj_pixels, 'bbox': (min_r, max_r, min_c, max_c)})
    return objects

def find_pixels(grid, color):
    """
    Finds the coordinates of all pixels of a specific color.

    Args:
        grid (np.array): The input grid.
        color (int): The color to find.

    Returns:
        list: A list of (row, col) tuples for pixels of the specified color.
    """
    # np.where returns tuple of arrays (rows, cols); zip pairs them up
    return list(zip(*np.where(grid == color)))


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 2. Identify Green Shapes and their initial bounding boxes
    green_shapes = find_objects(input_grid, 3)

    # 3. Identify Magenta Markers
    magenta_markers = find_pixels(input_grid, 6)
    magenta_marker_set = set(magenta_markers) # For quick lookup

    # 4. Process each green shape
    for shape in green_shapes:
        # Get the initial bounding box
        min_r, max_r, min_c, max_c = shape['bbox']
        initial_bbox = shape['bbox'] # Keep a reference

        # 4a. Calculate the extended bounding box
        ext_min_r, ext_max_r = min_r, max_r
        ext_min_c, ext_max_c = min_c, max_c

        for m_r, m_c in magenta_markers:
            # Check horizontal alignment (marker row within shape's initial row span)
            if min_r <= m_r <= max_r:
                # Marker is to the right of the initial bbox
                if m_c > max_c:
                    # Extend right edge up to one pixel before the marker
                    ext_max_c = max(ext_max_c, m_c - 1)
                # Marker is to the left of the initial bbox
                elif m_c < min_c:
                    # Extend left edge up to one pixel after the marker
                    ext_min_c = min(ext_min_c, m_c + 1)

            # Check vertical alignment (marker col within shape's initial col span)
            elif min_c <= m_c <= max_c:
                 # Marker is below the initial bbox
                if m_r > max_r:
                    # Extend bottom edge up to one pixel before the marker
                    ext_max_r = max(ext_max_r, m_r - 1)
                # Marker is above the initial bbox
                elif m_r < min_r:
                    # Extend top edge up to one pixel after the marker
                    ext_min_r = min(ext_min_r, m_r + 1)

        # Clamp extended bounds to grid limits (important edge case)
        ext_min_r = max(0, ext_min_r)
        ext_max_r = min(rows - 1, ext_max_r)
        ext_min_c = max(0, ext_min_c)
        ext_max_c = min(cols - 1, ext_max_c)
        
        # Store the calculated final extended bounding box for this shape
        extended_bbox = (ext_min_r, ext_max_r, ext_min_c, ext_max_c)

        # 4b. Iterate through pixels within the extended bounding box
        for r in range(ext_min_r, ext_max_r + 1):
            for c in range(ext_min_c, ext_max_c + 1):
                # 4c. Apply fill logic
                
                # i. Check if it's a magenta marker (already handled by initial copy)
                if (r, c) in magenta_marker_set:
                    continue # Skip, preserve marker

                # ii. Check if it's an internal white "hole" within the initial bbox
                is_within_initial_bbox = (initial_bbox[0] <= r <= initial_bbox[1] and
                                          initial_bbox[2] <= c <= initial_bbox[3])
                is_input_white = (input_grid[r, c] == 0)

                if is_within_initial_bbox and is_input_white:
                    continue # Skip, preserve internal white hole

                # iii. Otherwise, fill with green
                output_grid[r, c] = 3

    # 5. Return the modified output grid
    return output_grid