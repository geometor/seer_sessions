import numpy as np
from collections import Counter
from collections import deque

"""
Identifies the largest hollow rectangular frame in the input grid, extracts the subgrid defined by its bounding box, 
and transforms the interior background pixels. The transformation rule is: change an interior background pixel 
to the interior object color if there is any pixel of the interior object color in the same row or same column 
within the subgrid's interior.

1. Find the most frequent color (overall background, `C_main_bg`).
2. Find all connected objects of colors other than `C_main_bg`.
3. For each object, check if it forms a hollow rectangle:
    a. All pixels of the object must lie on the perimeter of its bounding box.
    b. All pixels *on* the perimeter of the bounding box must belong to the object.
    c. The interior area defined by the bounding box must not contain any pixels of the object's color.
4. Identify the hollow rectangle object whose bounding box encloses the largest area. Let its color be `C_frame` and bounding box `BBox`.
5. Extract the subgrid corresponding to `BBox`. Initialize the `output_grid` with this subgrid.
6. Analyze the *interior* of the subgrid (excluding the frame border) in the *original* input grid slice:
    a. Identify the `C_internal_bg` color (most frequent color inside, usually `C_main_bg`).
    b. Identify the `C_object` color (the single color inside that is not `C_frame` or `C_internal_bg`).
    c. Find the set of relative row indices (`R_obj`) and column indices (`C_obj`) occupied by `C_object` pixels within the interior.
7. Iterate through the interior pixels `(r, c)` of the `output_grid`.
8. If `output_grid[r, c]` is `C_internal_bg`:
    a. Check if the relative row index `(r-1)` is in `R_obj` OR the relative column index `(c-1)` is in `C_obj`.
    b. If true, change `output_grid[r, c]` to `C_object`.
9. Return the modified `output_grid`.
"""

def find_objects(grid, ignore_color):
    """
    Finds all connected objects of colors not equal to ignore_color using BFS.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != ignore_color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_color = color
                is_connected_component = True # Flag to ensure all parts have the same color

                while q:
                    curr_r, curr_c = q.popleft()
                    if grid[curr_r, curr_c] != obj_color:
                        is_connected_component = False # Should not happen with BFS start condition, but safe check
                        # This object is invalid, maybe stop BFS? Or just mark it.
                        # For simplicity, let's assume BFS finds single-color components correctly.

                    obj_coords.add((curr_r, curr_c))

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == obj_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if is_connected_component and obj_coords:
                    objects.append({'coords': obj_coords, 'color': obj_color})
    return objects

def get_bounding_box(coords):
    """
    Calculates the bounding box for a set of coordinates.
    """
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

def is_hollow_rectangle(grid, obj_color, obj_coords, bbox):
    """
    Checks if an object forms a hollow rectangle within its bounding box.
    """
    if bbox is None:
        return False
    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Must have dimensions > 1 to have an interior
    if height <= 1 or width <= 1:
        return False

    # Check 1: All object pixels must lie strictly on the perimeter
    for r, c in obj_coords:
        if not (r == min_r or r == max_r or c == min_c or c == max_c):
            return False  # Pixel is inside, not on perimeter

    # Check 2: All perimeter coordinates must have the object color
    perimeter_coords_count = 0
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Check if coordinate is on the perimeter
            is_on_perimeter = (r == min_r or r == max_r or c == min_c or c == max_c)
            if is_on_perimeter:
                 # Check grid bounds (should be within bbox, but safety)
                 if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                     if grid[r, c] != obj_color:
                         return False # Perimeter pixel has wrong color
                     perimeter_coords_count +=1
                 else:
                     return False # Bbox extends outside grid? Should not happen.

    # Check 2b: The number of object pixels must exactly match the number of perimeter pixels
    if len(obj_coords) != perimeter_coords_count:
         return False # Object doesn't perfectly cover the perimeter

    # Check 3: Interior must not contain the object color
    if height > 2 and width > 2: # Only check interior if it exists
        for r in range(min_r + 1, max_r):
            for c in range(min_c + 1, max_c):
                 # Check grid bounds (should be within bbox)
                 if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                    if grid[r, c] == obj_color:
                        return False # Found object color inside
                 else:
                     return False # Bbox extends outside grid?

    return True


def transform(input_grid):
    """
    Applies the frame-finding and interior transformation rule.
    """
    np_grid = np.array(input_grid, dtype=int)
    rows, cols = np_grid.shape

    # 1. Identify overall background color (most frequent)
    # Note: In examples, it's Azure 8, but let's compute it
    colors, counts = np.unique(np_grid, return_counts=True)
    if len(colors) > 0:
         overall_background_color = colors[np.argmax(counts)]
    else:
         return [] # Empty input grid?

    # 2. Find all distinct connected objects (excluding overall background)
    # We need to find frames which might be the background color if it's not overall most frequent.
    # Let's find all objects first.
    all_objects = find_objects(np_grid, -1) # Find all objects, including potential background ones if they form shapes
    
    # Filter out objects that ARE the overall background color, unless it's the only color.
    candidate_objects = [obj for obj in all_objects if obj['color'] != overall_background_color or len(colors) == 1]
    if not candidate_objects and len(colors) > 1: # If only background color object was found, add it back as candidate. Allows background color frames.
         candidate_objects = [obj for obj in all_objects if obj['color'] == overall_background_color]


    # 3. Filter for hollow rectangles and find the largest
    largest_frame_bbox = None
    largest_frame_obj = None
    max_area = -1

    for obj in candidate_objects:
        coords = obj['coords']
        color = obj['color']
        bbox = get_bounding_box(coords)

        if bbox:
            # Check if it's a hollow rectangle using the refined function
            if is_hollow_rectangle(np_grid, color, coords, bbox):
                min_r, min_c, max_r, max_c = bbox
                area = (max_r - min_r + 1) * (max_c - min_c + 1)
                # Keep track of the largest one found so far
                if area > max_area:
                    max_area = area
                    largest_frame_bbox = bbox
                    largest_frame_obj = obj

    # 4. Check if a frame was found
    if largest_frame_bbox is None:
        # No hollow rectangle found - return empty or original?
        # Based on ARC tasks, expect one. Maybe return input? Or empty. Let's return input.
        # return input_grid # Or raise error, or return []
        # Let's try returning empty list based on previous code run result format when fails
        return [] 


    # 5. Extract the subgrid
    min_r, min_c, max_r, max_c = largest_frame_bbox
    output_grid_np = np_grid[min_r:max_r + 1, min_c:max_c + 1].copy() # Use copy()
    output_h, output_w = output_grid_np.shape

    # Check if there is an interior to transform
    if output_h <= 2 or output_w <= 2:
        return output_grid_np.tolist() # No interior, return as is

    # 6. Analyze the Interior
    frame_color = largest_frame_obj['color']
    interior_slice = np_grid[min_r + 1:max_r, min_c + 1:max_c]
    
    if interior_slice.size == 0:
         return output_grid_np.tolist() # Should not happen if h,w > 2, but safe check

    int_colors, int_counts = np.unique(interior_slice, return_counts=True)
    int_color_counts = dict(zip(int_colors, int_counts))

    # Find internal background (most frequent IN INTERIOR, excluding frame color if present)
    internal_bg_color = -1 # Initialize
    max_count = -1
    potential_bg_colors = {c:cnt for c, cnt in int_color_counts.items() if c != frame_color}

    if not potential_bg_colors: # Interior only contains frame color? Invalid hollow rect check? Or just return.
         if int_colors[0] == frame_color and len(int_colors)==1:
              return output_grid_np.tolist() # Interior is filled with frame color, error in hollow check?
         # Handle case where interior only has one non-frame color
         elif len(int_colors) == 1:
             internal_bg_color = -1 # No background identifiable
             object_color = int_colors[0]
         elif len(potential_bg_colors) == 1:
              internal_bg_color = list(potential_bg_colors.keys())[0]
         else: # Find most frequent among potentials
              internal_bg_color = max(potential_bg_colors, key=potential_bg_colors.get)


    # Find object color (the one that's not frame and not internal bg)
    object_color = -1
    object_colors_found = []
    for c in int_colors:
        if c != frame_color and c != internal_bg_color:
            object_colors_found.append(c)

    if len(object_colors_found) == 1:
        object_color = object_colors_found[0]
    elif len(object_colors_found) == 0:
        # No distinct object color found, maybe only frame and bg. No transformation needed.
        return output_grid_np.tolist()
    else:
        # More than one object color - ambiguous based on examples.
        # For now, let's maybe pick the most frequent one? Or least frequent?
        # Let's stick to the assumption of one object color and potentially fail if > 1.
         # Or maybe just skip transformation? Let's skip.
         # print(f"Warning: Found multiple interior object colors: {object_colors_found}. Skipping transformation.") # Add logging if needed
         return output_grid_np.tolist()

    # 7. Find Object Locations (relative to interior)
    obj_rows_rel = set()
    obj_cols_rel = set()
    interior_h, interior_w = interior_slice.shape
    for r_rel in range(interior_h):
        for c_rel in range(interior_w):
            if interior_slice[r_rel, c_rel] == object_color:
                obj_rows_rel.add(r_rel)
                obj_cols_rel.add(c_rel)

    # 8. Transform Background Pixels in Output Grid's Interior
    for r in range(1, output_h - 1):
        for c in range(1, output_w - 1):
            if output_grid_np[r, c] == internal_bg_color:
                # Check row and column relative to interior
                r_rel = r - 1
                c_rel = c - 1
                if r_rel in obj_rows_rel or c_rel in obj_cols_rel:
                    output_grid_np[r, c] = object_color

    # 9. Return Result
    output_grid = output_grid_np.tolist()
    return output_grid
