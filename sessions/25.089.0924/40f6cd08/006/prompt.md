
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies rectangular objects in the input grid. Distinguishes between:
1. Simple Rectangles: Filled with a single solid color.
2. Pattern Rectangle: Has a 1-pixel frame of one color and an interior containing at least one pixel of a different color. Assumes at most one Pattern Rectangle exists.

Transformation:
- Finds the unique Pattern Rectangle.
- Finds all Simple Rectangles whose solid color matches the Pattern Rectangle's frame color and are at least 3x3.
- Copies the inner pattern from the Pattern Rectangle into the inner area of each matching Simple Rectangle.
- If the target Simple Rectangle's inner area is smaller than the source pattern, the pattern is cropped (top-left portion is copied).
- Other rectangles and the background remain unchanged.
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
    # (This check confirms no background holes within the bbox)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r, c] == 0:
                return False # Background pixel found inside the bounding box
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

    # Extract the rectangle content
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
            if np.any(inner_slice != frame_color):
                interior_differs = True

        # If frame is consistent and interior differs, classify as pattern
        if frame_ok and interior_differs:
            inner_pattern = inner_slice # Already extracted
            return {'type': 'pattern', 'frame_color': frame_color, 'bbox': bbox, 'inner_pattern': inner_pattern.copy()}

    # If it's neither simple nor a valid pattern rectangle
    # This might happen for multi-colored rectangles without a proper frame. Ignore for this task.
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

    # Ensure target is large enough (redundant check if called correctly)
    if target_h < 3 or target_w < 3:
        return

    # Pattern details
    if source_pattern.size == 0: return # Nothing to paste
    source_h, source_w = source_pattern.shape

    # Target interior details
    target_inner_top, target_inner_left = min_r + 1, min_c + 1
    target_inner_h = target_h - 2
    target_inner_w = target_w - 2

    # Determine copy dimensions (cropping)
    copy_h = min(source_h, target_inner_h)
    copy_w = min(source_w, target_inner_w)

    # Perform copy if dimensions are valid
    if copy_h > 0 and copy_w > 0:
        pattern_to_copy = source_pattern[:copy_h, :copy_w]
        output_grid[target_inner_top : target_inner_top + copy_h,
                    target_inner_left : target_inner_left + copy_w] = pattern_to_copy


# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation: finds a unique pattern rectangle and copies its
    inner pattern into simple rectangles of the same color as the pattern's frame.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = input_grid_np.copy()
    h, w = input_grid_np.shape
    # Keep track of visited pixels to avoid processing objects multiple times
    visited = np.zeros_like(input_grid_np, dtype=bool)

    all_objects = []

    # 1. Find and classify all solid rectangular objects
    for r in range(h):
        for c in range(w):
            # If pixel is non-background and not yet visited, start BFS
            if input_grid_np[r, c] != 0 and not visited[r, c]:
                # Find all connected non-background pixels for this component
                coords = bfs_find_connected(input_grid_np, (r, c), visited)

                if coords:
                    # Calculate the bounding box for the component
                    bbox = get_bounding_box(coords)

                    # Check if the component perfectly fills its bounding box (is a solid rectangle)
                    if is_solid_rectangle(input_grid_np, coords, bbox):
                        # Classify the solid rectangle
                        obj_info = classify_rectangle(input_grid_np, bbox)
                        if obj_info:
                            all_objects.append(obj_info)
                    # else:
                    # Component is not a solid rectangle, ignore it

    # 2. Separate simple and pattern objects (assuming only one pattern)
    simple_rects = []
    pattern_rect = None
    for obj in all_objects:
        if obj['type'] == 'simple':
            simple_rects.append(obj)
        elif obj['type'] == 'pattern':
            if pattern_rect is None: # Store the first pattern rect found
                pattern_rect = obj
            # else: Ignore subsequent pattern rects if assumption holds

    # 3. Apply transformation if a pattern rectangle was found
    if pattern_rect is None:
        # No pattern rectangle found, return the original grid
        return output_grid.tolist()

    # Get pattern details
    pattern_frame_color = pattern_rect['frame_color']
    source_pattern = pattern_rect['inner_pattern']

    # 4. Iterate through simple rectangles and apply the pattern if colors match and size allows
    for simple_obj in simple_rects:
        # Check if the simple rectangle's color matches the pattern's frame color
        if simple_obj['color'] == pattern_frame_color:
            min_r, min_c, max_r, max_c = simple_obj['bbox']
            simple_h = max_r - min_r + 1
            simple_w = max_c - min_c + 1

            # Check if the simple rectangle is large enough to have an interior (at least 3x3)
            if simple_h >= 3 and simple_w >= 3:
                # Paste the pattern (handles cropping internally)
                paste_pattern(output_grid, simple_obj['bbox'], source_pattern)

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 6 6 6 6 6 6 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 6 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 6 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 70
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 15.555555555555543

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 1 1 1 1 1 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 1 1 1 1 1 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 1 1 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 1 1 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 4 4 1 1 8 8 8 1 1 4 4 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 4 4 4 4 4 4 4 4 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 1 1 1 1 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 1 1 8 8 8 8 1 1 4 4 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 77
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 19.012345679012356

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 4 4 4 4 4 4 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 4 2 2 2 2 4 8 8 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 4 4 4 4 4 4 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 4 4 4 4 4 4 4 4 4 4 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 2 2 2 2 2 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 2 2 2 2 2 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 2 2 2 2 2 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 2 2 2 2 2 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 2 2 2 2 2 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 4 4 4 4 4 4 4 4 4 4 4 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 4 4 4 4 4 4 4 8 0
0 0 0 0 8 8 4 2 2 2 2 2 4 8 8 0 0 0 0 8 8 4 2 2 2 2 2 4 8 0
0 0 0 0 8 8 4 4 4 4 4 4 4 8 8 0 0 0 0 8 8 4 2 2 2 2 2 4 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 4 2 2 2 2 2 4 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 4 4 4 4 4 4 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 4 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 4 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 2 2 2 2 2 4 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 4 4 4 4 4 4 4 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 74
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.44444444444443
