import numpy as np
import math

"""
Transforms a grid containing a unique 3x3 pattern of blue (1) and azure (8) pixels, and potentially scattered yellow (4) pixels, against a white (0) background.

1.  **Initialize:** Create a copy of the input grid.
2.  **Find Pattern:** Locate the unique 3x3 subgrid composed entirely of blue (1) and azure (8) pixels. Record its top-left coordinates (`pattern_r`, `pattern_c`).
3.  **Analyze Pattern:**
    a. Extract the 3x3 pattern.
    b. Count the total number of blue pixels (`count_blue`) and azure pixels (`count_azure`).
    c. Identify the four corner pixels (top-left, top-right, bottom-left, bottom-right).
    d. Count how many corner pixels are blue (`count_corner_blue`).
    e. Record the pattern's center coordinates (`pattern_center_r`, `pattern_center_c`).
4.  **Rotate Pattern:** Modify the pattern *in place* within the output grid copy based on counts:
    a. If `count_azure > count_blue`: Rotate the pattern 180 degrees.
    b. If `count_blue > count_azure`:
        i.  If `count_corner_blue` is 4: Rotate 90 degrees clockwise.
        ii. If `count_corner_blue` is 3: Rotate 90 degrees counter-clockwise.
        iii. If `count_corner_blue` is 2: Rotate 90 degrees counter-clockwise.  # Corrected rule
    (Other counts for `corner_blue` when `count_blue > count_azure` are not expected based on examples).
    c. Otherwise (counts equal), do not rotate.
5.  **Consolidate Yellow Markers (if present):**
    a. Find coordinates of all yellow (4) pixels in the original input grid.
    b. If yellow pixels exist:
        i. Calculate median row (`median_row`) and column (`median_col`).
        ii. If pattern was found, use its center coordinates (`center_r`, `center_c`).
        iii. Calculate target coordinates (`target_r`, `target_c`) using custom rounding for medians ending in .5 (round towards pattern center if available, otherwise standard rounding), standard rounding otherwise.
        iv. In the output grid, remove all original yellow pixels (set to white 0).
        v. In the output grid, place a single yellow pixel at (`target_r`, `target_c`).
6.  **Output:** Return the modified grid.
"""

def find_pattern_location(grid_np):
    """Finds the top-left corner of the 3x3 pattern of blue(1)/azure(8) pixels."""
    height, width = grid_np.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid_np[r:r+3, c:c+3]
            # Check if the subgrid contains only 1s and 8s and is not uniform
            # and is exactly 3x3
            if subgrid.shape == (3, 3) and \
               np.all(np.isin(subgrid, [1, 8])) and \
               len(np.unique(subgrid)) > 1:
                 return r, c
    return None # Should not happen based on task description but good practice

def analyze_pattern_corners(pattern):
    """Counts the number of blue pixels in the corners of a 3x3 pattern."""
    # Corners are relative to the 3x3 pattern: (0,0), (0,2), (2,0), (2,2)
    corners = [pattern[0, 0], pattern[0, 2], pattern[2, 0], pattern[2, 2]]
    count_corner_blue = sum(1 for pixel in corners if pixel == 1)
    return count_corner_blue

def custom_round(median_val, center_val):
    """
    Applies the custom rounding rule for medians ending in .5.
    Rounds towards the center coordinate if the median is exactly halfway.
    """
    if median_val % 1 == 0.5:
        # If median is exactly halfway, round towards the center coordinate
        if center_val > median_val:
            return math.ceil(median_val)
        elif center_val < median_val:
             return math.floor(median_val)
        else: # center_val == median_val - should not happen if median ends in .5
             # but if it does, standard rounding is fine.
             return int(round(median_val))
    else:
        # Standard rounding for non-.5 cases (round half up)
        return int(round(median_val))


def transform(input_grid):
    """
    Applies the transformation: rotates a 3x3 pattern based on color counts and corner analysis,
    and consolidates yellow pixels using median and custom rounding relative to the pattern center.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # 1. Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    height, width = output_grid.shape

    # --- 2. Find Pattern ---
    pattern_loc = find_pattern_location(input_grid_np)
    pattern_center_r, pattern_center_c = -1, -1 # Initialize pattern center

    if pattern_loc:
        pattern_r, pattern_c = pattern_loc
        # e. Record pattern's center coordinates
        pattern_center_r = pattern_r + 1
        pattern_center_c = pattern_c + 1

        # --- 3. Analyze Pattern ---
        # a. Extract the 3x3 pattern
        pattern = input_grid_np[pattern_r:pattern_r+3, pattern_c:pattern_c+3]
        # b. Count blue and azure pixels
        count_blue = np.count_nonzero(pattern == 1)
        count_azure = np.count_nonzero(pattern == 8)
        # d. Count blue pixels in corners
        count_corner_blue = analyze_pattern_corners(pattern)

        # --- 4. Rotate Pattern ---
        rotated_pattern = pattern # Default to no rotation if conditions aren't met
        rotation_k = 0 # np.rot90 k value (0: 0, 1: 90ccw, 2: 180, 3: 90cw)

        # a. Check condition: Azure > Blue
        if count_azure > count_blue:
            rotation_k = 2 # Rotate 180 degrees
        # b. Check condition: Blue > Azure
        elif count_blue > count_azure:
            # i. Check corner count == 4
            if count_corner_blue == 4:
                rotation_k = 3 # Rotate 90 degrees clockwise (k=3 is 270 CCW)
            # ii. Check corner count == 3
            elif count_corner_blue == 3:
                rotation_k = 1 # Rotate 90 degrees counter-clockwise
            # iii. Check corner count == 2 (CORRECTED)
            elif count_corner_blue == 2:
                rotation_k = 1 # Rotate 90 degrees counter-clockwise
            # Other corner counts not covered by examples when Blue > Azure

        # Apply the determined rotation
        if rotation_k != 0:
            rotated_pattern = np.rot90(pattern, k=rotation_k)

        # Place the (potentially) rotated pattern back into the output grid
        output_grid[pattern_r:pattern_r+3, pattern_c:pattern_c+3] = rotated_pattern
    else:
        # Handle case where pattern is not found (though examples suggest it's always present)
        print("Warning: 3x3 blue/azure pattern not found.")
        # Continue without rotation, yellow consolidation might use standard rounding if pattern center unknown

    # --- 5. Consolidate Yellow Markers (if present) ---
    # a. Find coordinates of all yellow pixels in the *original* input
    yellow_pixels = np.where(input_grid_np == 4)
    yellow_rows, yellow_cols = yellow_pixels

    # b. Check if yellow pixels exist
    if len(yellow_rows) > 0:
        # i. Calculate Median Coordinates
        median_row = np.median(yellow_rows)
        median_col = np.median(yellow_cols)

        # ii. Determine target coordinates with custom/standard rounding
        if pattern_loc:
             # Use custom rounding relative to pattern center
            target_r = custom_round(median_row, pattern_center_r)
            target_c = custom_round(median_col, pattern_center_c)
        else:
            # Fallback if pattern wasn't found - cannot use custom rounding
            # Use standard rounding (round half up)
            target_r = int(round(median_row))
            target_c = int(round(median_col))
            print("Warning: Yellow pixels consolidated using standard rounding due to missing pattern.")

        # Ensure target coordinates are within grid bounds (safety check)
        target_r = max(0, min(height - 1, target_r))
        target_c = max(0, min(width - 1, target_c))

        # iv. Remove all original yellow pixels from the output grid
        output_grid[yellow_rows, yellow_cols] = 0 # Set to white

        # v. Place a single new yellow pixel at the target location in the output grid
        output_grid[target_r, target_c] = 4
    # Else: No yellow pixels found, do nothing.

    # --- 6. Final Output ---
    # Convert back to list of lists format
    return output_grid.tolist()