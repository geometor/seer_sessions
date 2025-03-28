```python
import numpy as np
import math

"""
This transformation rule operates on a grid containing a unique 3x3 pattern of blue (1) and azure (8) pixels, and potentially several scattered yellow (4) pixels, against a white (0) background.

1.  **Identify the Pattern:** Locate the unique 3x3 subgrid composed entirely of blue (1) and azure (8) pixels. Note its top-left coordinates.
2.  **Analyze Pattern Content:** Count the number of blue pixels (`count_blue`) and azure pixels (`count_azure`) within this 3x3 pattern.
3.  **Rotate the Pattern:**
    *   If `count_blue` is greater than `count_azure`, rotate the 3x3 pattern 90 degrees counter-clockwise in place.
    *   Otherwise (if `count_azure` is greater than or equal to `count_blue`), rotate the 3x3 pattern 180 degrees in place.
4.  **Consolidate Yellow Markers (if present):**
    a. Find the coordinates (row, column) of all yellow (4) pixels in the original input grid.
    b. If yellow pixels exist:
        i. Calculate the median row (`median_row`) and median column (`median_col`) from the list of yellow pixel coordinates.
        ii. Find the center coordinates (row `center_r`, column `center_c`) of the 3x3 blue/azure pattern (which is its top-left row + 1, top-left column + 1).
        iii. Determine the final target coordinates (`target_r`, `target_c`) by applying a specific rounding rule to the median coordinates:
            - For `median_row`: If it ends in .5, round it towards `center_r` (up if `center_r > median_row`, down if `center_r < median_row`). Otherwise, apply standard rounding (e.g., `int(round(x))`). Assign the result to `target_r`.
            - For `median_col`: If it ends in .5, round it towards `center_c` (up if `center_c > median_col`, down if `center_c < median_col`). Otherwise, apply standard rounding (e.g., `int(round(x))`). Assign the result to `target_c`.
        iv. Remove all original yellow pixels from the grid (change their color to white (0)).
        v. Place a single new yellow pixel at the calculated (`target_r`, `target_c`).
5.  **Output:** The resulting grid, containing the rotated pattern and the single consolidated yellow pixel (if any were present initially), is the final output.
"""


def find_pattern_location(grid_np):
    """Finds the top-left corner of the 3x3 pattern of blue/azure pixels."""
    height, width = grid_np.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid_np[r:r+3, c:c+3]
            # Check if the subgrid contains only 1s and 8s and is not uniform
            if np.all(np.isin(subgrid, [1, 8])) and len(np.unique(subgrid)) > 1:
                 return r, c
    return None # Should not happen based on task description but good practice


def custom_round(median_val, center_val):
    """Applies the custom rounding rule for medians ending in .5."""
    if median_val % 1 == 0.5:
        if center_val > median_val:
            # Round towards center (up)
            return math.ceil(median_val)
        else: # center_val < median_val (center_val cannot equal median_val if median_val ends in .5)
             # Round towards center (down)
            return math.floor(median_val)
    else:
        # Standard rounding for non-.5 cases (round half up)
        return int(round(median_val))


def transform(input_grid):
    """
    Applies the described transformation: conditionally rotates a 3x3 pattern
    and consolidates yellow pixels based on median and custom rounding.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    height, width = output_grid.shape

    # --- 1. Identify Pattern ---
    pattern_loc = find_pattern_location(input_grid_np)
    pattern_center_r, pattern_center_c = -1, -1 # Initialize pattern center

    if pattern_loc:
        pattern_r, pattern_c = pattern_loc
        pattern_center_r = pattern_r + 1
        pattern_center_c = pattern_c + 1

        # Extract the 3x3 pattern
        pattern = input_grid_np[pattern_r:pattern_r+3, pattern_c:pattern_c+3]

        # --- 2. Analyze Pattern Content ---
        count_blue = np.count_nonzero(pattern == 1)
        count_azure = np.count_nonzero(pattern == 8)

        # --- 3. Rotate the Pattern ---
        if count_blue > count_azure:
            # Rotate 90 degrees counter-clockwise
            rotated_pattern = np.rot90(pattern, k=1)
        else: # count_azure >= count_blue
            # Rotate 180 degrees
            rotated_pattern = np.rot90(pattern, k=2)

        # Place the rotated pattern back into the output grid
        output_grid[pattern_r:pattern_r+3, pattern_c:pattern_c+3] = rotated_pattern
    else:
        # Handle case where pattern is not found (though examples suggest it's always present)
        print("Warning: 3x3 blue/azure pattern not found.")
        # Continue without rotation, but yellow consolidation might fail if it relies on center

    # --- 4. Consolidate Yellow Markers (if present) ---
    yellow_pixels = np.where(input_grid_np == 4)
    yellow_rows, yellow_cols = yellow_pixels

    if len(yellow_rows) > 0:
        # a. Found yellow pixels coordinates

        # b.i Calculate Median Coordinates
        median_row = np.median(yellow_rows)
        median_col = np.median(yellow_cols)

        # Check if pattern was found before trying to use its center
        if pattern_loc:
            # b.ii Find Pattern Center (already done above)

            # b.iii Apply Custom Rounding Rule
            target_r = custom_round(median_row, pattern_center_r)
            target_c = custom_round(median_col, pattern_center_c)

            # Ensure target coordinates are within grid bounds (safety check)
            target_r = max(0, min(height - 1, target_r))
            target_c = max(0, min(width - 1, target_c))

            # b.iv Remove all original yellow pixels
            # Important: Do this *after* finding the pattern and calculating target location
            # to avoid erasing the target if it overlaps an original yellow pixel.
            output_grid[yellow_rows, yellow_cols] = 0

            # b.v Place a single new yellow pixel at the target location
            output_grid[target_r, target_c] = 4
        else:
            # Fallback if pattern wasn't found - cannot use custom rounding
            # Use standard rounding and remove/place yellow pixels
            target_r = int(round(median_row))
            target_c = int(round(median_col))
            target_r = max(0, min(height - 1, target_r))
            target_c = max(0, min(width - 1, target_c))
            output_grid[yellow_rows, yellow_cols] = 0
            output_grid[target_r, target_c] = 4
            print("Warning: Yellow pixels consolidated using standard rounding due to missing pattern.")


    # --- 5. Final Output ---
    # Convert back to list of lists format
    return output_grid.tolist()
```