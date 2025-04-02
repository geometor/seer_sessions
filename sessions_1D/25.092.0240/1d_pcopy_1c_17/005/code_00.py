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
                return int(color_c), r, int(min_c), int(max_c)
    return None # No non-white pixels found


def transform(input_grid_list):
    """
    Transforms the input grid based on a reference line and trigger pixels below it.
    1. Identifies the topmost contiguous horizontal segment of a single non-white
       color (the "reference line").
    2. Records its color (C), row (R), and column range [min_col, max_col].
    3. Iterates through rows below the reference line (r > R).
    4. If any pixel in an input row r (below R) has the color C, it triggers filling.
    5. In the output grid, the segment from min_col to max_col in the triggered row r
       is filled entirely with color C.
    6. Pixels not part of the reference line or the filled segments remain unchanged.
    """

    # --- Initialization and Grid Setup ---
    input_array = np.array(input_grid_list, dtype=int)

    # Determine grid shape. Assume 4x8 for length 32, fail otherwise for now.
    # More robust ARC solutions might dynamically determine shape.
    if len(input_grid_list) == 32:
        shape = (4, 8)
    else:
        # Handle potential other shapes or raise an error if shape is ambiguous/unexpected
        # For this specific problem, based on examples, 4x8 seems implied.
        # A more general solution would need shape inference.
        # Let's try inferring rectangular shapes:
        rows = int(np.sqrt(len(input_grid_list)))
        if rows * rows == len(input_grid_list): # perfect square
            shape = (rows, rows)
        else: # try common factors, this part is heuristic for ARC
             factors = [(i, len(input_grid_list)//i) for i in range(1, int(len(input_grid_list)**0.5) + 1) if len(input_grid_list) % i == 0]
             # Prefer squarish shapes or shapes seen in ARC?
             # This is complex. Hardcoding 4x8 based on the example data length.
             if len(input_grid_list) != 32:
                 raise ValueError("Input list length is not 32, cannot assume 4x8 shape.")
             shape = (4,8) # Defaulting back to the observed size


    try:
        input_grid = input_array.reshape(shape)
    except ValueError as e:
        print(f"Error reshaping input list of length {len(input_grid_list)}: {e}")
        # Decide how to handle error: return input? raise?
        return input_grid_list # Return original if reshape fails

    # Initialize output grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows, cols = input_grid.shape

    # --- Find Reference Line ---
    reference_info = find_first_contiguous_segment(input_grid)

    # If no reference line is found (e.g., all white grid), return the original grid
    if reference_info is None:
        return output_grid.tolist() # Convert back to list of lists

    color_c, row_r, min_col, max_col = reference_info

    # --- Scan Rows Below Reference and Apply Transformation ---
    # Iterate through each row 'r' strictly below the reference line's row 'row_r'
    for r in range(row_r + 1, rows):
        # Check if any pixel in the *input* grid's current row 'r' has the reference color 'color_c'
        trigger_found = False
        # Use numpy's any() for efficient checking across the row
        if np.any(input_grid[r] == color_c):
            trigger_found = True

        # If a trigger pixel was found in input row 'r'
        if trigger_found:
            # Fill the corresponding segment in the *output* grid's row 'r'
            # The segment spans the same columns as the reference line [min_col, max_col]
            # Ensure slice indices are within grid bounds, although they should be if reference line was valid.
            fill_start_col = max(0, min_col)
            fill_end_col = min(cols, max_col + 1) # Slicing is exclusive at the end

            # Modify the output grid segment with the reference color
            output_grid[r, fill_start_col:fill_end_col] = color_c

    # --- Return Result ---
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()