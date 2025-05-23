import numpy as np
from collections import deque

"""
Identify candidate 'framed objects' in the input grid. A framed object has a border of one color, an interior of white (0), and a single contiguous inner shape of a third color.
Identify the largest solid rectangular block of a single color (excluding white=0 and gray=5), which acts as a potential container.
Select the target framed object:
  - If any framed objects are fully contained within the largest solid block, choose the top-leftmost one. Mark this as 'contained'.
  - Otherwise, choose the framed object with the numerically smallest inner color. Break ties using the top-leftmost position. Mark this as 'not_contained'.
Determine output colors:
  - inner_color: The color of the inner shape of the target framed object.
  - interior_color: Always white (0).
  - primary_color: If 'contained', it's the color of the container block. If 'not_contained', it's the inner_color.
Construct the output grid:
  - If 'contained', create a 5x5 grid using a specific pattern with inner_color, primary_color, and interior_color.
  - If 'not_contained', create a 4x4 grid using a specific pattern with primary_color (which equals inner_color) and interior_color.
"""

def find_objects(grid, colors_to_find=None, colors_to_ignore=None):
    """
    Finds all contiguous objects of specified colors in the grid.

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

def is_framed_object(grid, obj_pixels, obj_color, bbox):
    """
    Checks if a set of pixels represents a framed object.
    This is a simplified check focusing on the presence of an inner white area
    and a single non-white, non-border color shape within it.

    Args:
        grid (np.array): The input grid.
        obj_pixels (set): The pixels belonging to the potential frame.
        obj_color (int): The color of the potential frame.
        bbox (tuple): The bounding box of the potential frame.

    Returns:
        tuple: (bool, int or None) - (True if it's a framed object, inner_color)
               or (False, None)
    """
    min_r, min_c, max_r, max_c = bbox
    
    # Check if the bounding box area inside the frame contains white (0)
    has_white_inside = False
    inner_pixels = []
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            if (r,c) not in obj_pixels:
                 inner_pixels.append((r,c))
                 if grid[r,c] == 0:
                     has_white_inside = True

    if not has_white_inside or not inner_pixels:
        return False, None

    # Find connected components within the bounding box, *excluding* the frame pixels
    inner_objects = []
    visited_inner = set(obj_pixels) # Don't search starting from the frame

    for r_inner, c_inner in inner_pixels:
         if (r_inner, c_inner) not in visited_inner:
            color = grid[r_inner, c_inner]
            component_pixels = set()
            q = deque([(r_inner, c_inner)])
            visited_inner.add((r_inner, c_inner))
            is_valid_component = True

            while q:
                row, col = q.popleft()
                # Ensure component stays within the bounding box defined by frame
                if not (min_r < row < max_r and min_c < col < max_c):
                    # This component touches/crosses the frame boundary - invalid inner shape definition
                    # This check might be too strict depending on how frame is defined.
                    # Let's allow touching the inner boundary for now. Revisit if needed.
                    pass

                component_pixels.add((row, col))

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    # Check neighbor is within bounds, not part of the frame, not visited, and same color
                    if min_r <= nr <= max_r and min_c <= nc <= max_c and \
                       (nr, nc) not in obj_pixels and \
                       (nr, nc) not in visited_inner and \
                       grid[nr, nc] == color:
                        visited_inner.add((nr, nc))
                        q.append((nr, nc))

            if is_valid_component and color != 0: # Add only non-white components
                 inner_objects.append({'color': color, 'pixels': component_pixels})
            # We might also want to collect the white component to ensure it's contiguous,
            # but let's keep it simpler first.


    # A valid framed object should have exactly one non-white inner object,
    # and its color should be different from the frame color.
    if len(inner_objects) == 1 and inner_objects[0]['color'] != obj_color:
        return True, inner_objects[0]['color']
    
    return False, None


def find_largest_solid_block(grid, colors_to_ignore):
    """Finds the largest solid rectangular block of a single color, ignoring specified colors."""
    rows, cols = grid.shape
    max_area = -1
    largest_block = None # Store {'color': c, 'bbox': (r, c, r+h-1, c+w-1)}

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in colors_to_ignore:
                continue

            # Check max possible width from this point
            max_w = 0
            for w in range(1, cols - c + 1):
                if grid[r, c + w - 1] == color:
                    max_w = w
                else:
                    break
            
            # Check height for each potential width
            for w in range(1, max_w + 1):
                h = 0
                for current_h in range(1, rows - r + 1):
                    is_solid = True
                    # Check if the entire row segment matches the color
                    for k in range(w):
                        if grid[r + current_h - 1, c + k] != color:
                            is_solid = False
                            break
                    if is_solid:
                        h = current_h
                    else:
                        break # Height expansion stops here for width w
                
                # Update largest block if current one is bigger
                area = w * h
                if area > max_area:
                    max_area = area
                    largest_block = {'color': color, 'bbox': (r, c, r + h - 1, c + w - 1)}
                elif area == max_area and largest_block is not None:
                     # Tie-breaking: top-leftmost
                     current_bbox = (r, c, r + h - 1, c + w - 1)
                     if current_bbox[0] < largest_block['bbox'][0] or \
                        (current_bbox[0] == largest_block['bbox'][0] and current_bbox[1] < largest_block['bbox'][1]):
                         largest_block = {'color': color, 'bbox': current_bbox}


    return largest_block

def is_contained(inner_bbox, outer_bbox):
    """Checks if inner_bbox is strictly inside outer_bbox."""
    if outer_bbox is None:
        return False
    min_r_in, min_c_in, max_r_in, max_c_in = inner_bbox
    min_r_out, min_c_out, max_r_out, max_c_out = outer_bbox
    return min_r_out <= min_r_in and min_c_out <= min_c_in and \
           max_r_in <= max_r_out and max_c_in <= max_c_out

def transform(input_grid):
    """
    Transforms the input grid based on finding framed objects and a container block.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Identify Candidate Framed Objects
    candidate_objects = []
    # Find all objects first, excluding only white=0 initially might be better
    # Then filter them based on frame structure
    all_objects = find_objects(grid, colors_to_ignore={0}) # Find non-white objects

    for obj in all_objects:
        is_framed, inner_color = is_framed_object(grid, obj['pixels'], obj['color'], obj['bbox'])
        if is_framed:
            candidate_objects.append({
                'inner_color': inner_color,
                'bbox': obj['bbox'],
                'frame_color': obj['color'] # Keep frame color for potential later use
            })

    if not candidate_objects:
        # Handle cases where no framed objects are found (return empty or default?)
        # Based on examples, this shouldn't happen, but good practice.
        # Let's assume one will always be found according to the task logic.
        # If not, maybe return a small grid of 0s?
         return [[0]] * 3 # Placeholder for error/no object

    # 2. Identify Largest Solid Container
    container_block = find_largest_solid_block(grid, colors_to_ignore={0, 5}) # Ignore white and gray

    # 3. Select the Target Framed Object
    contained_candidates = []
    if container_block:
        container_bbox = container_block['bbox']
        for cand in candidate_objects:
            if is_contained(cand['bbox'], container_bbox):
                contained_candidates.append(cand)

    target_object = None
    is_contained_flag = False

    if contained_candidates:
        # Sort by top-left position (row first, then column)
        contained_candidates.sort(key=lambda x: (x['bbox'][0], x['bbox'][1]))
        target_object = contained_candidates[0]
        is_contained_flag = True
    else:
        # No contained candidates, sort by inner_color, then top-left position
        candidate_objects.sort(key=lambda x: (x['inner_color'], x['bbox'][0], x['bbox'][1]))
        target_object = candidate_objects[0]
        is_contained_flag = False

    # 4. Determine Output Colors
    inner_color = target_object['inner_color']
    interior_color = 0 # Always white

    if is_contained_flag:
        primary_color = container_block['color']
    else:
        primary_color = inner_color # Use inner color as primary if not contained

    # 5. Construct Output Grid
    if is_contained_flag:
        # 5x5 pattern
        output_grid = np.full((5, 5), interior_color, dtype=int)
        # Row 1 is already interior_color
        output_grid[1, 0] = inner_color
        output_grid[1, 1:] = primary_color
        output_grid[2:, 0] = primary_color
        # Rows 3, 4, 5 columns 1-4 are already interior_color
    else:
        # 4x4 pattern
        output_grid = np.full((4, 4), primary_color, dtype=int) # Start filled with primary
        output_grid[0, 2] = interior_color
        output_grid[1, 0:3] = interior_color
        # Row 2 is already primary_color
        output_grid[3, 1:3] = interior_color

    return output_grid.tolist()