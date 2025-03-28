"""
Identifies pairs of objects where one object (container) encloses another (content).
Finds other objects (targets) in the grid that are identical in shape and color to the content object but located outside the container.
For each target found, copies the corresponding container and content structure and pastes it onto the grid such that the copied content perfectly replaces the target object, maintaining the relative position of the container around the content.
The original container/content pairs remain untouched.
"""

import numpy as np
from collections import deque

def find_objects(grid):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int), 'coords' (set of (r, c) tuples),
              and 'bbox' (tuple: min_r, min_c, max_r, max_c).
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                current_color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    curr_r, curr_c = q.popleft()

                    if not (0 <= curr_r < height and 0 <= curr_c < width) or \
                       visited[curr_r, curr_c] or \
                       grid[curr_r, curr_c] != current_color:
                        continue

                    visited[curr_r, curr_c] = True
                    coords.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Add neighbors (4-way sufficient for connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        q.append((nr, nc))

                if coords:
                    objects.append({
                        'color': current_color,
                        'coords': coords,
                        'bbox': (min_r, min_c, max_r, max_c)
                    })
    return objects

def get_relative_mask(obj):
    """
    Calculates the relative coordinates (mask) of an object's pixels
    with respect to its bounding box top-left corner.

    Args:
        obj (dict): An object dictionary from find_objects.

    Returns:
        dict: Contains 'mask' (set of (rel_r, rel_c) tuples) and
              'size' (tuple: height, width).
    """
    min_r, min_c, max_r, max_c = obj['bbox']
    mask = set()
    for r, c in obj['coords']:
        mask.add((r - min_r, c - min_c))
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return {'mask': mask, 'size': (height, width)}

def check_containment(container_obj, content_obj, grid):
    """
    Checks if container_obj fully encloses content_obj using flood fill.

    Args:
        container_obj (dict): Potential container object.
        content_obj (dict): Potential content object.
        grid (np.array): The input grid.

    Returns:
        bool: True if containment is confirmed, False otherwise.
    """
    height, width = grid.shape
    content_bbox = content_obj['bbox']
    container_bbox = container_obj['bbox']

    # Basic checks
    if not (content_bbox[0] >= container_bbox[0] and
            content_bbox[1] >= container_bbox[1] and
            content_bbox[2] <= container_bbox[2] and
            content_bbox[3] <= container_bbox[3]):
        return False # Bbox not inside
    if container_obj['color'] == content_obj['color']:
        return False # Must be different colors
    if content_obj['coords'].intersection(container_obj['coords']):
         return False # Cannot overlap


    # Flood fill background from border
    reachable_background = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add border background cells
    for r in range(height):
        for c in [0, width - 1]:
             if grid[r, c] == 0 and not reachable_background[r, c]:
                q.append((r, c))
                reachable_background[r, c] = True
    for c in range(width): # Use range(width) instead of range(1, width-1) to catch all border pixels
         for r in [0, height - 1]:
             if grid[r, c] == 0 and not reachable_background[r, c]:
                 q.append((r, c))
                 reachable_background[r, c] = True


    # BFS for reachable background
    while q:
        r, c = q.popleft()
        # Check 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc

                if 0 <= nr < height and 0 <= nc < width and \
                   not reachable_background[nr, nc] and \
                   grid[nr, nc] == 0: # Only spread through background
                    reachable_background[nr, nc] = True
                    q.append((nr, nc))

    # Check if any content pixel is adjacent to reachable background or border
    for r, c in content_obj['coords']:
        # Check 8 neighbors
         for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc

                if not (0 <= nr < height and 0 <= nc < width):
                     return False # Content adjacent to grid border
                if reachable_background[nr, nc]:
                     return False # Content adjacent to background reachable from border

    # If no such adjacency found, it's contained
    return True


def are_identical(obj1_mask, obj2_mask):
    """
    Checks if two objects are identical based on their relative masks.

    Args:
        obj1_mask (dict): Relative mask dict for object 1.
        obj2_mask (dict): Relative mask dict for object 2.

    Returns:
        bool: True if identical shape and size, False otherwise.
    """
    return obj1_mask['size'] == obj2_mask['size'] and \
           obj1_mask['mask'] == obj2_mask['mask']

def transform(input_grid):
    """
    Applies the transformation rule: identifies container/content/target triplets
    and copies the container/content structure to replace the target.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    objects = find_objects(input_grid)

    if not objects:
        return output_grid

    object_masks = {i: get_relative_mask(obj) for i, obj in enumerate(objects)}

    # 1. Identify containment pairs (container, content)
    containment_pairs = []
    for i in range(len(objects)):
        for j in range(len(objects)):
            if i == j: continue
            container_candidate = objects[i]
            content_candidate = objects[j]
            if check_containment(container_candidate, content_candidate, input_grid):
                containment_pairs.append({'container_idx': i, 'content_idx': j})

    # 2. Identify triplets (container, content, target)
    triplets = []
    found_targets_for_content = {} # key: content_idx, value: set of target_idx

    for pair in containment_pairs:
        container_idx = pair['container_idx']
        content_idx = pair['content_idx']
        content_obj = objects[content_idx]
        content_mask = object_masks[content_idx]
        container_bbox = objects[container_idx]['bbox']

        if content_idx not in found_targets_for_content:
             found_targets_for_content[content_idx] = set()

        for k in range(len(objects)):
            if k == container_idx or k == content_idx: continue

            target_candidate = objects[k]
            target_bbox = target_candidate['bbox']

            # Check if target is identical to content
            if target_candidate['color'] == content_obj['color']:
                target_mask = object_masks[k]
                if are_identical(content_mask, target_mask):
                    # Check if target is outside the container (non-overlapping bounding box)
                    overlap = not (target_bbox[2] < container_bbox[0] or
                                   target_bbox[0] > container_bbox[2] or
                                   target_bbox[3] < container_bbox[1] or
                                   target_bbox[1] > container_bbox[3])

                    if not overlap:
                        # Ensure this target hasn't been assigned to this content type via another container
                        is_new_target = True
                        for c_idx, assigned_targets in found_targets_for_content.items():
                            if k in assigned_targets:
                                is_new_target = False
                                break
                        
                        if is_new_target:
                            triplets.append({
                                'container_idx': container_idx,
                                'content_idx': content_idx,
                                'target_idx': k
                            })
                            found_targets_for_content[content_idx].add(k)


    # 3. Perform replacements
    processed_targets = set()
    for triplet in triplets:
        target_idx = triplet['target_idx']
        if target_idx in processed_targets: continue # Ensure each target is replaced only once
        processed_targets.add(target_idx)

        container = objects[triplet['container_idx']]
        content = objects[triplet['content_idx']]
        target = objects[triplet['target_idx']]

        # Calculate offset of content within container
        cont_min_r, cont_min_c, _, _ = content['bbox']
        cr_min_r, cr_min_c, _, _ = container['bbox']
        offset_r = cont_min_r - cr_min_r
        offset_c = cont_min_c - cr_min_c

        # Calculate target paste location for the *container's* top-left corner
        target_min_r, target_min_c, _, _ = target['bbox']
        paste_cr_top_left_r = target_min_r - offset_r
        paste_cr_top_left_c = target_min_c - offset_c

        # Clear the area where the new structure will be pasted?
        # No, the examples show overwriting. Example 1 overwrites background.

        # Paste container pixels relative to the new container top-left
        container_color = container['color']
        for r, c in container['coords']:
            rel_r = r - cr_min_r
            rel_c = c - cr_min_c
            out_r = paste_cr_top_left_r + rel_r
            out_c = paste_cr_top_left_c + rel_c
            if 0 <= out_r < height and 0 <= out_c < width:
                output_grid[out_r, out_c] = container_color

        # Paste content pixels relative to the *target's* top-left (to ensure alignment)
        content_color = content['color']
        for r, c in content['coords']:
            rel_r = r - cont_min_r
            rel_c = c - cont_min_c
            out_r = target_min_r + rel_r # Align content with original target position
            out_c = target_min_c + rel_c
            if 0 <= out_r < height and 0 <= out_c < width:
                output_grid[out_r, out_c] = content_color # Overwrites container pixels if needed


    return output_grid