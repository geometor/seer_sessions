```python
import numpy as np
from collections import Counter

# Constants for colors
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3
YELLOW = 4
GRAY = 5

"""
The transformation rule depends on the location (left or right of a central gray vertical line) of 'significant' colors (Red or Green).

1.  **Find Separator**: Identify the vertical column composed entirely of gray pixels (5). This divides the grid into left and right parts.
2.  **Determine Case**: Check if Red (2) or Green (3) pixels exist exclusively on the left side or exclusively on the right side of the gray separator.
    *   **Case A (Left)**: If Red or Green appear only on the left side.
    *   **Case B (Right)**: If Red or Green appear only on the right side.

3.  **Transformation Logic**:

    *   **Case A (Left Side Rule)**:
        a.  Create an output grid with the same height as the input and a fixed width of 7, initialized to White (0).
        b.  Set the central column (index 3) of the output grid entirely to Blue (1).
        c.  Iterate through each row `r` of the input grid:
            i.  Examine the portion of the input row `r` to the left of the gray separator.
            ii. If Red (2) is present in this left portion, fill all cells in the corresponding output row `r`, *except* the central column (index 3), with Red (2).
            iii.Else if Green (3) is present in this left portion, fill all cells in the corresponding output row `r`, *except* the central column (index 3), with Green (3).
            iv. Otherwise (if neither Red nor Green is present on the left), the output row `r` remains White (0) in the non-central columns and Blue (1) in the center.

    *   **Case B (Right Side Rule)**:
        a.  Create an output grid with the same height as the input and a fixed width of 7, initialized to White (0).
        b.  **Find Pattern Row**: Locate the row (`pattern_r`) in the input grid that contains Blue (1) pixels *to the right* of the gray separator. Extract the segment of this row to the right of the separator as the `pattern_p`.
        c.  **Find Special Row**: Identify the row index (`yellow_r`) in the input grid which has the *maximum number* of Yellow (4) pixels *to the left* of the gray separator. This row determines the unique row in the output.
        d.  **Fill Fixed Columns**: Determine two colors from the `pattern_p`. The color at index 1 of `pattern_p` dictates the color for the entire output column 2. The color at index 3 of `pattern_p` dictates the color for the entire output column 4.
        e.  **Fill Special Row**: Populate the output row `yellow_r` based on an expanded version of `pattern_p`. Specifically:
            - output[yellow_r, 0] = pattern_p[0]
            - output[yellow_r, 1] = pattern_p[0]
            - output[yellow_r, 2] = pattern_p[1] (already set in step 3d)
            - output[yellow_r, 3] = pattern_p[2]
            - output[yellow_r, 4] = pattern_p[3] (already set in step 3d)
            - output[yellow_r, 5] = pattern_p[4]
            - output[yellow_r, 6] = pattern_p[4]
        f.  All other rows in the output (rows != `yellow_r`) retain their White (0) background in the columns not set in step 3d (columns 0, 1, 3, 5, 6).

"""

def find_gray_separator(grid):
    """Finds the index of the first column composed entirely of GRAY pixels."""
    height, width = grid.shape
    for c in range(width):
        # Check if all elements in the column are GRAY
        if np.all(grid[:, c] == GRAY):
            return c
    # Return -1 if no such column is found (should not happen based on examples)
    return -1

def check_significant_color_location(grid, sep_col):
    """Checks if Red(2) or Green(3) are present left or right of the separator."""
    height, width = grid.shape
    # Define the significant colors
    sig_colors = {RED, GREEN}

    # Check left side (columns before separator)
    left_colors = set()
    if sep_col > 0:
        left_colors = set(grid[:, :sep_col].flatten())
    left_has_sig = bool(sig_colors.intersection(left_colors))

    # Check right side (columns after separator)
    right_colors = set()
    if sep_col < width - 1:
        right_colors = set(grid[:, sep_col+1:].flatten())
    right_has_sig = bool(sig_colors.intersection(right_colors))

    # Determine location based on exclusive presence
    if left_has_sig and not right_has_sig:
        return "left"
    elif right_has_sig and not left_has_sig:
        return "right"
    elif left_has_sig and right_has_sig:
         # This case wasn't explicitly in examples, assume 'left' as priority or handle error
         # Based on re-evaluation, examples seem mutually exclusive.
         # Let's treat this as ambiguous for now.
         print("Warning: Significant colors found on both sides.")
         return "ambiguous"
    else:
        # No significant colors found anywhere
        return "none"

def transform_case_a(input_grid, sep_col):
    """Handles transformation when significant colors (Red/Green) are on the left."""
    height, width = input_grid.shape
    output_height = height
    output_width = 7
    # Initialize output grid with white background
    output_grid = np.full((output_height, output_width), WHITE, dtype=int)

    # Set the central column (index 3) to blue
    output_grid[:, 3] = BLUE

    # Process each row based on colors found on the left side
    for r in range(height):
        # Extract the segment of the row left of the separator
        if sep_col > 0:
             left_row_segment = input_grid[r, :sep_col]
        else:
             left_row_segment = np.array([]) # Handle edge case where separator is column 0

        fill_color = WHITE # Default fill color if no significant color found
        if RED in left_row_segment:
            fill_color = RED
        elif GREEN in left_row_segment:
            fill_color = GREEN
        # Else: fill_color remains WHITE

        # Fill the non-central columns of the output row if needed
        if fill_color != WHITE:
            for c in range(output_width):
                if c != 3: # Do not overwrite the central blue column
                    output_grid[r, c] = fill_color
            # Note: central column remains blue

    return output_grid

def find_max_yellow_row(grid, sep_col):
    """Finds the index of the row with the most YELLOW pixels left of the separator."""
    height = grid.shape[0]
    max_yellow_count = -1
    yellow_r = -1
    if sep_col <= 0: # No left side to check
        return -1
        
    for r in range(height):
        left_row_segment = grid[r, :sep_col]
        # Count occurrences of YELLOW in the left segment
        yellow_count = np.count_nonzero(left_row_segment == YELLOW)
        # Update if this row has more yellow pixels than the current max
        if yellow_count > 0 and yellow_count >= max_yellow_count: # >= handles ties, preferring later rows if counts equal
             # Small correction: if counts are equal, maybe prefer first row? Let's stick to ">" first.
             # After checking Example 4, it seems just ">" is sufficient if there's a unique max.
             # Let's try >= to be robust against ties, taking the last one. If that fails, revert to >.
             # Reverting to > as the original logic implicitly picked the unique max row 4 in example 4.
             # If yellow_count > max_yellow_count: -> This seems safer if a unique max exists.
             if yellow_count > max_yellow_count:
                 max_yellow_count = yellow_count
                 yellow_r = r
                 
    # If max_yellow_count is still 0 (or -1), no yellow was found
    if max_yellow_count <= 0:
        return -1 # Indicate no suitable yellow row found

    return yellow_r


def transform_case_b(input_grid, sep_col):
    """Handles transformation when significant colors (Red/Green) are on the right."""
    height, width = input_grid.shape
    output_height = height
    output_width = 7
    # Initialize output grid with white background
    output_grid = np.full((output_height, output_width), WHITE, dtype=int)

    # --- Find pattern row (contains BLUE on right side) ---
    pattern_r = -1
    pattern_p = None
    if sep_col < width - 1:
        for r in range(height):
            # Extract segment right of separator
            right_row_segment = input_grid[r, sep_col+1:]
            # Check if Blue exists in this segment
            if BLUE in right_row_segment:
                pattern_r = r
                pattern_p = right_row_segment
                break # Found the first pattern row

    if pattern_p is None:
        print(f"Error: Pattern row (with Blue right of col {sep_col}) not found.")
        return output_grid # Return empty grid or handle error appropriately

    # --- Find special output row (row with max YELLOW on left side) ---
    yellow_r = find_max_yellow_row(input_grid, sep_col)

    if yellow_r == -1:
        print(f"Error: Yellow row (left of col {sep_col}) not found or none had max count.")
        return output_grid # Return empty grid or handle error appropriately

    # --- Determine fixed column colors from pattern P ---
    # Ensure pattern has enough elements for indices 1 and 3
    if len(pattern_p) < 4:
         print(f"Error: Pattern P (length {len(pattern_p)}) is too short for column definition.")
         return output_grid

    fixed_col_2_color = pattern_p[1] # Color for output column 2
    fixed_col_4_color = pattern_p[3] # Color for output column 4

    # --- Fill fixed columns ---
    output_grid[:, 2] = fixed_col_2_color
    output_grid[:, 4] = fixed_col_4_color

    # --- Fill the special row (yellow_r) based on expanded pattern P ---
    # Ensure pattern has enough elements for indices 0, 2, 4
    if len(pattern_p) < 5:
         print(f"Error: Pattern P (length {len(pattern_p)}) is too short for special row fill.")
         # We might still be able to fill columns, but not the special row fully.
         # Let's return the grid with columns filled but potentially incomplete special row.
         return output_grid

    # Fill cells in the special row 'yellow_r'
    output_grid[yellow_r, 0] = pattern_p[0]
    output_grid[yellow_r, 1] = pattern_p[0]
    # output_grid[yellow_r, 2] is already set by column fill
    output_grid[yellow_r, 3] = pattern_p[2]
    # output_grid[yellow_r, 4] is already set by column fill
    output_grid[yellow_r, 5] = pattern_p[4]
    output_grid[yellow_r, 6] = pattern_p[4]

    # --- Rows other than yellow_r keep WHITE background in non-fixed columns ---
    # This is already handled by initializing with WHITE and only filling fixed columns
    # and the specific special row.

    return output_grid


def transform(input_grid):
    """
    Transforms the input grid based on the location of Red/Green relative
    to a vertical gray line.
    """
    # Convert input to numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Find the gray separator column
    sep_col = find_gray_separator(input_grid_np)
    if sep_col == -1:
        print("Error: Gray separator column not found.")
        # Return a default grid or original if separator is mandatory but missing
        # Let's return an empty grid of expected size as a fallback.
        # Size might vary, let's default to 7 width and original height
        return np.full((height, 7), WHITE, dtype=int).tolist()

    # 2. Determine location of significant colors (Red=2, Green=3)
    location = check_significant_color_location(input_grid_np, sep_col)

    # 3. Apply transformation based on location
    if location == "left":
        output_grid_np = transform_case_a(input_grid_np, sep_col)
    elif location == "right":
        output_grid_np = transform_case_b(input_grid_np, sep_col)
    elif location == "ambiguous":
         print("Ambiguous case: Significant colors on both sides. No defined transformation.")
         # Return default/empty grid
         output_grid_np = np.full((height, 7), WHITE, dtype=int)
    else: # location == "none"
        print("Warning: Significant colors (Red/Green) not found.")
        # Define behavior if no Red/Green found. Maybe return Case A default?
        # Let's return the default white grid with blue center from Case A.
        output_grid_np = np.full((height, 7), WHITE, dtype=int)
        output_grid_np[:, 3] = BLUE


    # Convert the final numpy grid back to a list of lists
    return output_grid_np.tolist()
```