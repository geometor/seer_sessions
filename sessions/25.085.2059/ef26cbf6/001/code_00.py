import numpy as np

"""
Identifies horizontal bands separated by rows of yellow pixels (4).
Within each band, identifies vertical columns of yellow pixels (4) that separate left and right sub-regions.
Finds the first non-white (0) and non-yellow (4) 'source' color pixel in the left sub-region.
Replaces all blue (1) pixels in the corresponding right sub-region with this 'source' color.
All other pixels (white, yellow, original source colors) remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on color replacement rules within regions defined by yellow separators.

    Args:
        input_grid (list of lists of int): The input grid represented as a 2D list.

    Returns:
        list of lists of int: The transformed grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    num_rows, num_cols = grid.shape

    # 1. Identify horizontal separator rows (all yellow)
    h_sep_rows = [r for r in range(num_rows) if np.all(grid[r, :] == 4)]

    # 2. Define horizontal band boundaries. Include implicit boundaries at the top and bottom.
    band_rows = [-1] + h_sep_rows + [num_rows]

    # 3. Iterate through each horizontal band
    for i in range(len(band_rows) - 1):
        row_start = band_rows[i]
        row_end = band_rows[i+1]

        # Skip if the band is empty or just the separator line itself
        if row_start + 1 >= row_end:
            continue

        # 4. Identify vertical separator columns (all yellow) within the current band
        v_sep_cols = []
        for c in range(num_cols):
             # Check if the column segment within the band boundaries (excluding separators) is all yellow
             if np.all(grid[row_start + 1 : row_end, c] == 4):
                 v_sep_cols.append(c)


        # 5. Define vertical sub-region boundaries within the band
        subregion_cols = [-1] + v_sep_cols + [num_cols]

        # 6. Iterate through adjacent sub-regions defined by vertical separators
        # We need pairs of (left_region, right_region) separated by a v_sep_col
        for j in range(len(v_sep_cols)):
            col_separator = v_sep_cols[j]
            # Define the boundaries for the left region (before the separator)
            col_left_start = subregion_cols[j]
            # Define the boundaries for the right region (after the separator)
            col_right_end = subregion_cols[j+1] # boundary for the right region


            # 7. Find the 'source' color in the left sub-region
            source_color = -1 # Use -1 to indicate not found
            found_source = False
            # Iterate through the cells in the left sub-region for this band
            # Ensure indices stay within grid bounds and region bounds
            for r in range(row_start + 1, row_end):
                for c in range(col_left_start + 1, col_separator):
                     # Check bounds just in case, although loops should handle it
                     # if 0 <= r < num_rows and 0 <= c < num_cols:
                    pixel_value = grid[r, c]
                    if pixel_value != 0 and pixel_value != 4:
                        source_color = pixel_value
                        found_source = True
                        break # Found the first one
                if found_source:
                    break # Stop searching rows once source is found

            # 8. If a source color was found, replace blue pixels in the right sub-region
            if source_color != -1:
                # Iterate through the cells in the right sub-region for this band
                # Ensure indices stay within grid bounds and region bounds
                for r in range(row_start + 1, row_end):
                    for c in range(col_separator + 1, col_right_end):
                        # Check bounds just in case
                        # if 0 <= r < num_rows and 0 <= c < num_cols:
                        if output_grid[r, c] == 1: # If the pixel is blue
                           output_grid[r, c] = source_color # Replace with source color

    # Convert the result back to a list of lists
    return output_grid.tolist()
