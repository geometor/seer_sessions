import numpy as np

"""
Extract a specific sub-pattern located below a horizontal white separator in the 
input grid. The target sub-pattern is identified by its primary color, which is 
the non-white color found in the lower section (below the separator) that is 
different from the primary non-white color found in the upper section (above 
the separator). The output is the minimal bounding box enclosing all pixels of 
this target color within the lower section.
"""

def find_separator_end_row(grid_np):
    """
    Finds the index of the last row of the first horizontal block 
    of all-white (0) rows. Returns -1 if no such block is found before 
    a non-white row, or the last row index if the grid ends with the separator.
    """
    in_separator = False
    separator_end_row = -1
    num_rows = grid_np.shape[0]

    for r in range(num_rows):
        is_all_white = np.all(grid_np[r, :] == 0)
        if is_all_white:
            if not in_separator:
                # Found the start of a potential separator block
                # Check if this is the very first row
                is_first_row_separator = (r == 0)
                # Or if the previous row was not all white
                is_previous_not_separator = (r > 0 and not np.all(grid_np[r-1, :] == 0))
                
                if is_first_row_separator or is_previous_not_separator:
                     in_separator = True # Start of the *first* separator block
                
            if in_separator:
                separator_end_row = r # Update the end row as long as we see white rows within the first block
        elif in_separator:
            # We found a non-white row *after* being in the first separator block
            return separator_end_row # The previous row was the end
        # else: not in separator or not the first separator, and not all white, continue scanning

    # If the grid ends with the first separator block or is all white
    if in_separator:
        return separator_end_row
        
    # If no separator block was ever entered (e.g., grid has no all-white rows)
    return -1

def get_unique_non_white_colors(grid_region_np):
    """Returns a list of unique non-zero colors in a given grid region."""
    if grid_region_np.size == 0:
        return []
    return list(np.unique(grid_region_np[grid_region_np != 0]))

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    grid_np = np.array(input_grid, dtype=int)
    num_rows, num_cols = grid_np.shape

    # 1. Find the end row of the separator block
    separator_end_row = find_separator_end_row(grid_np)

    # Handle edge case: No separator found or separator is the entire grid or ends at the last row
    if separator_end_row == -1 or separator_end_row >= num_rows - 1:
        # Cannot determine upper/lower regions or no lower region exists
        return [] 

    # Define upper and lower region start rows
    upper_region_end_row = separator_end_row # The separator itself isn't part of upper pattern content
    lower_region_start_row = separator_end_row + 1

    # Extract regions (careful with slicing limits)
    upper_region_np = grid_np[:upper_region_end_row, :] if upper_region_end_row > 0 else np.array([[]])
    lower_region_np = grid_np[lower_region_start_row:, :]
    
    # Check if lower region actually exists
    if lower_region_np.shape[0] == 0:
        return []

    # 2. Identify the unique non-white color in the upper region
    upper_colors = get_unique_non_white_colors(upper_region_np)
    # Assuming there's typically one dominant color. Handle cases if needed.
    # If upper region is all white or empty, this list will be empty.
    upper_color = upper_colors[0] if len(upper_colors) > 0 else -1 # Use -1 if no upper color

    # 3. Identify all unique non-white colors in the lower region
    lower_section_colors = get_unique_non_white_colors(lower_region_np)

    # 4. Determine the target color 
    target_color = -1 # Default if not found
    possible_target_colors = [c for c in lower_section_colors if c != upper_color]
    
    if len(possible_target_colors) == 1:
        target_color = possible_target_colors[0]
    elif len(possible_target_colors) == 0 and len(lower_section_colors) > 0:
         # This might happen if the only color below is the same as above,
         # or if the upper part had no color. Assume the single lower color is the target.
         if len(lower_section_colors) == 1:
              target_color = lower_section_colors[0]
         else:
             # Ambiguous case: multiple lower colors, none different from upper.
             # Based on examples, this shouldn't happen. Return empty?
             return []
    elif len(possible_target_colors) > 1:
         # Ambiguous case: multiple colors below are different from the upper color.
         # Based on examples, this shouldn't happen. Return empty?
         return []
    else: # No non-white colors in lower section at all
        return []


    # 5. Find coordinates of the target color *only within the lower section rows*
    # We search the original grid but filter by row index >= lower_region_start_row
    all_coords = np.argwhere(grid_np == target_color)
    target_coords = all_coords[all_coords[:, 0] >= lower_region_start_row]


    # 6. If no pixels matching target_color are found in the lower section
    if target_coords.size == 0:
        return [] 

    # 7. Calculate the minimal bounding box based on these coordinates
    min_row = np.min(target_coords[:, 0])
    max_row = np.max(target_coords[:, 0])
    min_col = np.min(target_coords[:, 1])
    max_col = np.max(target_coords[:, 1])

    # 8. Extract the subgrid from the original input grid using the bounding box
    output_grid_np = grid_np[min_row : max_row + 1, min_col : max_col + 1]

    # Convert back to list of lists
    output_grid = output_grid_np.tolist()

    return output_grid