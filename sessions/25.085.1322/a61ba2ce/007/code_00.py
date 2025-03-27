import numpy as np
from collections import Counter

"""
Identifies exactly four 3-pixel L-shaped objects in the input grid.
Calculates the bounding box (bbox) center for each object.
Determines the median row and median column from these four centers to establish relative quadrant boundaries.
Assigns each object to a relative input quadrant (InTL, InTR, InBL, InBR) based on its bbox center relative to the median coordinates.
Calculates the vertical midline indices of the input grid.
Checks if the bbox of the object assigned to InTL OR the object assigned to InTR crosses the vertical midline. Crossing means the bbox spans columns on both sides of the midline boundary.
Constructs a 4x4 output grid by placing the 2x2 patterns extracted from each object's bbox:
  - Pattern from InBL object goes to output BL (bottom-left).
  - Pattern from InBR object goes to output BR (bottom-right).
  - If the crossing condition is True, the pattern from InTR goes to output TL (top-left), and the pattern from InTL goes to output TR (top-right).
  - If the crossing condition is False, the pattern from InTL goes to output TL, and the pattern from InTR goes to output TR.
"""

def find_l_objects(grid):
    """
    Finds all contiguous 3-pixel L-shaped objects of non-background colors.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing an L-shaped object with keys:
              'color': The color of the object's pixels.
              'pixels': A list of (row, col) coordinates of the object's pixels.
              'bbox': A tuple (min_r, min_c, max_r, max_c) of the bounding box (should be 2x2).
              'pattern': A 2x2 numpy array of the pattern within the bbox.
              'bbox_center': A tuple (center_r, center_c) of the bounding box center coordinates.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                q = [(r, c)]
                visited[r, c] = True
                component_pixels = []
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Use BFS to find all connected pixels of the same color
                while q:
                    row, col = q.pop(0)
                    component_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Check if the found component is an L-shape (3 pixels and 2x2 bbox)
                if len(component_pixels) == 3 and (max_r - min_r == 1) and (max_c - min_c == 1):
                    bbox = (min_r, min_c, max_r, max_c)
                    # Extract the 2x2 pattern directly using the bounding box
                    pattern = grid[min_r:min_r+2, min_c:min_c+2].copy() # Use copy

                    # Calculate bbox center
                    center_r = (min_r + max_r) / 2.0
                    center_c = (min_c + max_c) / 2.0
                    bbox_center = (center_r, center_c)

                    # Defensive check for pattern shape
                    if pattern.shape == (2, 2):
                        objects.append({
                            'color': color,
                            'pixels': component_pixels,
                            'bbox': bbox,
                            'pattern': pattern, # Keep as numpy array
                            'bbox_center': bbox_center
                        })
                    # else: # Should not happen for valid L-shapes, but could log if needed
                    #    print(f"Warning: Pattern shape incorrect {pattern.shape} for bbox {bbox}. Skipping object.")

    return objects


def transform(input_grid):
    """
    Transforms the input grid according to the L-shape quadrant mapping rule.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    default_output_grid = np.zeros((4, 4), dtype=int) # Grid to return on error

    # 1. Identify Objects: Find exactly four L-shaped objects
    objects = find_l_objects(input_grid_np)
    if len(objects) != 4:
        # print(f"Warning: Expected 4 L-shaped objects, found {len(objects)}. Returning default grid.")
        return default_output_grid.tolist()

    # 2. Determine Relative Center: Calculate median center coordinates
    centers_r = [obj['bbox_center'][0] for obj in objects]
    centers_c = [obj['bbox_center'][1] for obj in objects]
    median_r = np.median(centers_r)
    median_c = np.median(centers_c)

    # 3. Assign Input Quadrants: Based on median coordinates
    objects_by_quadrant = {'InTL': None, 'InTR': None, 'InBL': None, 'InBR': None}
    quadrant_assignment_count = 0
    assigned_quadrants_list = [] # To check for duplicates

    for obj in objects:
        center_r, center_c = obj['bbox_center']
        quadrant = ""
        if center_r < median_r: quadrant += "InT"
        else: quadrant += "InB" # Objects exactly on median line go to Bottom/Right

        if center_c < median_c: quadrant += "L"
        else: quadrant += "R"

        if quadrant in objects_by_quadrant and objects_by_quadrant[quadrant] is None:
            objects_by_quadrant[quadrant] = obj
            quadrant_assignment_count += 1
            assigned_quadrants_list.append(quadrant)
        else:
            # This case should be less likely with median but handle defensively
            # print(f"Warning: Quadrant assignment issue for object at center {obj['bbox_center']} -> quadrant {quadrant}. Existing: {objects_by_quadrant.get(quadrant)}")
            return default_output_grid.tolist()

    # Check if all quadrants were assigned exactly one object
    if quadrant_assignment_count != 4 or len(set(assigned_quadrants_list)) != 4:
         # print(f"Warning: Not all quadrants assigned uniquely. Count: {quadrant_assignment_count}, Unique: {len(set(assigned_quadrants_list))}. Returning default grid.")
         return default_output_grid.tolist()

    # 4. Check Crossing Condition: Check if InTL or InTR crosses the vertical midline
    vertical_center_col_idx_left = (width - 1) // 2
    vertical_center_col_idx_right = vertical_center_col_idx_left + 1
    swap_top_quadrants = False

    obj_intl = objects_by_quadrant['InTL']
    obj_intr = objects_by_quadrant['InTR']

    # Check InTL crossing
    bbox_intl = obj_intl['bbox']
    if bbox_intl[1] <= vertical_center_col_idx_left and bbox_intl[3] >= vertical_center_col_idx_right:
        swap_top_quadrants = True

    # Check InTR crossing (only if InTL didn't cross)
    if not swap_top_quadrants:
        bbox_intr = obj_intr['bbox']
        if bbox_intr[1] <= vertical_center_col_idx_left and bbox_intr[3] >= vertical_center_col_idx_right:
            swap_top_quadrants = True

    # 5. Assemble Output Grid: Create 4x4 grid and place patterns
    output_grid = np.zeros((4, 4), dtype=int)

    # Place bottom patterns (fixed relative mapping)
    output_grid[2:4, 0:2] = objects_by_quadrant['InBL']['pattern']
    output_grid[2:4, 2:4] = objects_by_quadrant['InBR']['pattern']

    # Place top patterns based on swap condition
    if swap_top_quadrants:
        # Swap: InTR pattern -> OutTL, InTL pattern -> OutTR
        output_grid[0:2, 0:2] = obj_intr['pattern']
        output_grid[0:2, 2:4] = obj_intl['pattern']
    else:
        # No swap: InTL pattern -> OutTL, InTR pattern -> OutTR
        output_grid[0:2, 0:2] = obj_intl['pattern']
        output_grid[0:2, 2:4] = obj_intr['pattern']

    # 6. Return the assembled grid as a list of lists
    return output_grid.tolist()