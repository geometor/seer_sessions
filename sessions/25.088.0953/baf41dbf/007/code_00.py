import numpy as np
from collections import deque

"""
Transforms the input grid by expanding green shapes into adjacent white areas. 
The expansion is directed towards magenta markers that are horizontally or vertically 
aligned with the initial bounding box of the green shape. The expansion stops one 
pixel short of the marker. Only white pixels in the expansion path are filled 
with green. Original green shapes, magenta markers, and white pixels within the 
original green shape's bounding box are preserved.

1.  Create a copy of the input grid for the output.
2.  Find all distinct contiguous green (3) shapes and their initial bounding 
    boxes (min_r, max_r, min_c, max_c).
3.  Find the coordinates of all magenta (6) markers.
4.  For each green shape:
    a.  Determine the maximum extent of expansion in each of the four 
        directions (up, down, left, right) based on aligned magenta markers.
        i.  Initialize expansion limits: find the marker closest but outside 
            the initial bounding box for each direction (left, right, top, bottom) 
            that shares the respective row/column range of the initial box.
        ii. Calculate the final expansion boundaries, stopping one pixel before 
            the respective marker. Default to the initial bounding box edge if 
            no marker exists in a direction.
    b.  Define four rectangular expansion zones (potentially empty):
        - Left Zone: The area between the calculated left expansion boundary and 
          the initial left edge of the shape, within the shape's initial row span.
        - Right Zone: The area between the initial right edge and the calculated 
          right expansion boundary, within the shape's initial row span.
        - Top Zone: The area between the calculated top expansion boundary and 
          the initial top edge, within the shape's initial column span.
        - Bottom Zone: The area between the initial bottom edge and the 
          calculated bottom expansion boundary, within the shape's initial column span.
    c.  Iterate through the pixels within these four expansion zones.
    d.  If a pixel `(r, c)` within an expansion zone corresponds to a white (0) 
        pixel in the *input* grid, change its color to green (3) in the *output* grid.
5.  Return the modified output grid.
"""

# --- Helper Functions ---

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid using BFS.

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

    # 4. Process each green shape
    for shape in green_shapes:
        # Get the initial bounding box
        min_r, max_r, min_c, max_c = shape['bbox']

        # 4a. Determine expansion limits based on aligned markers
        # Find the marker *positions* that define the furthest expansion boundary
        limit_left_c = -1  # Furthest marker col to the left
        limit_right_c = cols # Furthest marker col to the right
        limit_top_r = -1   # Furthest marker row above
        limit_bottom_r = rows # Furthest marker row below

        for m_r, m_c in magenta_markers:
            # Check horizontal alignment (marker row within shape's initial row span)
            if min_r <= m_r <= max_r:
                if m_c < min_c:
                    limit_left_c = max(limit_left_c, m_c) # Find the closest marker to the shape edge
                elif m_c > max_c:
                    limit_right_c = min(limit_right_c, m_c) # Find the closest marker to the shape edge

            # Check vertical alignment (marker col within shape's initial col span)
            if min_c <= m_c <= max_c:
                if m_r < min_r:
                    limit_top_r = max(limit_top_r, m_r) # Find the closest marker to the shape edge
                elif m_r > max_r:
                    limit_bottom_r = min(limit_bottom_r, m_r) # Find the closest marker to the shape edge

        # Calculate the final coordinates for the expansion fill (stop before marker)
        # Default to initial bbox edge if no marker found in that direction
        expand_min_c = limit_left_c + 1 if limit_left_c != -1 else min_c
        expand_max_c = limit_right_c - 1 if limit_right_c != cols else max_c
        expand_min_r = limit_top_r + 1 if limit_top_r != -1 else min_r
        expand_max_r = limit_bottom_r - 1 if limit_bottom_r != rows else max_r

        # Clamp to grid boundaries (though loop ranges should handle this)
        expand_min_c = max(0, expand_min_c)
        expand_max_c = min(cols - 1, expand_max_c)
        expand_min_r = max(0, expand_min_r)
        expand_max_r = min(rows - 1, expand_max_r)

        # 4b. Define and fill expansion zones
        # 4c/d. Iterate through zones and fill white pixels

        # Fill Left Zone (if expansion happened leftwards)
        if expand_min_c < min_c:
            for r in range(min_r, max_r + 1):
                for c in range(expand_min_c, min_c): # Up to min_c - 1
                     # Check bounds just in case, though range should be correct
                    if 0 <= r < rows and 0 <= c < cols:
                        if input_grid[r, c] == 0:
                           output_grid[r, c] = 3

        # Fill Right Zone (if expansion happened rightwards)
        if expand_max_c > max_c:
            for r in range(min_r, max_r + 1):
                for c in range(max_c + 1, expand_max_c + 1): # Up to expand_max_c
                     if 0 <= r < rows and 0 <= c < cols:
                        if input_grid[r, c] == 0:
                            output_grid[r, c] = 3

        # Fill Top Zone (if expansion happened upwards)
        if expand_min_r < min_r:
            for r in range(expand_min_r, min_r): # Up to min_r - 1
                for c in range(min_c, max_c + 1):
                     if 0 <= r < rows and 0 <= c < cols:
                        if input_grid[r, c] == 0:
                            output_grid[r, c] = 3

        # Fill Bottom Zone (if expansion happened downwards)
        if expand_max_r > max_r:
            for r in range(max_r + 1, expand_max_r + 1): # Up to expand_max_r
                for c in range(min_c, max_c + 1):
                     if 0 <= r < rows and 0 <= c < cols:
                        if input_grid[r, c] == 0:
                            output_grid[r, c] = 3

    # 5. Return the modified output grid
    return output_grid