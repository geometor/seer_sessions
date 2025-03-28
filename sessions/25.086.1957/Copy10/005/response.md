```python
# -*- coding: utf-8 -*-
"""
Identifies 'template' structures in the input grid, where a 'container' object encloses a 'content' object based on specific spatial criteria (bounding box inclusion, no border adjacency for content).

Finds other 'target' objects elsewhere in the grid that are identical in shape, size, and color to the 'content' object and are located outside the original 'container'.

For each unique target found, copies the corresponding template structure (container and content) and pastes it onto the grid. The pasting aligns the copied content precisely with the original target object, maintaining the container's relative position around it.

The original template structures and targets remain in the input part of the grid unless overwritten by a paste operation initiated by a different template/target pair. Uses 8-way connectivity for object detection.
"""

import numpy as np
from collections import deque

def find_objects(grid):
    """
    Finds all contiguous objects of non-background colors (value 0) in the grid
    using 8-way connectivity.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'id' (int), 'color' (int), 'coords' (set of (r, c) tuples),
              'bbox' (tuple: min_r, min_c, max_r, max_c), and 'size' (tuple: height, width).
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    obj_id_counter = 0

    for r in range(height):
        for c in range(width):
            # Start BFS if a non-background pixel hasn't been visited
            if grid[r, c] != 0 and not visited[r, c]:
                current_color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                min_r, min_c = r, c
                max_r, max_c = r, c
                visited_in_obj = set([(r,c)]) # Track visited for this specific BFS traversal

                while q:
                    curr_r, curr_c = q.popleft()

                    # Process the current pixel
                    visited[curr_r, curr_c] = True
                    coords.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore 8-way neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc

                            # Check if neighbor is valid, same color, and not yet visited in this BFS
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == current_color and \
                               (nr, nc) not in visited_in_obj:
                                visited_in_obj.add((nr, nc))
                                q.append((nr, nc))

                # Store the found object
                if coords:
                    objects.append({
                        'id': obj_id_counter,
                        'color': current_color,
                        'coords': coords,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'size': (max_r - min_r + 1, max_c - min_c + 1)
                    })
                    obj_id_counter += 1
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
    min_r, min_c, _, _ = obj['bbox']
    mask = set()
    for r, c in obj['coords']:
        mask.add((r - min_r, c - min_c))
    # Size is already calculated in find_objects, reuse it
    return {'mask': mask, 'size': obj['size']}

def check_containment(container_obj, content_obj, grid):
    """
    Checks if container_obj encloses content_obj based on revised criteria:
    - Different colors.
    - Content bounding box is strictly inside container bounding box.
    - No coordinate overlap between container and content.
    - Content object is not adjacent (8-way) to the grid border.

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

    # 1. Check different colors
    if container_obj['color'] == content_obj['color']:
        return False

    # 2. Check bounding box relationship (content strictly inside container bbox)
    if not (content_bbox[0] > container_bbox[0] and
            content_bbox[1] > container_bbox[1] and
            content_bbox[2] < container_bbox[2] and
            content_bbox[3] < container_bbox[3]):
        return False

    # 3. Check no overlap between container and content coords
    if content_obj['coords'].intersection(container_obj['coords']):
        return False

    # 4. Check if content is adjacent to the grid border (8-way)
    for r_cont, c_cont in content_obj['coords']:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r_cont + dr, c_cont + dc
                # If a neighbor coordinate is outside the grid, the content pixel is adjacent to the border
                if not (0 <= nr < height and 0 <= nc < width):
                    return False # Content is adjacent to border

    # If all checks pass, it's considered contained by these rules
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
    # Check size first for quick exit
    if obj1_mask['size'] != obj2_mask['size']:
        return False
    # Check the set of relative coordinates
    return obj1_mask['mask'] == obj2_mask['mask']

def is_bbox_outside(inner_bbox, outer_bbox):
    """
    Checks if inner_bbox is entirely outside outer_bbox.

    Args:
        inner_bbox (tuple): Bbox of the object to check (min_r, min_c, max_r, max_c).
        outer_bbox (tuple): Bbox of the reference area (min_r, min_c, max_r, max_c).

    Returns:
        bool: True if inner_bbox is completely outside outer_bbox, False otherwise.
    """
    inner_min_r, inner_min_c, inner_max_r, inner_max_c = inner_bbox
    outer_min_r, outer_min_c, outer_max_r, outer_max_c = outer_bbox

    # Check for non-overlap: inner ends before outer starts OR inner starts after outer ends
    is_outside_vertical = inner_max_r < outer_min_r or inner_min_r > outer_max_r
    is_outside_horizontal = inner_max_c < outer_min_c or inner_min_c > outer_max_c

    # If it's outside either vertically or horizontally, it cannot overlap.
    # To be strictly outside, it must not overlap at all.
    # An overlap occurs if NOT is_outside_vertical AND NOT is_outside_horizontal.
    # Therefore, it is outside if is_outside_vertical OR is_outside_horizontal.
    return is_outside_vertical or is_outside_horizontal


def transform(input_grid):
    """
    Applies the transformation rule: identifies container/content/target triplets
    based on revised containment rules and copies the container/content structure
    to replace the target.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Find all objects in the input grid
    objects = find_objects(input_grid)
    if not objects:
        return output_grid # Return copy if no objects found

    # 2. Pre-calculate relative masks for all objects for efficient comparison
    object_masks = {obj['id']: get_relative_mask(obj) for obj in objects}

    # 3. Identify containment pairs (template pairs) using the revised check
    containment_pairs = []
    for i in range(len(objects)):
        for j in range(len(objects)):
            if i == j: continue # An object cannot contain itself
            container_candidate = objects[i]
            content_candidate = objects[j]
            # Use the revised containment check function
            if check_containment(container_candidate, content_candidate, input_grid):
                containment_pairs.append({
                    'container_idx': i,
                    'content_idx': j,
                    'container_obj': container_candidate, # Store refs for convenience
                    'content_obj': content_candidate
                })

    # 4. Identify triplets (container, content, target)
    triplets = []
    # Keep track of targets already assigned to ensure uniqueness
    assigned_target_indices = set()

    for pair in containment_pairs:
        content_obj = pair['content_obj']
        content_idx = pair['content_idx']
        content_mask = object_masks[content_idx]
        container_obj = pair['container_obj']
        container_idx = pair['container_idx']
        container_bbox = container_obj['bbox'] # Bbox of the original container

        # Iterate through all objects to find potential targets
        for k in range(len(objects)):
            # Target cannot be the container or content of the current pair
            if k == container_idx or k == content_idx: continue
            # Target must not have already been assigned
            if k in assigned_target_indices: continue

            target_candidate = objects[k]

            # Check if target candidate has the same color and shape/size as the content
            if target_candidate['color'] == content_obj['color']:
                target_mask = object_masks[k]
                if are_identical(content_mask, target_mask):
                    # Check if target is outside the original container's bounding box
                    if is_bbox_outside(target_candidate['bbox'], container_bbox):
                        # If it's a valid, outside, and unassigned target, record the triplet
                        triplets.append({
                            'container_idx': container_idx,
                            'content_idx': content_idx,
                            'target_idx': k
                        })
                        # Mark this target index (k) as assigned
                        assigned_target_indices.add(k)
                        # Important: Break if you only want one target per content type?
                        # The prompt implies finding *all* valid targets and copying for each.
                        # The uniqueness constraint is on the *target* object itself.


    # 5. Perform replacements based on identified triplets
    # Note: The previous step already ensures targets are unique via assigned_target_indices.
    for triplet in triplets:
        # Get the original container, content, and target objects using their indices
        container = objects[triplet['container_idx']]
        content = objects[triplet['content_idx']]
        target = objects[triplet['target_idx']]

        # Calculate the relative offset of the content's top-left corner
        # within the container's bounding box.
        cont_min_r, cont_min_c, _, _ = content['bbox']
        cr_min_r, cr_min_c, _, _ = container['bbox']
        offset_r = cont_min_r - cr_min_r
        offset_c = cont_min_c - cr_min_c

        # Determine the top-left corner where the *new container* should be pasted.
        # This is based on the target's top-left corner minus the content's offset
        # relative to its container. This ensures the copied content aligns with the target.
        target_min_r, target_min_c, _, _ = target['bbox']
        paste_cr_top_left_r = target_min_r - offset_r
        paste_cr_top_left_c = target_min_c - offset_c

        # --- Perform the pasting onto the output grid ---

        # a) Paste the container pixels
        container_color = container['color']
        cr_mask = object_masks[triplet['container_idx']]['mask']
        for rel_r, rel_c in cr_mask:
            out_r = paste_cr_top_left_r + rel_r
            out_c = paste_cr_top_left_c + rel_c
            # Ensure pasted pixel is within grid bounds before writing
            if 0 <= out_r < height and 0 <= out_c < width:
                output_grid[out_r, out_c] = container_color

        # b) Paste the content pixels (overwriting container pixels if necessary)
        # Paste content aligned with the original target position.
        content_color = content['color']
        cont_mask = object_masks[triplet['content_idx']]['mask']
        for rel_r, rel_c in cont_mask:
            out_r = target_min_r + rel_r
            out_c = target_min_c + rel_c
            # Ensure pasted pixel is within grid bounds before writing
            if 0 <= out_r < height and 0 <= out_c < width:
                output_grid[out_r, out_c] = content_color

    # Return the modified grid
    return output_grid
```