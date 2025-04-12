import numpy as np
from scipy.ndimage import label, find_objects
from typing import List, Tuple, Dict, Optional

"""
Transforms the input grid by:
1. Identifying three distinct non-background objects: a 'pattern' object, a 'source' object whose bounding box contains the pattern object's bounding box, and a 'target' object (the remaining object).
2. Determining the type of linear pattern (anti-diagonal or main-diagonal-offset) and its characteristic parameter (k_s) based on the pattern pixels' coordinates relative to the source object's top-left bounding box corner.
3. Calculating a corresponding parameter (k_t) for the target object. If the pattern is anti-diagonal, k_t = H_t - 1 (where H_t is target bbox height). If the pattern is a main-diagonal-offset, k_t = k_s.
4. Applying the identified pattern rule (using k_t and the pattern object's color) to modify the pixels within the target object's bounding box in the output grid. Pixels satisfying the rule (dr_t + dc_t == k_t for anti-diag, dr_t - dc_t == k_t for main-diag-offset) are recolored.
"""

# ================= HELPER FUNCTIONS =================

def find_connected_components(grid_np: np.ndarray, background_color: int = 0) -> List[Dict]:
    """
    Finds all distinct connected components (objects) of non-background colors
    using 4-connectivity (orthogonal neighbors).

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
    # Use default connectivity (structure=np.array([[0,1,0],[1,1,1],[0,1,0]]))
    labeled_array, num_features = label(binary_grid)

    if num_features == 0:
        return objects

    slices = find_objects(labeled_array)
    for i, slc in enumerate(slices):
        obj_id = i + 1
        if slc is None: continue # Skip if slice is invalid
             
        coords_raw = np.argwhere(labeled_array == obj_id)
        if coords_raw.size == 0: continue # No pixels for this label

        obj_color = grid_np[coords_raw[0, 0], coords_raw[0, 1]]
        coords = [tuple(coord) for coord in coords_raw]

        min_r = np.min(coords_raw[:, 0])
        min_c = np.min(coords_raw[:, 1])
        max_r = np.max(coords_raw[:, 0])
        max_c = np.max(coords_raw[:, 1])
        bbox = (min_r, min_c, max_r, max_c)

        if obj_color != background_color:
            objects.append({
                'id': obj_id,
                'color': obj_color,
                'coords': coords,
                'bbox': bbox,
                'size': len(coords)
            })
    return objects

def is_contained(bbox_inner: Tuple[int, int, int, int], bbox_outer: Tuple[int, int, int, int]) -> bool:
    """Checks if bbox_inner is contained within or equal to bbox_outer."""
    r1_i, c1_i, r2_i, c2_i = bbox_inner
    r1_o, c1_o, r2_o, c2_o = bbox_outer
    return r1_o <= r1_i and c1_o <= c1_i and r2_i <= r2_o and c2_i <= c2_o

def identify_objects(components: List[Dict]) -> Tuple[Optional[Dict], Optional[Dict], Optional[Dict]]:
    """
    Identifies the pattern, source, and target objects based on containment.
    Assumes exactly one containment relationship exists among the objects.

    Args:
        components: A list of object dictionaries.

    Returns:
        A tuple (pattern_obj, source_obj, target_obj). Returns (None, None, None)
        if the expected structure (e.g., 3 objects, one containment) is not found.
    """
    if len(components) != 3: # Expecting exactly 3 objects based on examples
        return None, None, None

    pattern_obj = None
    source_obj = None
    target_obj = None

    # Iterate through all pairs to find the containment relationship
    found_containment = False
    for i in range(len(components)):
        for j in range(len(components)):
            if i == j: continue # Don't compare object with itself

            potential_pattern = components[i]
            potential_source = components[j]

            # Check if potential_pattern's bbox is contained in potential_source's bbox
            if is_contained(potential_pattern['bbox'], potential_source['bbox']):
                # Ensure they are distinct objects (different IDs)
                if potential_pattern['id'] != potential_source['id']:
                    pattern_obj = potential_pattern
                    source_obj = potential_source
                    found_containment = True
                    break # Found the relationship, assume only one
        if found_containment:
            break

    if not pattern_obj or not source_obj:
        return None, None, None # Containment relationship not found

    # The target object is the one remaining
    for obj in components:
        if obj['id'] != pattern_obj['id'] and obj['id'] != source_obj['id']:
            target_obj = obj
            break

    if not target_obj:
         # Should not happen if len(components) == 3 and containment found
         return None, None, None

    return pattern_obj, source_obj, target_obj

def get_pattern_relative_coords(pattern_obj: Dict, source_obj: Dict) -> List[Tuple[int, int]]:
    """Calculates pattern coords relative to the source bbox top-left corner."""
    rel_coords = []
    src_min_r, src_min_c, _, _ = source_obj['bbox']
    for r, c in pattern_obj['coords']:
        dr = r - src_min_r
        dc = c - src_min_c
        rel_coords.append((dr, dc))
    return rel_coords

def determine_pattern_rule(relative_coords: List[Tuple[int, int]]) -> Tuple[Optional[str], Optional[int]]:
    """Determines pattern type ('anti_diag', 'main_diag_offset') and parameter k_s."""
    if not relative_coords:
        return None, None

    # Sort coords to ensure consistent parameter calculation if needed (optional here)
    # relative_coords.sort()
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

    return None, None # Unknown pattern

def calculate_target_parameter(pattern_type: str, k_s: int, target_obj: Dict) -> Optional[int]:
    """Calculates the corresponding parameter k_t for the target bbox."""
    min_r, _, max_r, _ = target_obj['bbox']
    H_t = max_r - min_r + 1

    if pattern_type == 'main_diag_offset':
        return k_s
    elif pattern_type == 'anti_diag':
        return H_t - 1
    else:
        return None # Unsupported pattern type

def apply_pattern_rule(output_grid_np: np.ndarray, target_obj: Dict, pattern_type: str, k_t: int, pattern_color: int):
    """Applies the pattern rule to modify the output grid within the target bbox."""
    min_r, min_c, max_r, max_c = target_obj['bbox']
    H_t = max_r - min_r + 1
    W_t = max_c - min_c + 1

    for dr_t in range(H_t):
        for dc_t in range(W_t):
            apply_pixel = False
            # Check if the current relative coordinate satisfies the pattern rule
            if pattern_type == 'main_diag_offset' and dr_t - dc_t == k_t:
                apply_pixel = True
            elif pattern_type == 'anti_diag' and dr_t + dc_t == k_t:
                apply_pixel = True
            
            if apply_pixel:
                # Calculate absolute coordinates
                abs_r = min_r + dr_t
                abs_c = min_c + dc_t
                # Paint if within grid bounds
                if 0 <= abs_r < output_grid_np.shape[0] and 0 <= abs_c < output_grid_np.shape[1]:
                    output_grid_np[abs_r, abs_c] = pattern_color

# ================= MAIN TRANSFORM FUNCTION =================

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Main function to transform the input grid based on the identified pattern transfer rule.
    """
    # Convert input to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_array = np.copy(input_array)
    background_color = 0 # Assuming background is 0 (white)

    # --- Step 1: Find all distinct non-background objects ---
    components = find_connected_components(input_array, background_color)
    if not components:
         return input_grid # Return original if no objects found

    # --- Step 2: Identify pattern, source, and target objects ---
    pattern_obj, source_obj, target_obj = identify_objects(components)
    if not pattern_obj or not source_obj or not target_obj:
         # Failed to identify the required roles or structure
         return input_grid # Return original

    # --- Step 3: Extract pattern color ---
    pattern_color = pattern_obj['color']

    # --- Step 4: Calculate pattern coordinates relative to source bbox ---
    relative_coords = get_pattern_relative_coords(pattern_obj, source_obj)
    if not relative_coords:
         # Should not happen if pattern_obj has coordinates
         return input_grid

    # --- Step 5: Determine pattern rule (type and k_s) from relative coordinates ---
    pattern_type, k_s = determine_pattern_rule(relative_coords)
    if not pattern_type or k_s is None:
        # Unknown or unsupported pattern type found
        return input_grid

    # --- Step 6: Calculate the corresponding parameter k_t for the target context ---
    k_t = calculate_target_parameter(pattern_type, k_s, target_obj)
    if k_t is None:
        # Could not determine target parameter for this pattern type
        return input_grid

    # --- Step 7: Apply the pattern rule using k_t within the target bbox on the output grid ---
    apply_pattern_rule(output_array, target_obj, pattern_type, k_t, pattern_color)

    # --- Step 8: Convert back to list of lists for the required output format ---
    return output_array.tolist()