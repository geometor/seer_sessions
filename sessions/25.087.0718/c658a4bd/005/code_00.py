import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Identify Objects:** Find all contiguous, non-white (0) objects in the input grid. For each object, record its color, pixel coordinates, bounding box (min/max row/col), height, width, and area (height * width). Use 4-way connectivity.
2.  **Filter Singletons:** Remove any objects with a bounding box area of 1 (single pixels) from the list.
3.  **Identify Frame Object:**
    *   Iterate through the remaining objects. Identify the unique object whose bounding box geometrically contains the bounding boxes of *all* other remaining objects. This is the 'Frame Object'.
    *   Record the frame object's color. Remove the frame object from the list of potential nested objects. (Assume exactly one such frame object exists).
4.  **Identify Nested Objects:** The remaining objects in the list are the 'Nested Objects'.
5.  **Sort Nested Objects:** Sort the nested objects by their bounding box area in ascending order (smallest area first).
6.  **Determine Output Size:**
    *   If the sorted list of nested objects is empty, the output is a 3x3 grid filled with the frame color.
    *   Otherwise, get the bounding box dimensions (height, width) of the *largest* area object in the sorted list.
    *   The output grid size is `(largest_height + 2)` x `(largest_width + 2)`.
7.  **Construct Output Grid:**
    *   Create an empty grid of the calculated output size, filled entirely with the frame color.
    *   Iterate through the sorted nested objects from *largest area* to *smallest area* (reverse order of the sorted list).
    *   For each object, retrieve its original pixel grid representation (`obj['grid']`) and bounding box dimensions (`obj_h`, `obj_w`).
    *   Calculate the top-left position `(start_row, start_col)` to center its bounding box within the output grid's inner area (excluding the 1-pixel border). Calculation: `start_row = (output_h - obj_h) // 2`, `start_col = (output_w - obj_w) // 2`.
    *   Place the object's pixels onto the output grid at `(start_row, start_col)`, overwriting existing pixels. Only copy non-zero pixels from the object's grid (`obj['grid']`).
8.  **Add Central Red Pixel (Conditional):**
    *   If nested objects were placed:
        *   Identify the innermost (smallest area) object from the sorted list.
        *   Get its bounding box dimensions (`inner_h`, `inner_w`).
        *   If *both* `inner_h` and `inner_w` are odd, calculate the absolute center coordinates of the *output grid*: `center_row = output_h // 2`, `center_col = output_w // 2`.
        *   Set the pixel at `(center_row, center_col)` to Red (2).
"""

# Helper function to find connected components (objects) using 4-way connectivity
def find_objects(grid):
    """Finds all connected components of non-background pixels."""
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                q = deque([(r, c)])
                points = set([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # 4-way connectivity
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            points.add((nr, nc))

                bbox = (min_r, min_c, max_r, max_c)
                bbox_h = max_r - min_r + 1
                bbox_w = max_c - min_c + 1
                obj_grid = extract_object_grid(grid, points, bbox)
                objects.append({
                    'id': len(objects), # Unique ID for reference
                    'color': color,
                    'points': points,
                    'bbox': bbox,
                    'grid': obj_grid,
                    'bbox_h': bbox_h,
                    'bbox_w': bbox_w,
                    'bbox_area': bbox_h * bbox_w,
                    'pixel_count': len(points) # Store actual pixel count
                 })
    return objects

# Helper function to extract the object's minimal grid representation
def extract_object_grid(grid, points, bbox):
    """Extracts the object's minimal grid representation based on its points."""
    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    obj_grid = np.zeros((height, width), dtype=int)
    color = 0
    # Determine the color from the first point (all points have the same color)
    if points:
        first_r, first_c = next(iter(points))
        color = grid[first_r, first_c]

    for r_idx in range(height):
        for c_idx in range(width):
            if (r_idx + min_r, c_idx + min_c) in points:
                 obj_grid[r_idx, c_idx] = color
    return obj_grid

# Helper function to check if bbox1 contains bbox2
def bbox_contains(bbox1, bbox2):
    """Checks if bbox1 completely contains bbox2."""
    min_r1, min_c1, max_r1, max_c1 = bbox1
    min_r2, min_c2, max_r2, max_c2 = bbox2
    return min_r1 <= min_r2 and min_c1 <= min_c2 and \
           max_r1 >= max_r2 and max_c1 >= max_c2

def transform(input_grid_list):
    """
    Applies the transformation rules to the input grid.
    Input is expected as a list containing one numpy array.
    """
    input_grid = np.array(input_grid_list)

    # 1. Identify Objects
    all_objects = find_objects(input_grid)

    # Handle case where input grid might be empty or only contain background
    if not all_objects:
        # Default to a 3x3 white grid if no objects found
        return np.zeros((3, 3), dtype=int).tolist()

    # 2. Filter Singletons
    significant_objects = [obj for obj in all_objects if obj['bbox_area'] > 1]

    # Handle case where only singletons were present
    if not significant_objects:
         # Default to a 3x3 white grid if only singletons found
        return np.zeros((3, 3), dtype=int).tolist()

    # 3. Identify Frame Object
    frame_object = None
    frame_color = 0 # Default to white
    nested_objects = []

    if len(significant_objects) == 1:
        # If only one significant object exists, it must be the frame
        frame_object = significant_objects[0]
        frame_color = frame_object['color']
        # nested_objects remains empty
    else:
        for i, candidate_frame in enumerate(significant_objects):
            is_frame = True
            others = significant_objects[:i] + significant_objects[i+1:]
            if not others: # Should not happen if len > 1, but safe check
                is_frame = False
                break
            for other_obj in others:
                if not bbox_contains(candidate_frame['bbox'], other_obj['bbox']):
                    is_frame = False
                    break
            if is_frame:
                frame_object = candidate_frame
                frame_color = frame_object['color']
                nested_objects = others # All other significant objects are nested
                break

    # Handle edge case where no frame object is found (e.g., overlapping objects not contained)
    if frame_object is None:
        # Fallback: Perhaps return the input or a default grid?
        # For now, let's assume a frame always exists per the problem structure.
        # If rigorously needed, pick the object with the largest bbox as frame?
        # Let's default to 3x3 of the most frequent color or largest obj color.
        if significant_objects:
            significant_objects.sort(key=lambda o: o['bbox_area'], reverse=True)
            frame_color = significant_objects[0]['color']
        else: # Only singletons existed initially
             all_objects.sort(key=lambda o: o['bbox_area'], reverse=True) # Find largest singleton
             frame_color = all_objects[0]['color'] if all_objects else 0

        print("Warning: Could not identify a unique enclosing frame object. Defaulting.")
        return np.full((3, 3), frame_color, dtype=int).tolist()


    # 4. Identify Nested Objects - Already done during frame identification

    # 5. Sort Nested Objects by BBox Area (Ascending)
    nested_objects.sort(key=lambda o: o['bbox_area'])

    # 6. Determine Output Size
    if not nested_objects:
        # Only frame object existed (after filtering singletons)
        output_grid = np.full((3, 3), frame_color, dtype=int)
        return output_grid.tolist()
    else:
        largest_nested_object = nested_objects[-1] # Largest area is last after sort
        largest_h, largest_w = largest_nested_object['bbox_h'], largest_nested_object['bbox_w']
        output_h = largest_h + 2
        output_w = largest_w + 2

    # 7. Construct Output Grid
    #    a. Create grid with frame color
    output_grid = np.full((output_h, output_w), frame_color, dtype=int)

    #    b. Place objects (largest area first -> smallest area last)
    for obj in reversed(nested_objects): # Iterate largest to smallest area
        obj_h, obj_w = obj['bbox_h'], obj['bbox_w']
        obj_grid_repr = obj['grid'] # Use the stored minimal grid representation

        # Calculate top-left corner for centering within the output grid (inside the frame border)
        start_r = (output_h - obj_h) // 2
        start_c = (output_w - obj_w) // 2

        # Place object pixels onto output grid, overwriting frame/previous objects
        for r in range(obj_h):
            for c in range(obj_w):
                if obj_grid_repr[r, c] != 0: # Only copy the object's actual pixels (non-background)
                    # Check bounds just in case, though centering should be correct
                    if 0 <= start_r + r < output_h and 0 <= start_c + c < output_w:
                         output_grid[start_r + r, start_c + c] = obj_grid_repr[r, c]

    # 8. Add Central Red Pixel (Conditional)
    if nested_objects: # Ensure there was at least one nested object placed
        innermost_object = nested_objects[0] # Smallest area object
        inner_h, inner_w = innermost_object['bbox_h'], innermost_object['bbox_w']

        # Check if both dimensions of the *innermost* object's bounding box are odd
        if inner_h % 2 != 0 and inner_w % 2 != 0:
            center_r = output_h // 2
            center_c = output_w // 2
            # Ensure center coords are within grid bounds (should always be true for calculated output size)
            if 0 <= center_r < output_h and 0 <= center_c < output_w:
                output_grid[center_r, center_c] = 2 # Set center to Red

    # Return as list of lists
    return output_grid.tolist()