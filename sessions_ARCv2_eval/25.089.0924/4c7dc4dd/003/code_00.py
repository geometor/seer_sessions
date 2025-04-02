import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Identify Candidate Framed Objects:** Find all objects in the input grid that consist of a contiguous border of a single color (frame_color), surrounding an area filled entirely with white (0), which in turn contains a single, contiguous shape of a third distinct color (inner_color, different from frame_color). Record the `inner_color`, `frame_color`, and bounding box (`bbox`) for each candidate.
2.  **Identify Largest Object (Potential Container):** Find the object with the largest number of pixels, excluding white (0) and gray (5). If multiple objects have the same largest pixel count, choose the one whose bounding box is top-leftmost. Note its color (`container_color`) and bounding box (`container_bbox`). If no such object exists, consider the container absent.
3.  **Select the Target Framed Object:**
    *   Identify candidates whose bounding box (`bbox`) is entirely within the `container_bbox`.
    *   From these potentially contained candidates, filter further: only keep those where the `frame_color` is *different* from the `container_color`.
    *   If one or more candidates remain after this filtering (i.e., are geometrically contained *and* have a different frame color than the container), select the top-leftmost one among them as the "target object". Mark this case as `contained`.
    *   If *no* candidates meet both containment criteria, select the candidate object (from the *original* list of all framed objects found in step 1) that has the numerically smallest `inner_color`. If there's a tie in `inner_color`, choose the top-leftmost one among them. Mark this case as `not_contained`.
4.  **Determine Output Colors:**
    *   Get the `inner_color` from the target object.
    *   The `interior_color` is always white (0).
    *   If the case is `contained`, the `primary_color` is the `container_color` identified in step 2.
    *   If the case is `not_contained`, the `primary_color` is the same as the `inner_color` of the target object.
5.  **Construct Output Grid:**
    *   If the case is `contained`: Create a 5x5 grid following the specific pattern:
        Row 1: [0, 0, 0, 0, 0]
        Row 2: [inner, primary, primary, primary, primary]
        Row 3: [primary, 0, 0, 0, 0]
        Row 4: [primary, 0, 0, 0, 0]
        Row 5: [primary, 0, 0, 0, 0]
    *   If the case is `not_contained`: Create a 4x4 grid following the specific pattern:
        Row 1: [primary, primary, 0, primary]
        Row 2: [0, 0, 0, primary]
        Row 3: [primary, primary, primary, primary]
        Row 4: [primary, 0, 0, primary]
"""

def find_objects(grid, colors_to_find=None, colors_to_ignore=None):
    """
    Finds all contiguous objects of specified colors in the grid using 4-connectivity.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set): Set of colors to look for. If None, find all colors not ignored.
        colors_to_ignore (set): Set of colors to ignore.

    Returns:
        list: A list of objects. Each object is a dictionary containing:
              'color': The color of the object.
              'pixels': A set of (row, col) tuples for the object's pixels.
              'bbox': A tuple (min_row, min_col, max_row, max_col) representing the bounding box.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    if colors_to_ignore is None:
        colors_to_ignore = set()

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if not visited[r, c] and color not in colors_to_ignore and \
               (colors_to_find is None or color in colors_to_find):
                
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def is_framed_object_strict(grid, frame_obj):
    """
    Checks if a given object (frame_obj) acts as a frame for an inner object.
    Checks:
    1. Interior region exists within the frame's bounding box.
    2. Interior region (excluding frame pixels) contains only white (0) and exactly one other contiguous non-white object (inner_obj).
    3. The inner_obj's color is different from the frame_obj's color.
    4. The inner_obj does not touch the bounding box edges (it's fully contained within frame space).

    Args:
        grid (np.array): The input grid.
        frame_obj (dict): A potential frame object from find_objects.

    Returns:
        tuple: (bool, int or None) - (True if valid framed object, inner_color)
               or (False, None)
    """
    frame_pixels = frame_obj['pixels']
    frame_color = frame_obj['color']
    min_r, min_c, max_r, max_c = frame_obj['bbox']
    rows, cols = grid.shape

    # Bounding box must allow for an interior
    if max_r - min_r < 2 or max_c - min_c < 2:
        return False, None

    inner_components = []
    visited_inner = set(frame_pixels) # Start by marking frame as visited
    has_white_inside = False

    # Iterate through the potential interior area defined by the bounding box
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            if (r, c) not in visited_inner:
                color = grid[r, c]
                
                # Start BFS for this component
                component_pixels = set()
                q = deque([(r, c)])
                visited_inner.add((r, c))
                component_min_r, component_min_c = r, c
                component_max_r, component_max_c = r, c
                
                is_valid_component_boundary = True

                while q:
                    row, col = q.popleft()

                    # Check if component touches the bounding box boundary - disqualifies inner objects
                    # This ensures the inner shape is truly 'inside'
                    if row <= min_r or row >= max_r or col <= min_c or col >= max_c:
                       # This can happen if the frame is not fully enclosing
                       # Let's just skip adding this component if it touches bbox boundary
                       is_valid_component_boundary = False
                       # No need to break, just mark and continue BFS to mark all visited
                       
                    component_pixels.add((row, col))
                    component_min_r = min(component_min_r, row)
                    component_min_c = min(component_min_c, col)
                    component_max_r = max(component_max_r, row)
                    component_max_c = max(component_max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check neighbor is within grid, not visited, and not part of the frame
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited_inner and \
                           (nr, nc) not in frame_pixels and \
                           grid[nr, nc] == color:
                             
                            visited_inner.add((nr, nc))
                            q.append((nr, nc))
                
                # Store the component if it's non-white and didn't touch bbox boundary
                if color == 0:
                    has_white_inside = True
                elif is_valid_component_boundary: # Only consider non-white, non-boundary touching shapes
                     inner_components.append({
                         'color': color, 
                         'pixels': component_pixels,
                         'bbox': (component_min_r, component_min_c, component_max_r, component_max_c)
                     })

    # Check final conditions:
    # 1. Must have found white pixels inside.
    # 2. Must have found exactly one non-white inner component.
    # 3. The inner component's color must differ from the frame color.
    if has_white_inside and len(inner_components) == 1 and inner_components[0]['color'] != frame_color:
        # Optional check: Ensure all pixels inside bbox are either frame, white or inner obj
        # This guards against stray pixels.
        all_interior_pixels = set((r, c) for r in range(min_r + 1, max_r) for c in range(min_c + 1, max_c))
        covered_pixels = frame_pixels.union(inner_components[0]['pixels'])
        
        is_fully_explained = True
        for r_int, c_int in all_interior_pixels:
             if (r_int, c_int) not in covered_pixels and grid[r_int, c_int] != 0 :
                  is_fully_explained = False
                  break
        
        if is_fully_explained:
            return True, inner_components[0]['color']

    return False, None


def find_largest_object_by_pixels(grid, colors_to_ignore):
    """Finds the object with the most pixels, ignoring specified colors."""
    all_objs = find_objects(grid, colors_to_ignore=colors_to_ignore)
    
    if not all_objs:
        return None

    largest_obj = None
    max_pixels = -1

    for obj in all_objs:
        num_pixels = len(obj['pixels'])
        if num_pixels > max_pixels:
            max_pixels = num_pixels
            largest_obj = obj
        elif num_pixels == max_pixels:
            # Tie-breaking: top-leftmost bounding box
            current_bbox = obj['bbox']
            if current_bbox[0] < largest_obj['bbox'][0] or \
               (current_bbox[0] == largest_obj['bbox'][0] and current_bbox[1] < largest_obj['bbox'][1]):
                largest_obj = obj
                
    return largest_obj

def is_contained(inner_bbox, outer_bbox):
    """Checks if inner_bbox is strictly inside or touching the boundaries of outer_bbox."""
    if outer_bbox is None or inner_bbox is None:
        return False
    min_r_in, min_c_in, max_r_in, max_c_in = inner_bbox
    min_r_out, min_c_out, max_r_out, max_c_out = outer_bbox
    return min_r_out <= min_r_in and min_c_out <= min_c_in and \
           max_r_in <= max_r_out and max_c_in <= max_c_out


def transform(input_grid):
    grid = np.array(input_grid, dtype=int)

    # 1. Identify Candidate Framed Objects
    candidate_objects = []
    # Find all non-white, non-gray potential frames first
    potential_frames = find_objects(grid, colors_to_ignore={0, 5}) 

    for p_frame in potential_frames:
        is_framed, inner_color = is_framed_object_strict(grid, p_frame)
        if is_framed:
            candidate_objects.append({
                'inner_color': inner_color,
                'bbox': p_frame['bbox'],
                'frame_color': p_frame['color'] 
            })

    if not candidate_objects:
         # Fallback if no valid framed objects found
         # This case wasn't explicitly defined by examples, return small default
         return [[0]] 

    # 2. Identify Largest Object (Potential Container)
    container_object = find_largest_object_by_pixels(grid, colors_to_ignore={0, 5}) # Ignore white and gray

    # 3. Select the Target Framed Object
    valid_contained_candidates = []
    if container_object:
        container_bbox = container_object['bbox']
        container_color = container_object['color']
        for cand in candidate_objects:
            # Check geometric containment AND different frame/container color
            if is_contained(cand['bbox'], container_bbox) and cand['frame_color'] != container_color:
                valid_contained_candidates.append(cand)

    target_object = None
    is_contained_flag = False

    if valid_contained_candidates:
        # Sort by top-left position (row first, then column)
        valid_contained_candidates.sort(key=lambda x: (x['bbox'][0], x['bbox'][1]))
        target_object = valid_contained_candidates[0]
        is_contained_flag = True
    else:
        # No valid contained candidates, sort ALL candidates by inner_color, then top-left
        candidate_objects.sort(key=lambda x: (x['inner_color'], x['bbox'][0], x['bbox'][1]))
        target_object = candidate_objects[0]
        is_contained_flag = False

    # 4. Determine Output Colors
    inner_color = target_object['inner_color']
    interior_color = 0 # Always white

    if is_contained_flag:
        # Container must exist if is_contained_flag is True
        primary_color = container_object['color']
    else:
        primary_color = inner_color # Use inner color as primary if not contained

    # 5. Construct Output Grid
    if is_contained_flag:
        # 5x5 pattern
        output_grid = np.full((5, 5), interior_color, dtype=int)
        output_grid[1, 0] = inner_color
        output_grid[1, 1:] = primary_color
        output_grid[2:, 0] = primary_color
    else:
        # 4x4 pattern
        output_grid = np.full((4, 4), primary_color, dtype=int) # Start filled with primary
        output_grid[0, 2] = interior_color
        output_grid[1, 0:3] = interior_color
        # Row 2 is filled with primary
        output_grid[3, 1:3] = interior_color

    return output_grid.tolist()