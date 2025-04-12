import numpy as np
from scipy.ndimage import label, find_objects

"""
Transforms the input grid by:
1. Identifying three distinct non-background objects: a 'pattern' object, a 'source' object that contains it, and a 'target' object. Containment is defined by the pattern object's bounding box being strictly within the source object's bounding box.
2. Determining the type of pattern (e.g., anti-diagonal, main diagonal offset) and its characteristic parameter (k_s) based on the pattern pixels' coordinates relative to the source object's top-left bounding box corner.
3. Calculating a corresponding parameter (k_t) for the target object, based on the pattern type and the target object's bounding box dimensions (specifically, height H_t for anti-diagonal, or k_s itself for main diagonal offset).
4. Applying the pattern rule (using k_t and the pattern object's color) to modify the pixels within the target object's bounding box in the output grid.
"""

def find_connected_components(grid_np: np.ndarray, background_color: int = 0) -> list[dict]:
    """
    Finds all distinct connected components (objects) of non-background colors.

    Args:
        grid_np: A numpy array representing the input grid.
        background_color: The integer value representing the background color.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains 'id', 'color', 'coords' (list of tuples), and 'bbox'
        (tuple: min_r, min_c, max_r, max_c). Returns empty list if no
        non-background objects are found.
    """
    objects = []
    binary_grid = grid_np != background_color
    # Use default connectivity (orthogonal neighbors)
    labeled_array, num_features = label(binary_grid)

    if num_features == 0:
        return objects

    slices = find_objects(labeled_array)
    for i, slc in enumerate(slices):
        obj_id = i + 1
        # Check if the slice is valid and corresponds to a feature
        if slc is None:
             continue # Should not happen with find_objects output normally
             
        coords_raw = np.argwhere(labeled_array == obj_id)
        if coords_raw.size == 0: continue # No pixels for this label

        # Use the color of the first pixel found for this component
        obj_color = grid_np[coords_raw[0, 0], coords_raw[0, 1]]
        # Ensure coords are tuples
        coords = [tuple(coord) for coord in coords_raw]

        # Calculate bounding box directly from coordinates
        min_r = np.min(coords_raw[:, 0])
        min_c = np.min(coords_raw[:, 1])
        max_r = np.max(coords_raw[:, 0])
        max_c = np.max(coords_raw[:, 1])
        bbox = (min_r, min_c, max_r, max_c)

        # Store object info only if it's not background
        if obj_color != background_color:
            objects.append({
                'id': obj_id,
                'color': obj_color,
                'coords': coords,
                'bbox': bbox,
                'size': len(coords)
            })
    return objects

def is_contained(bbox_inner: tuple, bbox_outer: tuple) -> bool:
    """Checks if bbox_inner is strictly contained within bbox_outer."""
    r1_i, c1_i, r2_i, c2_i = bbox_inner
    r1_o, c1_o, r2_o, c2_o = bbox_outer
    # Check strict containment (inner must be smaller or equal and inside)
    contained = r1_o <= r1_i and c1_o <= c1_i and r2_i <= r2_o and c2_i <= c2_o
    # Check if inner is strictly smaller in at least one dimension OR if coords are exactly the same
    # This handles cases where the "pattern" might touch the edge of the frame bbox
    smaller = (r2_i - r1_i < r2_o - r1_o) or (c2_i - c1_i < c2_o - c1_o) or (bbox_inner == bbox_outer)

    # Refined check: strictly inside OR identical bounds (for pattern touching frame)
    # AND must be truly inside (not equal)
    # Let's simplify: Inner box corners must be >= outer box corners,
    # and inner box must not be identical to outer box IF they have different object IDs.
    strictly_inside = r1_o <= r1_i and c1_o <= c1_i and r2_i <= r2_o and c2_i <= c2_o
    # We require the *object* bbox to be contained, not necessarily strictly smaller bbox
    # if they represent different objects conceptually.

    return strictly_inside


def identify_objects(components: list[dict]) -> tuple[dict | None, dict | None, dict | None]:
    """
    Identifies the pattern, source, and target objects based on containment.

    Args:
        components: A list of object dictionaries from find_connected_components.

    Returns:
        A tuple (pattern_obj, source_obj, target_obj). Returns (None, None, None)
        if identification fails (e.g., wrong number of objects, no containment).
    """
    if len(components) < 2: # Need at least pattern and source, ideally 3
        return None, None, None

    pattern_obj = None
    source_obj = None
    target_obj = None

    # Iterate through all pairs to find containment relationship
    for i in range(len(components)):
        for j in range(len(components)):
            if i == j: continue # Don't compare object with itself

            potential_pattern = components[i]
            potential_source = components[j]

            if is_contained(potential_pattern['bbox'], potential_source['bbox']):
                 # Check if potential pattern is strictly smaller than potential source
                 # This helps avoid ambiguity if bounding boxes accidentally match
                 ppb = potential_pattern['bbox']
                 psb = potential_source['bbox']
                 p_h, p_w = ppb[2]-ppb[0]+1, ppb[3]-ppb[1]+1
                 s_h, s_w = psb[2]-psb[0]+1, psb[3]-psb[1]+1

                 # Pattern must be smaller or equal in size and strictly contained
                 # or have the same bbox but different ID (pattern on edge)
                 if (p_h <= s_h and p_w <= s_w) and \
                    (potential_pattern['id'] != potential_source['id']): # Ensure different objects
                        # Found a candidate pair
                        pattern_obj = potential_pattern
                        source_obj = potential_source
                        break # Assume only one such relationship exists
        if pattern_obj:
            break

    if not pattern_obj or not source_obj:
        return None, None, None # Containment relationship not found

    # The target object is the remaining one
    for obj in components:
        if obj['id'] != pattern_obj['id'] and obj['id'] != source_obj['id']:
            target_obj = obj
            break # Assume only one target

    if not target_obj:
         # Handle cases with only 2 objects (pattern+source, no separate target?)
         # This shouldn't happen based on examples, return failure
         return None, None, None

    return pattern_obj, source_obj, target_obj

def get_pattern_relative_coords(pattern_obj: dict, source_obj: dict) -> list[tuple[int, int]]:
    """Calculates pattern coords relative to the source bbox top-left."""
    rel_coords = []
    src_min_r, src_min_c, _, _ = source_obj['bbox']
    for r, c in pattern_obj['coords']:
        dr = r - src_min_r
        dc = c - src_min_c
        rel_coords.append((dr, dc))
    return rel_coords

def determine_pattern_rule(relative_coords: list[tuple[int, int]]) -> tuple[str | None, int | None]:
    """Determines pattern type ('anti_diag', 'main_diag_offset') and parameter k_s."""
    if not relative_coords:
        return None, None

    # Sort for consistent checking, although mathematically not always needed
    relative_coords.sort()
    dr0, dc0 = relative_coords[0]

    # Check for anti-diagonal: dr + dc = k_s
    k_s_anti = dr0 + dc0
    is_anti_diag = all(dr + dc == k_s_anti for dr, dc in relative_coords)
    if is_anti_diag:
        return 'anti_diag', k_s_anti

    # Check for main diagonal offset: dr - dc = k_s
    k_s_main = dr0 - dc0
    is_main_diag = all(dr - dc == k_s_main for dr, dc in relative_coords)
    if is_main_diag:
        return 'main_diag_offset', k_s_main

    # Add other patterns here if needed (e.g., horizontal, vertical)
    # k_s_horiz = dr0
    # is_horiz = all(dr == k_s_horiz for dr, dc in relative_coords)
    # if is_horiz: return 'horiz', k_s_horiz
    # k_s_vert = dc0
    # is_vert = all(dc == k_s_vert for dr, dc in relative_coords)
    # if is_vert: return 'vert', k_s_vert

    return None, None # Unknown pattern

def calculate_target_parameter(pattern_type: str, k_s: int, target_obj: dict) -> int | None:
    """Calculates the corresponding parameter k_t for the target bbox."""
    min_r, min_c, max_r, max_c = target_obj['bbox']
    H_t = max_r - min_r + 1
    # W_t = max_c - min_c + 1 # Width might be needed for other patterns

    if pattern_type == 'main_diag_offset':
        return k_s # Parameter seems constant for this type
    elif pattern_type == 'anti_diag':
        # Rule derived from examples: k_t depends on target height
        return H_t - 1
    # Add rules for other pattern types here
    # elif pattern_type == 'horiz': return k_s
    # elif pattern_type == 'vert': return k_s
    else:
        return None # Unsupported pattern type

def apply_pattern_rule(output_grid_np: np.ndarray, target_obj: dict, pattern_type: str, k_t: int, pattern_color: int):
    """Applies the pattern rule to modify the output grid within the target bbox."""
    min_r, min_c, max_r, max_c = target_obj['bbox']
    H_t = max_r - min_r + 1
    W_t = max_c - min_c + 1

    for dr_t in range(H_t):
        for dc_t in range(W_t):
            apply = False
            if pattern_type == 'main_diag_offset' and dr_t - dc_t == k_t:
                apply = True
            elif pattern_type == 'anti_diag' and dr_t + dc_t == k_t:
                apply = True
            # Add conditions for other pattern types here
            # elif pattern_type == 'horiz' and dr_t == k_t: apply = True
            # elif pattern_type == 'vert' and dc_t == k_t: apply = True

            if apply:
                # Calculate absolute coordinates
                abs_r = min_r + dr_t
                abs_c = min_c + dc_t
                # Check if coordinates are within grid bounds before painting
                if 0 <= abs_r < output_grid_np.shape[0] and 0 <= abs_c < output_grid_np.shape[1]:
                    output_grid_np[abs_r, abs_c] = pattern_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    background_color = 0 # Assuming background is 0 (white)

    # 1. Find all distinct non-background objects
    components = find_connected_components(input_array, background_color)
    if not components:
         return input_grid # Return original if no objects found

    # 2. Identify pattern, source, and target objects based on containment
    pattern_obj, source_obj, target_obj = identify_objects(components)
    if not pattern_obj or not source_obj or not target_obj:
         # Failed to identify the three required roles
         return input_grid # Return original

    # 3. Extract pattern color
    pattern_color = pattern_obj['color']

    # 4. Calculate pattern coordinates relative to source bbox
    relative_coords = get_pattern_relative_coords(pattern_obj, source_obj)
    if not relative_coords:
         # Should not happen if pattern_obj has coordinates, but check anyway
         return input_grid

    # 5. Determine pattern rule (type and k_s) from source relative coordinates
    pattern_type, k_s = determine_pattern_rule(relative_coords)
    if not pattern_type:
        # Unknown or unsupported pattern type
        return input_grid

    # 6. Calculate the corresponding parameter k_t for the target context
    k_t = calculate_target_parameter(pattern_type, k_s, target_obj)
    if k_t is None:
        # Could not determine target parameter for this pattern type
        return input_grid

    # 7. Apply the pattern rule using k_t within the target bbox on the output grid
    apply_pattern_rule(output_array, target_obj, pattern_type, k_t, pattern_color)

    # Convert back to list of lists for the required output format
    return output_array.tolist()