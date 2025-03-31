import numpy as np
from collections import deque

"""
Transformation Rule Description:

1. Identify all distinct, solid, rectangular objects in the input grid against the white (0) background. An object is a connected component of non-background pixels. A rectangular object is one where the connected component perfectly fills its bounding box without any background holes.
2. Distinguish between two types of these rectangular objects:
   - "Simple Rectangles": Filled entirely with a single solid color.
   - "Pattern Rectangle": Has an outer frame (1-pixel thick border) of one color and an interior area containing at least one pixel of a different color. Assume there is at most one such Pattern Rectangle per input grid.
3. If a Pattern Rectangle exists:
   a. Extract its frame color and its inner pattern (the grid content inside the 1-pixel frame).
   b. Iterate through all identified Simple Rectangles.
   c. If a Simple Rectangle's solid color matches the Pattern Rectangle's frame color, and the Simple Rectangle is large enough to have an interior (at least 3x3 in size):
      i. Copy the inner pattern from the Pattern Rectangle.
      ii. Place this pattern into the interior area of the Simple Rectangle (the area inside its 1-pixel border), aligning the top-left corner of the pattern with the top-left corner of the Simple Rectangle's interior.
      iii. If the Simple Rectangle's interior is smaller than the pattern, crop the pattern (copy only the top-left portion that fits).
4. Rectangles (Simple or Patterned) that do not meet the matching criteria, as well as the original Pattern Rectangle itself, remain unchanged in the output.
5. The background remains unchanged.
6. The output grid has the same dimensions as the input grid.
"""

# --- Helper Functions ---

def bfs_find_connected(grid, start_coord, visited):
    """
    Finds all connected non-background (non-zero) pixels starting from
    start_coord using Breadth-First Search. Marks visited pixels.
    Returns a set of (row, col) coordinates for the connected component.
    """
    q = deque([start_coord])
    coords = set()
    h, w = grid.shape
    start_r, start_c = start_coord

    # Check if starting point is valid (non-background and not visited)
    if not (0 <= start_r < h and 0 <= start_c < w) or \
       grid[start_r, start_c] == 0 or \
       visited[start_r, start_c]:
        return set() # Return empty set if start is invalid

    # Mark start as visited and add to coordinates
    visited[start_r, start_c] = True
    coords.add(start_coord)

    while q:
        r, c = q.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if not visited, and if not background
            if 0 <= nr < h and 0 <= nc < w and \
               not visited[nr, nc] and grid[nr, nc] != 0:
                visited[nr, nc] = True
                coords.add((nr, nc))
                q.append((nr, nc))
    return coords

def get_bounding_box(coords):
    """
    Calculates the minimum bounding box (min_r, min_c, max_r, max_c)
    for a set of coordinates. Returns None if coords is empty.
    """
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return (min_r, min_c, max_r, max_c)

def is_solid_rectangle(grid, coords, bbox):
    """
    Checks if a connected component (coords) perfectly forms a solid rectangle
    within its bounding box (bbox), meaning all pixels within the bbox
    are part of the component and are non-background.
    """
    if not coords or not bbox:
        return False
    min_r, min_c, max_r, max_c = bbox
    obj_h = max_r - min_r + 1
    obj_w = max_c - min_c + 1

    # Check 1: Does the number of coords match the bbox area?
    if len(coords) != obj_h * obj_w:
        return False

    # Check 2: Are all pixels within the bbox non-zero?
    # This confirms no background holes within the bbox for the found component
    # This check might seem redundant if Check 1 passed and BFS worked on a truly solid rectangle,
    # but ensures we're dealing with a filled rectangle based on the grid values themselves within the box.
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # If a pixel inside the bounding box is background, it's not solid.
            if grid[r, c] == 0:
                 # This case should ideally be caught by check 1 if BFS found fewer coords than bbox area.
                 # Including it adds robustness against weird shapes.
                return False
            # Additionally, confirm the pixel was part of the found component (coords).
            # This ensures the component *is* the rectangle, not just contained within it.
            if (r, c) not in coords:
                return False # Should also be caught by check 1.
    return True

def classify_rectangle(grid, bbox):
    """
    Classifies a confirmed solid rectangular region defined by bbox
    as either 'simple' or 'pattern'.
    Returns a dictionary with object info or None if classification fails.
    """
    min_r, min_c, max_r, max_c = bbox
    obj_h = max_r - min_r + 1
    obj_w = max_c - min_c + 1

    # Extract the rectangle content directly using bbox for efficiency
    rect_slice = grid[min_r:max_r+1, min_c:max_c+1]

    # Use the top-left color as the reference
    ref_color = rect_slice[0, 0]

    # Check if it's a simple rectangle (all pixels match ref_color)
    if np.all(rect_slice == ref_color):
        return {'type': 'simple', 'color': ref_color, 'bbox': bbox}

    # If not simple, check if it's a pattern rectangle (needs frame)
    # Check requires at least 3x3 size for an interior
    if obj_h >= 3 and obj_w >= 3:
        frame_color = rect_slice[0, 0] # Assume frame color is top-left
        frame_ok = True
        # Check top row
        if not np.all(rect_slice[0, :] == frame_color): frame_ok = False
        # Check bottom row
        if frame_ok and not np.all(rect_slice[-1, :] == frame_color): frame_ok = False
        # Check left column
        if frame_ok and not np.all(rect_slice[:, 0] == frame_color): frame_ok = False
        # Check right column
        if frame_ok and not np.all(rect_slice[:, -1] == frame_color): frame_ok = False

        # If frame is consistent, check if the interior has at least one different color
        interior_differs = False
        if frame_ok:
            inner_slice = rect_slice[1:-1, 1:-1]
            # Check if any element in the inner slice is different from the frame color
            if np.any(inner_slice != frame_color):
                interior_differs = True

        # If frame is consistent and interior differs, classify as pattern
        if frame_ok and interior_differs:
            inner_pattern = inner_slice # Already sliced
            return {'type': 'pattern', 'frame_color': frame_color, 'bbox': bbox, 'inner_pattern': inner_pattern.copy()}

    # If it's neither simple nor a valid pattern rectangle (e.g., multi-colored without proper frame)
    return None

def paste_pattern(output_grid, target_bbox, source_pattern):
    """
    Pastes the source_pattern into the inner area of the target_bbox
    on the output_grid, cropping the pattern if necessary.
    Assumes target_bbox corresponds to a rectangle >= 3x3.
    """
    min_r, min_c, max_r, max_c = target_bbox
    target_h = max_r - min_r + 1
    target_w = max_c - min_c + 1

    # Basic check: ensure target is large enough for an interior
    if target_h < 3 or target_w < 3:
        return # Cannot paste into something without an interior

    # Pattern details
    if source_pattern is None or source_pattern.size == 0:
        return # Nothing to paste

    source_h, source_w = source_pattern.shape

    # Target interior details: top-left corner coordinates and dimensions
    target_inner_top, target_inner_left = min_r + 1, min_c + 1
    target_inner_h = target_h - 2
    target_inner_w = target_w - 2

    # Determine copy dimensions (cropping based on minimum of source/target interior)
    copy_h = min(source_h, target_inner_h)
    copy_w = min(source_w, target_inner_w)

    # Perform copy only if there are valid dimensions to copy
    if copy_h > 0 and copy_w > 0:
        # Select the top-left portion of the source pattern to copy
        pattern_to_copy = source_pattern[:copy_h, :copy_w]

        # Place the cropped pattern onto the output grid's interior section
        output_grid[target_inner_top : target_inner_top + copy_h,
                    target_inner_left : target_inner_left + copy_w] = pattern_to_copy


# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation: finds a unique pattern rectangle and copies its
    inner pattern into simple rectangles of the same color as the pattern's frame.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input, modified in place
    output_grid = input_grid_np.copy()
    h, w = input_grid_np.shape
    # Keep track of visited pixels to avoid processing objects multiple times
    visited = np.zeros_like(input_grid_np, dtype=bool)

    all_objects = []

    # Step 1: Find all connected components (potential objects)
    for r in range(h):
        for c in range(w):
            # If pixel is non-background and not yet visited, start a search
            if input_grid_np[r, c] != 0 and not visited[r, c]:
                # Find all connected non-background pixels for this component
                coords = bfs_find_connected(input_grid_np, (r, c), visited)

                if coords: # If a component was found
                    # Step 2: Check if the component is a solid rectangle
                    bbox = get_bounding_box(coords)
                    if is_solid_rectangle(input_grid_np, coords, bbox):
                        # Step 3: Classify the solid rectangle
                        obj_info = classify_rectangle(input_grid_np, bbox)
                        if obj_info:
                            # Store successfully classified rectangles
                            all_objects.append(obj_info)
                    # else: Component is not a solid rectangle, ignore it


    # Step 4: Separate simple and pattern objects from the classified list
    simple_rects = []
    pattern_rect = None
    for obj in all_objects:
        if obj['type'] == 'simple':
            simple_rects.append(obj)
        elif obj['type'] == 'pattern':
            # Assume only one pattern rectangle exists per grid. Store the first one found.
            if pattern_rect is None:
                pattern_rect = obj
            # else: Ignore subsequent pattern rects if assumption holds true

    # Step 5: Apply transformation if a pattern rectangle was found
    if pattern_rect is None:
        # No pattern rectangle found, return the original grid (already copied)
        return output_grid.tolist()

    # Get pattern details from the identified pattern rectangle
    pattern_frame_color = pattern_rect['frame_color']
    source_pattern = pattern_rect['inner_pattern']

    # Step 6: Iterate through simple rectangles and apply the pattern if colors match and size allows
    for simple_obj in simple_rects:
        # Check if the simple rectangle's color matches the pattern's frame color
        if simple_obj['color'] == pattern_frame_color:
            # Get dimensions to check if it can have an interior
            min_r, min_c, max_r, max_c = simple_obj['bbox']
            simple_h = max_r - min_r + 1
            simple_w = max_c - min_c + 1

            # Apply pattern only if the simple rectangle is large enough (>= 3x3)
            if simple_h >= 3 and simple_w >= 3:
                # Call the helper function to paste the pattern (handles cropping)
                paste_pattern(output_grid, simple_obj['bbox'], source_pattern)

    # Convert the final modified numpy array back to a list of lists
    return output_grid.tolist()