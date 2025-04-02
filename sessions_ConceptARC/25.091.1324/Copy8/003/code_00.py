"""
Identifies a pair of identical contiguous anchor objects and a potentially non-contiguous mobile object (defined by all pixels of a third distinct color). Calculates the positional offset between the top-left corner of the mobile object's overall bounding box and the top-left corner of the first anchor object's bounding box. Applies this offset to the top-left corner of the second anchor object's bounding box to determine a target origin. Copies all pixels of the mobile object, maintaining their positions relative to the mobile object's bounding box top-left, placing them relative to the calculated target origin in the output grid. The original grid elements (background, anchors, original mobile object) remain in place.
"""

import numpy as np
from collections import defaultdict

def find_contiguous_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid using 4-connectivity.
    
    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing a contiguous object with keys:
              'color' (int): The color of the object.
              'pixels' (set): A set of (row, col) tuples for the object's pixels.
              'bbox' (tuple): The bounding box (min_row, min_col, max_row, max_col).
              'top_left' (tuple): The top-left corner (min_row, min_col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0: # 0 is background
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.pop(0)
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
                
                if obj_pixels: # Only add if pixels were found (should always be true here)
                    objects.append({
                        'color': color,
                        'pixels': obj_pixels,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'top_left': (min_r, min_c) 
                    })
    return objects

def get_color_pixel_groups(grid):
    """
    Groups all non-background pixels by color, finds their overall bounding box, 
    and top-left corner for each color group.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        dict: A dictionary where keys are colors and values are dictionaries
              containing 'color', 'pixels' (set of all pixels of that color),
              'bbox', and 'top_left' of the overall bounding box for that color.
              Returns an empty dictionary if no non-background pixels are found.
    """
    pixels_by_color = defaultdict(set)
    rows, cols = grid.shape
    has_pixels = False
    for r in range(rows):
        for c in range(cols):
            color = grid[r,c]
            if color != 0:
                pixels_by_color[color].add((r,c))
                has_pixels = True

    if not has_pixels:
        return {}

    groups = {}
    for color, pixels in pixels_by_color.items():
        if not pixels: continue # Should not happen if color is in keys, but safety check
        min_r = min(r for r, c in pixels)
        min_c = min(c for r, c in pixels)
        max_r = max(r for r, c in pixels)
        max_c = max(c for r, c in pixels)
        groups[color] = {
            'color': color,
            'pixels': pixels,
            'bbox': (min_r, min_c, max_r, max_c),
            'top_left': (min_r, min_c)
        }
    return groups


def transform(input_grid):
    """
    Applies the transformation rule based on anchor and mobile objects.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # 1. Identify Contiguous Objects
    contiguous_objects = find_contiguous_objects(input_grid)

    # 2. Find Anchor Color and Objects
    objects_by_color = defaultdict(list)
    for obj in contiguous_objects:
        objects_by_color[obj['color']].append(obj)

    anchor_color = None
    anchor_objects = []
    for color, obj_list in objects_by_color.items():
        if len(obj_list) == 2:
            anchor_color = color
            # Sort anchors by top-left: Anchor1 is top-leftmost
            anchor_objects = sorted(obj_list, key=lambda o: o['top_left']) 
            break
    
    if anchor_color is None:
        return output_grid # No anchor pair found

    anchor1 = anchor_objects[0]
    anchor2 = anchor_objects[1]
    anchor1_top_left = anchor1['top_left']
    anchor2_top_left = anchor2['top_left']

    # 3. Find Mobile Color and Pixels
    all_color_groups = get_color_pixel_groups(input_grid)
    mobile_color = None
    mobile_group = None
    
    # Iterate through all colors found in the grid
    for color, group_data in all_color_groups.items():
        if color != anchor_color:
             # Check if this color corresponds to a group that wasn't one of the contiguous anchors found earlier
             # This handles cases where the mobile object might *also* be contiguous
             is_anchor = False
             for anchor_obj in anchor_objects:
                 if anchor_obj['color'] == color and anchor_obj['pixels'] == group_data['pixels']:
                     is_anchor = True
                     break
             if not is_anchor:
                 mobile_color = color
                 mobile_group = group_data
                 break # Assume only one mobile color

    if mobile_color is None or mobile_group is None:
        return output_grid # No distinct mobile color/group found

    mobile_pixels = mobile_group['pixels']
    mobile_bbox_top_left = mobile_group['top_left']

    # 4. Calculate Offset
    delta_row = mobile_bbox_top_left[0] - anchor1_top_left[0]
    delta_col = mobile_bbox_top_left[1] - anchor1_top_left[1]

    # 5. Determine Copy Target Origin
    copy_target_origin_r = anchor2_top_left[0] + delta_row
    copy_target_origin_c = anchor2_top_left[1] + delta_col

    # 6. Copy Mobile Pixels to Target Location
    mob_origin_r, mob_origin_c = mobile_bbox_top_left
    
    for r_mob, c_mob in mobile_pixels:
        # Calculate pixel position relative to the mobile object's bounding box top-left
        relative_r = r_mob - mob_origin_r
        relative_c = c_mob - mob_origin_c
        
        # Calculate the target pixel position in the output grid
        target_r = copy_target_origin_r + relative_r
        target_c = copy_target_origin_c + relative_c

        # Ensure the target position is within bounds before drawing
        if 0 <= target_r < rows and 0 <= target_c < cols:
            output_grid[target_r, target_c] = mobile_color
            
    return output_grid