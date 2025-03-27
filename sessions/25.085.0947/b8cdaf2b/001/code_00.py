import numpy as np
from collections import defaultdict

def _find_pattern_row(grid_np):
    """
    Finds the lowest row containing a contiguous segment of one non-background color (C_central)
    flanked (not necessarily adjacently) by pixels of another non-background color (F_frame)
    within the same row.

    Returns:
        tuple: (R_source, C_central, F_frame, central_segment_columns, framing_pixel_columns)
               or None if no such row is found.
    """
    height, width = grid_np.shape
    for r in range(height - 1, -1, -1): # Iterate rows bottom-up
        row = grid_np[r]
        colors_data = defaultdict(list)
        non_background_pixels = False
        for c in range(width):
            color = row[c]
            if color != 0:
                colors_data[color].append(c)
                non_background_pixels = True

        if not non_background_pixels or len(colors_data) < 2:
            continue # Skip rows with no non-background pixels or only one non-background color

        # Check each color as a potential C_central
        for C_central, central_cols_list in colors_data.items():
            central_cols = sorted(central_cols_list)
            min_c = central_cols[0]
            max_c = central_cols[-1]

            # Check if the central segment is contiguous
            is_contiguous = all(central_cols[i] == central_cols[0] + i for i in range(len(central_cols)))
            if not is_contiguous:
                continue # This color block isn't contiguous, cannot be the central one

            # Check if it's flanked by any single other non-background color
            found_flanker = False
            F_frame = -1
            framing_cols = []
            for other_color, other_cols_list in colors_data.items():
                if other_color == C_central:
                    continue
                
                other_cols = sorted(other_cols_list)
                has_left_flank = any(oc < min_c for oc in other_cols)
                has_right_flank = any(oc > max_c for oc in other_cols)

                if has_left_flank and has_right_flank:
                    # Found a valid flanking color F_frame
                    found_flanker = True
                    F_frame = other_color
                    framing_cols = other_cols # Use all pixels of this flanking color in the row
                    break # Stop checking other colors once a valid flanker is found

            if found_flanker:
                # Found the pattern row and its components
                return r, C_central, F_frame, central_cols, framing_cols

    return None # No pattern row found

def transform(input_grid):
    """
    Identifies a specific horizontal pattern in the lowest possible row: a contiguous segment
    of a central color (C) flanked by pixels of a framing color (F) (F...F C...C F...F).
    For each framing pixel F in that row at column c_frame, calculates the minimum horizontal
    distance (dist) to the central segment C. Adds a new pixel of color C at row
    (source_row - dist - 1) and column c_frame.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid_np = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # 1. Find the source pattern row and its characteristics
    pattern_info = _find_pattern_row(input_grid_np)

    if pattern_info is None:
        # If no pattern row is found, return the original grid
        return output_grid_np.tolist()

    R_source, C_central, F_frame, central_segment_columns, framing_pixel_columns = pattern_info

    # 2. Calculate and place the added pixels
    for c_frame in framing_pixel_columns:
        # Calculate the minimum horizontal distance to the central segment
        min_dist = float('inf')
        for c_central in central_segment_columns:
            dist = abs(c_frame - c_central)
            if dist < min_dist:
                min_dist = dist

        # Calculate the target row index
        # The distance used seems to be the gap size, not direct distance?
        # Let's re-check examples.
        # Ex 1: F(0), C(1,2,3), F(4). R_source=4. C_central=1.
        # F(0): Closest C is at 1. dist=1. R_output = 4 - 1 - 1 = 2. Correct.
        # F(4): Closest C is at 3. dist=1. R_output = 4 - 1 - 1 = 2. Correct.
        # Ex 2: F(0,1), C(2), F(3,4). R_source=4. C_central=3.
        # F(0): Closest C is at 2. dist=2. R_output = 4 - 2 - 1 = 1. Correct.
        # F(1): Closest C is at 2. dist=1. R_output = 4 - 1 - 1 = 2. Correct.
        # F(3): Closest C is at 2. dist=1. R_output = 4 - 1 - 1 = 2. Correct.
        # F(4): Closest C is at 2. dist=2. R_output = 4 - 2 - 1 = 1. Correct.
        # Ex 4: F(0), C(1), F(2). R_source=2. C_central=4.
        # F(0): Closest C is at 1. dist=1. R_output = 2 - 1 - 1 = 0. Correct.
        # F(2): Closest C is at 1. dist=1. R_output = 2 - 1 - 1 = 0. Correct.
        # Okay, the distance calculation `min(abs(c_frame - c_central))` seems correct.
        
        R_output = R_source - min_dist - 1

        # Check if the target row is within grid bounds
        if R_output >= 0:
            # Check if the target column is within grid bounds (should always be true)
            if 0 <= c_frame < width:
                 # Place the pixel (overwriting if necessary, though examples show it lands on background)
                 output_grid_np[R_output, c_frame] = C_central

    # 3. Return the modified grid as a list of lists
    return output_grid_np.tolist()