"""
Transforms the input grid based on a reference line and trigger pixels below it.
1. Assumes the input is a 2D grid (list of lists).
2. Creates a deep copy of the input grid for the output.
3. Identifies the topmost contiguous horizontal segment of a single non-white
   color (the "reference line") by scanning top-down, left-right.
4. Records its color (C), row (R), and column range [min_col, max_col].
5. If no reference line is found, returns the original grid copy.
6. Iterates through rows below the reference line (r > R) in the input grid.
7. If any pixel in an input row r (below R) has the color C, it triggers filling.
8. In the output grid, the segment from min_col to max_col in the triggered row r
   is filled entirely with color C.
9. Pixels not part of the reference line or the filled segments remain unchanged.
10. Returns the modified output grid as a list of lists.
"""

import numpy as np
import copy

def find_first_contiguous_segment(grid):
    """
    Finds the first contiguous horizontal segment of a single non-white color
    encountered when scanning the grid top-to-bottom, left-to-right.

    Args:
        grid (np.ndarray): The input grid (2D NumPy array).

    Returns:
        tuple: (color, row_index, min_col, max_col) if found, otherwise None.
               color is the integer color value.
               row_index is the row where the segment starts.
               min_col is the starting column index of the segment.
               max_col is the ending column index of the segment.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color_c = grid[r, c]
            if color_c != 0:  # Found the first non-white pixel
                # Find the end of the contiguous segment of this color in this row
                min_c = c
                max_c = c
                # Look ahead to find the end of the segment with the *same* color
                while max_c + 1 < cols and grid[r, max_c + 1] == color_c:
                    max_c += 1
                # Found the first segment, return its properties
                # Ensure types are standard Python ints
                return int(color_c), int(r), int(min_c), int(max_c)
    return None # No non-white pixels found


def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid_list (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # --- Initialization and Grid Setup ---
    # Convert input list of lists to a NumPy array for efficient processing
    try:
        input_grid = np.array(input_grid_list, dtype=int)
    except ValueError:
        # Handle potentially inconsistent row lengths if necessary, although ARC spec implies rectangular
        print("Warning: Input grid might not be rectangular.")
        # Attempt to proceed if possible, or return input/raise error
        return copy.deepcopy(input_grid_list) # Return copy if conversion fails

    # Create a deep copy for the output grid to modify
    output_grid = copy.deepcopy(input_grid)
    rows, cols = input_grid.shape

    # --- Find Reference Line ---
    # Use the helper function to find the reference segment properties
    reference_info = find_first_contiguous_segment(input_grid)

    # If no reference line is found (e.g., all white grid), return the initial copy
    if reference_info is None:
        # Convert back to list of lists before returning
        return output_grid.tolist()

    # Unpack the reference line properties
    color_c, row_r, min_col, max_col = reference_info

    # --- Scan Rows Below Reference and Apply Transformation ---
    # Iterate through each row 'r' strictly below the reference line's row 'row_r'
    for r in range(row_r + 1, rows):
        # Check if any pixel in the *input* grid's current row 'r' has the reference color 'color_c'
        # Use numpy's any() for efficient checking across the row
        trigger_found = np.any(input_grid[r] == color_c)

        # If a trigger pixel was found in input row 'r'
        if trigger_found:
            # Fill the corresponding segment in the *output* grid's row 'r'
            # The segment spans the same columns as the reference line [min_col, max_col]
            # Ensure slice indices are within grid bounds, although they should be valid
            # if the reference line was correctly found within bounds.
            fill_start_col = max(0, min_col)
            fill_end_col = min(cols, max_col + 1) # Slicing is exclusive at the end

            # Modify the output grid segment with the reference color
            output_grid[r, fill_start_col:fill_end_col] = color_c

    # --- Return Result ---
    # Convert the final numpy array back to a list of lists format
    return output_grid.tolist()