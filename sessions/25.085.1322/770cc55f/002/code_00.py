# tool_code to verify column sets and subset relationship for each example (fix JSON serialization)
import numpy as np
import json

# Helper to convert numpy types to Python native types for JSON serialization
def convert_to_native_types(obj):
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                        np.int16, np.int32, np.int64, np.uint8,
                        np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float_, np.float16, np.float32,
                          np.float64)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_to_native_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native_types(i) for i in obj]
    return obj


def analyze_example(input_grid_list):
    input_np = np.array(input_grid_list, dtype=int)
    height, width = input_np.shape
    
    red_line_row = -1
    for r in range(height):
        # Check if the entire row is red
        is_full_red_line = np.all(input_np[r, :] == 2)
        # Check if at least one red pixel exists in the row (more robust)
        has_any_red = np.any(input_np[r, :] == 2)

        if is_full_red_line or has_any_red: # Prioritize full lines, but accept partial as indicator
             red_line_row = r
             # Check if *all* red pixels in the grid are on this single row
             red_rows, _ = np.where(input_np == 2)
             if np.all(red_rows == r):
                 break # Found the unique horizontal red line
             else:
                  # Handle cases with multiple red rows or complex shapes if needed
                  # For now, assume the first row found containing red is 'the line'
                  # This matches the simple examples provided.
                  break

    if red_line_row == -1:
        return {"error": "Red line indicator (color 2) not found"}

    paired_object_color = -1
    all_paired_pixels = []
    unique_colors = np.unique(input_np)
    for color in unique_colors:
        if color not in [0, 2]: # Exclude white and red
            paired_object_color = color
            rows, cols = np.where(input_np == paired_object_color)
            all_paired_pixels = list(zip(rows.tolist(), cols.tolist()))
            break # Assume only one such color pair exists per grid
            
    if paired_object_color == -1:
        return {"error": "Paired objects (non-white, non-red) not found"}

    pixels_above = [p for p in all_paired_pixels if p[0] < red_line_row]
    pixels_below = [p for p in all_paired_pixels if p[0] > red_line_row]

    cols_above = set(col for row, col in pixels_above)
    cols_below = set(col for row, col in pixels_below)
    
    intersection = cols_above.intersection(cols_below)
    
    # Use sets for proper subset checking
    is_above_proper_subset_of_below = cols_above.issubset(cols_below) and cols_above != cols_below
    is_below_proper_subset_of_above = cols_below.issubset(cols_above) and cols_below != cols_above
    
    placement = "Undetermined"
        
    if is_above_proper_subset_of_below:
        placement = "Below" # Place on the side of the 'larger' set (Below)
    elif is_below_proper_subset_of_above:
        placement = "Above" # Place on the side of the 'larger' set (Above)
    else:
        # Covers equality, disjoint, and overlapping without subset
        placement = "Above" # Default placement based on Ex 4 logic (also fits Ex 2)

    # Prepare results dictionary with native Python types
    analysis_result = {
        "grid_dims": f"{height}x{width}",
        "red_line_row": red_line_row,
        "paired_color": paired_object_color,
        "pixels_above_count": len(pixels_above),
        "pixels_below_count": len(pixels_below),
        "cols_above": sorted(list(cols_above)),
        "cols_below": sorted(list(cols_below)),
        "intersection": sorted(list(intersection)),
        "is_above_proper_subset_of_below": is_above_proper_subset_of_below,
        "is_below_proper_subset_of_above": is_below_proper_subset_of_above,
        "derived_placement_rule": f"Place {placement}",
    }
    
    return convert_to_native_types(analysis_result)


# Example Inputs (same as before)
ex1_input = [
    [0, 1, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
    [2, 2, 2, 2, 2], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
    [1, 1, 1, 1, 0]
]
ex2_input = [
    [0, 6, 6, 6, 6], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
    [2, 2, 2, 2, 2], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
    [0, 0, 6, 6, 6]
]
ex3_input = [
    [0, 0, 0, 3, 3, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], 
    [2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], 
    [0, 3, 3, 3, 3, 3]
]
ex4_input = [
    [0, 3, 3, 3], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], 
    [2, 2, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], 
    [3, 3, 0, 0]
]

results = {
    "Example 1": analyze_example(ex1_input),
    "Example 2": analyze_example(ex2_input),
    "Example 3": analyze_example(ex3_input),
    "Example 4": analyze_example(ex4_input),
}

print(json.dumps(results, indent=2))
