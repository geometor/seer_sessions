import numpy as np
import math

"""
This transformation rule operates on a grid containing a 3x3 pattern of blue (1) and azure (8) pixels, and several scattered yellow (4) pixels, against a white (0) background.

1.  **Pattern Rotation:** Identify the unique 3x3 subgrid composed solely of blue (1) and azure (8) pixels. Rotate this 3x3 pattern 90 degrees clockwise in place.
2.  **Yellow Pixel Consolidation:**
    a. Find the coordinates of all yellow (4) pixels in the input grid.
    b. Calculate the median row and median column index of these yellow pixels.
    c. Determine the coordinates of the center pixel of the 3x3 blue/azure pattern.
    d. Apply a specific rounding rule if the median row or column index ends in .5: Round the coordinate towards the corresponding coordinate (row or column) of the pattern's center. For example, if the median row is 3.5 and the pattern center row is 5, round the median row up to 4. If the median row is 3.5 and the pattern center row is 2, round the median row down to 3.
    e. Remove all original yellow pixels from the grid (replace them with white (0)).
    f. Place a single new yellow pixel at the final calculated (and possibly rounded) median coordinate.
3.  **Output:** The grid with the rotated pattern and the consolidated yellow pixel is the output. If no yellow pixels are present in the input, only the pattern rotation occurs.
"""


def find_pattern_location(grid_np):
    """Finds the top-left corner of the 3x3 pattern of blue/azure pixels."""
    height, width = grid_np.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid_np[r:r+3, c:c+3]
            # Check if the subgrid contains only 1s and 8s
            if np.all(np.isin(subgrid, [1, 8])):
                # Optional: Add a check to ensure it's not all 1s or all 8s, if needed
                # if np.any(subgrid == 1) and np.any(subgrid == 8):
                return r, c
    return None # Should not happen based on task description


def custom_round(median_val, center_val):
    """Applies the custom rounding rule for medians ending in .5."""
    if median_val % 1 == 0.5:
        if center_val > median_val:
            return math.ceil(median_val)
        else: # center_val < median_val (center_val cannot equal median_val if median_val ends in .5)
            return math.floor(median_val)
    else:
        # Standard rounding for non-.5 cases (or just truncate/floor if preferred, median usually implies specific handling)
        # Using standard rounding for simplicity here, np.median handles the standard case
        return int(round(median_val))


def transform(input_grid):
    """
    Applies the described transformation: rotates a 3x3 pattern and consolidates yellow pixels.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    height, width = output_grid.shape

    # --- 1. Identify and Rotate Pattern ---
    pattern_loc = find_pattern_location(input_grid_np)
    if pattern_loc:
        pattern_r, pattern_c = pattern_loc
        # Extract the 3x3 pattern
        pattern = input_grid_np[pattern_r:pattern_r+3, pattern_c:pattern_c+3]
        # Rotate the pattern 90 degrees clockwise
        rotated_pattern = np.rot90(pattern, k=-1)
        # Place the rotated pattern back into the output grid
        output_grid[pattern_r:pattern_r+3, pattern_c:pattern_c+3] = rotated_pattern
    else:
        # Handle case where pattern is not found, though examples suggest it's always present
        print("Warning: 3x3 blue/azure pattern not found.")
        return output_grid.tolist() # Return unchanged grid or handle error

    # --- 2. Identify and Consolidate Yellow Pixels ---
    yellow_pixels = np.where(input_grid_np == 4)
    yellow_rows, yellow_cols = yellow_pixels

    if len(yellow_rows) > 0:
        # a. Found yellow pixels coordinates
        
        # b. Calculate Median Coordinates
        median_row = np.median(yellow_rows)
        median_col = np.median(yellow_cols)

        # c. Determine Pattern Center (if pattern was found)
        if pattern_loc:
            center_r = pattern_r + 1
            center_c = pattern_c + 1

            # d. Apply Rounding
            target_r = custom_round(median_row, center_r)
            target_c = custom_round(median_col, center_c)
            
            # Ensure target coordinates are within grid bounds (safety check)
            target_r = max(0, min(height - 1, target_r))
            target_c = max(0, min(width - 1, target_c))

        else: # Fallback if pattern wasn't found - use simple rounding/floor
             target_r = int(round(median_row))
             target_c = int(round(median_col))
             # Ensure target coordinates are within grid bounds
             target_r = max(0, min(height - 1, target_r))
             target_c = max(0, min(width - 1, target_c))


        # e. Remove all original yellow pixels
        output_grid[yellow_rows, yellow_cols] = 0

        # f. Place a single new yellow pixel at the target location
        output_grid[target_r, target_c] = 4

    # --- 3. Final Output ---
    # Convert back to list of lists format
    return output_grid.tolist()
