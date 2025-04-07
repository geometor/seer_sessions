```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Identify Candidate Framed Objects:** Find all objects in the input grid that consist of a contiguous border of a single color (frame_color, excluding white=0 and gray=5), surrounding an interior region within its bounding box. This interior region must contain:
    a. At least one white (0) pixel.
    b. Exactly one contiguous object of a third color (inner_color), which must be different from the frame_color.
    c. All other pixels within the interior region must be white (0).
    Record the `inner_color`, `frame_color`, and bounding box (`bbox`) for each valid candidate.
2.  **Identify Largest Solid Rectangular Block (Potential Container):** Find the solid rectangular block with the largest area, consisting of a single color excluding white (0) and gray (5). If multiple blocks share the maximum area, choose the one whose top-left corner is highest, breaking further ties by choosing the leftmost one. Note its color (`container_color`) and bounding box (`container_bbox`). If no such block exists, consider the container absent.
3.  **Select the Target Framed Object:**
    a.  Identify candidate framed objects whose bounding box (`bbox`) is entirely contained within or touches the boundary of the `container_bbox`.
    b.  If one or more candidates are contained within the container block's bounding box, select the one whose top-left corner is highest, breaking further ties by choosing the leftmost one. This is the "target object". Mark this case as `contained`.
    c.  If *no* candidates are contained within the container block's bounding box, select the candidate object (from the *original* list of all valid framed objects found in step 1) that has the numerically smallest `inner_color`. If there's a tie in `inner_color`, choose the one whose top-left corner is highest, breaking further ties by choosing the leftmost one. This is the "target object". Mark this case as `not_contained`.
4.  **Determine Output Colors:**
    a.  Get the `inner_color` from the target object.
    b.  The `interior_color` is always white (0).
    c.  If the case is `contained`, the `primary_color` is the `container_color` identified in step 2.
    d.  If the case is `not_contained`, the `primary_color` is the same as the `inner_color` of the target object.
5.  **Construct Output Grid:**
    a.  If the case is `contained`: Create a 5x5 grid following the specific pattern:
        Row 1: [0, 0, 0, 0, 0]
        Row 2: [inner, primary, primary, primary, primary]
        Row 3: [primary, 0, 0, 0, 0]
        Row 4: [primary, 0, 0, 0, 0]
        Row 5: [primary, 0, 0, 0, 0]
    b.  If the case is `not_contained`: Create a 4x4 grid following the specific pattern:
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
            # Process pixel if not visited, not ignored, and either find all or in specific set
            if not visited[r, c] and color not in colors_to_ignore and \
               (colors_to_find is None or color in colors_to_find):
                
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is same color and not visited
                            if not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Store the found object
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def is_framed_object(grid, frame_obj):
    """
    Checks if a given object (frame_obj) acts as a valid frame for an inner object.

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

    # Frame bounding box must be large enough to potentially contain an interior
    if max_r - min_r < 2 or max_c - min_c < 2:
        return False, None

    inner_components_non_white = [] # Stores non-white components found inside
    visited_interior = set() # Tracks visited pixels within the interior search
    has_white_inside = False
    all_interior_pixels = set() # Track all non-frame pixels inside the bbox

    # Define the interior bounding box
    interior_min_r, interior_min_c = min_r + 1, min_c + 1
    interior_max_r, interior_max_c = max_r - 1, max_c - 1

    # Iterate only within the potential interior (inside the frame's bounding box)
    for r in range(interior_min_r, interior_max_r + 1):
        for c in range(interior_min_c, interior_max_c + 1):
            # Only consider pixels that are NOT part of the frame itself
            if (r, c) not in frame_pixels:
                 all_interior_pixels.add((r,c))
                 # If this interior pixel hasn't been visited by a previous component search
                 if (r,c) not in visited_interior:
                    color = grid[r, c]
                    
                    # Start BFS for this component within the interior region
                    component_pixels = set()
                    q = deque([(r, c)])
                    visited_interior.add((r, c))
                    
                    while q:
                        row, col = q.popleft()
                        component_pixels.add((row, col))

                        # Explore neighbors (4-connectivity)
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = row + dr, col + dc
                            
                            # Check neighbor is within the INTERIOR bounds,
                            # not frame, not visited, and same color
                            if interior_min_r <= nr <= interior_max_r and \
                               interior_min_c <= nc <= interior_max_c and \
                               (nr, nc) not in frame_pixels and \
                               (nr, nc) not in visited_interior and \
                               grid[nr, nc] == color:
                                
                                visited_interior.add((nr, nc))
                                q.append((nr, nc))
                    
                    # After BFS for the component, record it
                    if color == 0:
                        has_white_inside = True
                        # We process white components fully to mark visited, but don't store them
                    elif color != frame_color: # Must be different from frame color
                         inner_components_non_white.append({
                             'color': color, 
                             'pixels': component_pixels,
                         })
                    # If color == frame_color, it's invalid, just ignore the component

    # --- Final Validation Checks ---
    # 1. Must have found at least one white pixel in the interior.
    if not has_white_inside:
        return False, None

    # 2. Must have found exactly one non-white inner component, different from frame color.
    if len(inner_components_non_white) != 1:
        return False, None
        
    # 3. Check if all interior pixels are accounted for (either white or the single inner component)
    inner_pixels_found = inner_components_non_white[0]['pixels']
    for p in all_interior_pixels:
         # If an interior pixel was not visited (e.g., isolated white) or is not part of the inner object
         # and is not white, then the interior is not clean.
         if p not in visited_interior or (p not in inner_pixels_found and grid[p] != 0):
             return False, None # Stray pixel or unvisited area found
             
    # If all checks pass
    return True, inner_components_non_white[0]['color']


def find_largest_solid_block(grid, colors_to_ignore):
    """Finds the largest solid rectangular block of a single color, ignoring specified colors."""
    rows, cols = grid.shape
    max_area = -1
    largest_block = None # Store {'color': c, 'bbox': (min_r, min_c, max_r, max_c)}

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Skip ignored colors
            if color in colors_to_ignore:
                continue

            # Determine the maximum possible width starting at (r, c) for this color
            max_w = 0
            for w in range(1, cols - c + 1):
                if grid[r, c + w - 1] == color:
                    max_w = w
                else:
                    break # Width extension stops
            
            # For each possible width, find the maximum height
            min_h_for_width = rows # Optimization: track min height for width > 1
            for w in range(1, max_w + 1):
                h = 0
                # Check rows downwards, but not beyond the minimum height found for previous widths
                for current_h in range(1, min_h_for_width + 1):
                    # Ensure we don't go past grid bounds
                    if r + current_h - 1 >= rows:
                         break
                         
                    is_solid_row_segment = True
                    # Check if the entire row segment matches the color
                    for k in range(w):
                        if grid[r + current_h - 1, c + k] != color:
                            is_solid_row_segment = False
                            break
                    
                    if is_solid_row_segment:
                        h = current_h # Extend height
                    else:
                        break # Height expansion stops here for width w
                
                min_h_for_width = h # Update min height for next width check

                # Calculate area and update largest block if needed
                area = w * h
                if area > max_area:
                    max_area = area
                    largest_block = {'color': color, 'bbox': (r, c, r + h - 1, c + w - 1)}
                elif area == max_area and largest_block is not None:
                     # Tie-breaking: top-leftmost (compare top row, then left column)
                     current_bbox = (r, c, r + h - 1, c + w - 1)
                     if current_bbox[0] < largest_block['bbox'][0] or \
                        (current_bbox[0] == largest_block['bbox'][0] and current_bbox[1] < largest_block['bbox'][1]):
                         largest_block = {'color': color, 'bbox': current_bbox}

    return largest_block

def is_contained(inner_bbox, outer_bbox):
    """Checks if inner_bbox is strictly inside or touching the boundaries of outer_bbox."""
    if outer_bbox is None or inner_bbox is None:
        return False
    min_r_in, min_c_in, max_r_in, max_c_in = inner_bbox
    min_r_out, min_c_out, max_r_out, max_c_out = outer_bbox
    # Check if all corners of inner are within or on the boundary of outer
    return min_r_out <= min_r_in and min_c_out <= min_c_in and \
           max_r_in <= max_r_out and max_c_in <= max_c_out

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    colors_to_ignore_objects = {0, 5} # Colors to ignore for frames and containers

    # --- Step 1: Identify Candidate Framed Objects ---
    candidate_objects = []
    # Find all non-white, non-gray objects as potential frames
    potential_frames = find_objects(grid, colors_to_ignore=colors_to_ignore_objects) 

    # Validate each potential frame using the refined check
    for p_frame in potential_frames:
        is_valid_frame, inner_color = is_framed_object(grid, p_frame)
        if is_valid_frame:
            candidate_objects.append({
                'inner_color': inner_color,
                'bbox': p_frame['bbox'],
                'frame_color': p_frame['color'] 
            })

    # Handle case where no valid framed objects are found
    if not candidate_objects:
         # Return a minimal grid as fallback
         return [[0]] 

    # --- Step 2: Identify Largest Solid Rectangular Block (Potential Container) ---
    container_block = find_largest_solid_block(grid, colors_to_ignore=colors_to_ignore_objects) 

    # --- Step 3: Select the Target Framed Object ---
    contained_candidates = []
    if container_block:
        container_bbox = container_block['bbox']
        # Find candidates fully contained within the container's bounding box
        for cand in candidate_objects:
            if is_contained(cand['bbox'], container_bbox):
                contained_candidates.append(cand)

    target_object = None
    is_contained_flag = False

    if contained_candidates:
        # If candidates are contained, select the top-leftmost one
        # Sort by top row (bbox[0]), then left column (bbox[1])
        contained_candidates.sort(key=lambda x: (x['bbox'][0], x['bbox'][1]))
        target_object = contained_candidates[0]
        is_contained_flag = True
    else:
        # If no candidates are contained, select from ALL candidates
        # Sort by inner_color, then top row, then left column
        candidate_objects.sort(key=lambda x: (x['inner_color'], x['bbox'][0], x['bbox'][1]))
        target_object = candidate_objects[0]
        is_contained_flag = False

    # --- Step 4: Determine Output Colors ---
    inner_color = target_object['inner_color']
    interior_color = 0 # Always white

    if is_contained_flag:
        # If contained, primary color is the container's color
        # Container must exist if is_contained_flag is True
        primary_color = container_block['color']
    else:
        # If not contained, primary color is the inner color of the target
        primary_color = inner_color 

    # --- Step 5: Construct Output Grid ---
    if is_contained_flag:
        # Create the 5x5 pattern for contained objects
        output_grid = np.full((5, 5), interior_color, dtype=int) # Fill with white (0)
        output_grid[1, 0] = inner_color # Top-left of second row
        output_grid[1, 1:] = primary_color # Rest of second row
        output_grid[2:, 0] = primary_color # First column, rows 3-5
    else:
        # Create the 4x4 pattern for non-contained objects
        output_grid = np.full((4, 4), primary_color, dtype=int) # Fill with primary color
        # Set specific pixels to interior color (white 0)
        output_grid[0, 2] = interior_color
        output_grid[1, 0:3] = interior_color
        # Row 2 (index 2) remains primary color
        output_grid[3, 1:3] = interior_color

    # Return the result as a list of lists
    return output_grid.tolist()
```