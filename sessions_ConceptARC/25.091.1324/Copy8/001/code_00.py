"""
Identify objects by color. Find the color with exactly two objects (anchors) and the color with exactly one object (mobile). Determine the spatial offset between the first anchor (top-leftmost) and the mobile object. Apply this same offset to the second anchor to find the target location. Copy the mobile object to the target location in the output grid, leaving the rest of the input grid unchanged.
"""

import numpy as np
from collections import defaultdict

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid.
    
    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'color' (int): The color of the object.
              'pixels' (set): A set of (row, col) tuples for the object's pixels.
              'bbox' (tuple): The bounding box (min_row, min_col, max_row, max_col).
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

                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def transform(input_grid):
    """
    Applies the transformation rule: Copy a single object based on its relative
    position to a pair of anchor objects.

    Args:
        input_grid (np.ndarray): The input 2D array representing the grid.

    Returns:
        np.ndarray: The transformed 2D array.
    """
    
    # 1. Find all objects in the input grid
    objects = find_objects(input_grid)

    # 2. Categorize objects by color and count them
    objects_by_color = defaultdict(list)
    for obj in objects:
        objects_by_color[obj['color']].append(obj)

    anchor_color = None
    mobile_color = None
    anchor_objects = []
    mobile_object = None

    # 3. Find Anchor Pair and Mobile Object
    for color, obj_list in objects_by_color.items():
        if len(obj_list) == 2:
            anchor_color = color
            anchor_objects = obj_list
        elif len(obj_list) == 1:
            mobile_color = color
            mobile_object = obj_list[0]

    # Check if we found the required objects
    if anchor_color is None or mobile_color is None:
        # If the pattern doesn't match (e.g., different counts), return the input unchanged
        # or handle as an error, depending on desired behavior. 
        # For now, return a copy of the input.
        return np.copy(input_grid) 

    # 4. Order Anchors (Anchor1 is top-leftmost)
    anchor1 = min(anchor_objects, key=lambda obj: (obj['bbox'][0], obj['bbox'][1]))
    anchor2 = max(anchor_objects, key=lambda obj: (obj['bbox'][0], obj['bbox'][1]))

    # 5. Calculate Offset
    mob_r0, mob_c0, _, _ = mobile_object['bbox']
    anc1_r0, anc1_c0, _, _ = anchor1['bbox']
    delta_row = mob_r0 - anc1_r0
    delta_col = mob_c0 - anc1_c0

    # 6. Determine Copy Position
    anc2_r0, anc2_c0, _, _ = anchor2['bbox']
    copy_target_r0 = anc2_r0 + delta_row
    copy_target_c0 = anc2_c0 + delta_col
    
    # 7. Generate Output: Start with a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 8. Copy the mobile object's pixels to the target location
    mobile_color = mobile_object['color']
    for r_pix, c_pix in mobile_object['pixels']:
        # Calculate pixel position relative to the mobile object's top-left
        relative_r = r_pix - mob_r0
        relative_c = c_pix - mob_c0
        
        # Calculate the target pixel position in the output grid
        target_r = copy_target_r0 + relative_r
        target_c = copy_target_c0 + relative_c

        # Ensure the target position is within bounds before drawing
        if 0 <= target_r < rows and 0 <= target_c < cols:
            output_grid[target_r, target_c] = mobile_color

    return output_grid