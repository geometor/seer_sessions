import numpy as np
from scipy import ndimage
from collections import Counter

"""
Transformation Rule:
1.  Identify potential background digits P = {0, 1, 2, 3}.
2.  Identify "object" pixels: cells with values NOT in P.
3.  Find connected components (8-way) of object pixels.
4.  Identify the primary frame component:
    a. Find the component with the largest number of pixels. Store its coordinates (`frame_coords`).
    b. Determine the `frame_digit`: If the component is uniform, use that digit. If not, use the most frequent digit within the component's coordinates.
    c. **Fallback:** If no object components were found in step 3 (e.g., frame is made of digit 3), find connected components of *all non-zero* pixels. Iterate through these components from largest to smallest by pixel count. The *first* component found that is *uniform* (all pixels have the same digit) is considered the frame. Update `frame_coords` and `frame_digit`.
    d. If no frame component is found by either method, return an empty grid.
5.  Calculate the bounding box (`min_r`, `min_c`, `max_r`, `max_c`) of the final `frame_coords`.
6.  Define the actual background digits B = {0} union {d in {1, 2, 3} if d is not the `frame_digit`}.
7.  Create the output grid with dimensions determined by the frame's bounding box.
8.  Populate the output grid: For each cell within the bounding box in the input grid:
    a. Get the input value `v` and coordinates `coord`.
    b. If `v` is in B AND `coord` is NOT in `frame_coords`, the output cell is 0.
    c. Otherwise, the output cell is `v`.
9.  Return the output grid as a list of lists.
"""

def find_bounding_box(coords):
    """Calculates the bounding box for a set of (row, col) coordinates."""
    if not coords:
        return None
    min_row = min(r for r, c in coords)
    max_row = max(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

def get_component_info(labeled_array, num_features, input_grid):
    """Extracts coordinates, size, and digit info for each component."""
    components = {}
    for label in range(1, num_features + 1):
        coords_array = np.array(np.where(labeled_array == label)).T
        coords = set(map(tuple, coords_array)) # Use set of tuples
        if not coords:
            continue
        
        digits = [input_grid[r, c] for r, c in coords]
        size = len(coords)
        is_uniform = len(set(digits)) == 1
        most_frequent_digit = Counter(digits).most_common(1)[0][0] if digits else -1
        
        components[label] = {
            'coords': coords,
            'size': size,
            'is_uniform': is_uniform,
            'uniform_digit': digits[0] if is_uniform else -1,
            'most_frequent_digit': most_frequent_digit,
        }
    return components


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to extract and modify the framed content.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    potential_bg_digits = {0, 1, 2, 3}
    frame_coords = set()
    frame_digit = -1

    # --- 1. Try finding objects excluding potential background ---
    object_mask = np.isin(input_array, list(potential_bg_digits), invert=True)
    labeled_obj, num_obj_features = ndimage.label(object_mask, structure=np.ones((3,3), dtype=bool))
    
    if num_obj_features > 0:
        obj_components = get_component_info(labeled_obj, num_obj_features, input_array)
        # Find largest component by size
        largest_label = max(obj_components, key=lambda k: obj_components[k]['size'])
        largest_comp = obj_components[largest_label]
        frame_coords = largest_comp['coords']
        frame_digit = largest_comp['uniform_digit'] if largest_comp['is_uniform'] else largest_comp['most_frequent_digit']
        
    # --- 2. Fallback: Find largest uniform non-zero component if primary method failed ---
    if not frame_coords: 
        non_zero_mask = input_array != 0
        labeled_nz, num_nz_features = ndimage.label(non_zero_mask, structure=np.ones((3,3), dtype=bool))
        
        if num_nz_features > 0:
            nz_components = get_component_info(labeled_nz, num_nz_features, input_array)
            # Sort by size descending
            sorted_labels = sorted(nz_components, key=lambda k: nz_components[k]['size'], reverse=True)
            
            for label in sorted_labels:
                comp = nz_components[label]
                if comp['is_uniform']:
                    frame_coords = comp['coords']
                    frame_digit = comp['uniform_digit']
                    break # Found the largest uniform component

    # --- 3. If no frame identified, return empty ---
    if not frame_coords or frame_digit == -1:
        return []

    # --- 4. Calculate bounding box ---
    bbox = find_bounding_box(frame_coords)
    if bbox is None:
         return []
    min_row, min_col, max_row, max_col = bbox

    # --- 5. Define actual background digits ---
    background_digits = {0}
    present_low_digits = potential_bg_digits.intersection(set(input_array.flatten())) - {0}
    background_digits.update(d for d in present_low_digits if d != frame_digit)

    # --- 6. Create and populate output grid ---
    output_rows = max_row - min_row + 1
    output_cols = max_col - min_col + 1
    output_array = np.zeros((output_rows, output_cols), dtype=int)

    for r_out in range(output_rows):
        for c_out in range(output_cols):
            r_in = min_row + r_out
            c_in = min_col + c_out
            
            original_value = input_array[r_in, c_in]
            original_coord = (r_in, c_in)

            # Check conditions for replacement
            is_background = original_value in background_digits
            is_part_of_frame = original_coord in frame_coords
            
            if is_background and not is_part_of_frame:
                output_array[r_out, c_out] = 0
            else:
                output_array[r_out, c_out] = original_value

    # --- 7. Return result ---
    return output_array.tolist()