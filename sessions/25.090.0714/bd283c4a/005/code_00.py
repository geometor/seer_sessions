import numpy as np
from collections import Counter

"""
Processes the input grid according to the following transformation rules:

1.  Divide the input grid vertically into two halves based on the middle column index (`mid = width // 2`). The left half includes columns `0` to `mid-1`, and the right half includes columns `mid` to `width-1`.
2.  Left Half Transformation:
    a. Find the most frequent color (`C_left`) in the input grid's left half. If there's a tie in frequency, the color with the lowest numerical value is chosen.
    b. Fill the output grid's left half entirely with this `C_left` color.
3.  Right Half Transformation:
    a. Find the most frequent color (`C_right_bg`) in the input grid's right half. This acts as the 'background' color. Tie-breaking uses the lowest numerical value.
    b. Process columns `j` from the middle index (`mid`) up to, but not including, the last column (`width-1`):
        i. Identify all pixels in the input column `j` whose color is *not* `C_right_bg`. Store them as `(color, row_index)` pairs.
        ii. If no such non-background pixels exist in the column, fill the corresponding output column `j` entirely with `C_right_bg`.
        iii. If non-background pixels exist, determine the dominant color (`C_dom`) for the column:
            - Find the non-background color with the highest frequency in the column.
            - Tie-break 1: Choose the color whose lowest instance (maximum row index) appears lower (has a larger row index).
            - Tie-break 2: If still tied, choose the color with the lowest numerical value.
        iv. Fill the entire output column `j` with this dominant color `C_dom`. (Note: This rule is based on observations and may not be perfectly accurate, especially the tie-breaking).
    c. Process the last column (`j = width - 1`):
        i. Determine the fill color `C_prev` used for the output column `width-2` based on the calculation in step 3b. Handle cases where `width-2` is not in the right half (use `C_right_bg` as fallback).
        ii. Identify all non-`C_right_bg` pixels `(color, row_index)` in the input's last column.
        iii. If no such non-background pixels exist, fill the output's last column entirely with `C_prev` (or `C_right_bg` if `width-1` is the first column in the right half).
        iv. If non-background pixels exist:
            - Find `C1` = the numerically highest color value among all non-`C_right_bg` pixels in the input's last column.
            - Find `r_low` = the maximum row index among all non-`C_right_bg` pixels in the input's last column.
            - Let `C2 = C_prev` (or `C_right_bg` as fallback if `width-1 == mid`).
            - Fill the output's last column from row 0 down to `r_low` (inclusive) with `C1`.
            - Fill the output's last column from row `r_low + 1` down to the last row with `C2`. (This rule is based on observations from one example and might not generalize).
"""

def find_most_frequent_color(grid_part):
    """
    Finds the most frequent color in a grid or subgrid.
    Tie-breaking: lowest numerical value wins.
    """
    if grid_part.size == 0:
        return 0 # Default for empty part
    counts = Counter(grid_part.flatten())
    # Handle case where grid_part might be empty after flatten (e.g., if masked)
    if not counts:
         # Check if the original grid part had elements
         if grid_part.size > 0:
             # This case implies all elements were filtered out or grid had weird structure
             # Let's return the first element if possible, else 0
             try:
                return grid_part.flat[0]
             except IndexError:
                return 0 # Truly empty or problematic grid part
         else:
             return 0 # Original grid part was empty

    most_common = counts.most_common()
    # Ensure most_common list is not empty before accessing its elements
    if not most_common:
        return 0 # No elements counted, return default

    max_count = most_common[0][1]
    tied_colors = [color for color, count in most_common if count == max_count]
    # Return the minimum color value among those tied
    return min(tied_colors) if tied_colors else 0


def find_dominant_color_with_tie_break(column_colors_with_indices):
    """
    Finds the dominant color in a list of (color, index) tuples from a column.
    Dominant is most frequent.
    Tie-break 1: Color whose lowest instance (max index) is largest (appears further down).
    Tie-break 2: Lowest numerical color value if max indices are also tied.
    """
    # This function assumes column_colors_with_indices is not empty.
    # Caller handles the empty case.

    colors = [item[0] for item in column_colors_with_indices]
    counts = Counter(colors)

    most_common = counts.most_common()
    # Added check in case colors list becomes empty somehow (shouldn't happen)
    if not most_common:
        return 0 # Default color if no counts

    max_count = most_common[0][1]
    tied_colors = [color for color, count in most_common if count == max_count]

    if len(tied_colors) == 1:
        # No tie in frequency
        return tied_colors[0]
    else:
        # --- Tie-breaking logic ---
        max_row_indices = {}
        # Find the maximum row index for each tied color
        for color in tied_colors:
            indices = [idx for c, idx in column_colors_with_indices if c == color]
            if indices: # Should always be true if color is in tied_colors
                max_row_indices[color] = max(indices)
            else: # Defensive programming: if somehow a tied color has no indices
                 max_row_indices[color] = -1 # Assign invalid index

        # Find the maximum 'max_row_index' among the tied colors
        max_last_row = -1
        for color in tied_colors:
             # Check if color exists in max_row_indices before accessing
            if color in max_row_indices and max_row_indices[color] > max_last_row:
                max_last_row = max_row_indices[color]

        # Check if max_last_row was updated (i.e., at least one valid max index found)
        if max_last_row == -1:
             # This implies issues, maybe all indices were -1? Fallback to lowest value tie-break
             return min(tied_colors) if tied_colors else 0

        # Identify colors that achieve this maximum last row index
        colors_at_max_row = [color for color in tied_colors if color in max_row_indices and max_row_indices[color] == max_last_row]

        if len(colors_at_max_row) == 1:
             # Tie broken by lowest position
             return colors_at_max_row[0]
        else:
             # Final tie-break: lowest color value among those still tied
             # Ensure colors_at_max_row is not empty before min()
             return min(colors_at_max_row) if colors_at_max_row else min(tied_colors) if tied_colors else 0


def transform(input_grid):
    """
    Applies the described transformation rules to the input grid.
    """
    input_grid = np.array(input_grid, dtype=int)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    if width == 0 or height == 0:
        return [] # Handle empty grid case

    # Determine the midpoint column for splitting
    mid_col = width // 2

    # --- Process Left Half (Columns 0 to mid_col - 1) ---
    if mid_col > 0: # Check if there is a left half
        left_half_input = input_grid[:, :mid_col]
        if left_half_input.size > 0:
             # Calculate most frequent color for the left half
             c_left = find_most_frequent_color(left_half_input)
             # Fill the output grid's left half
             output_grid[:, :mid_col] = c_left

    # --- Process Right Half (Columns mid_col to width - 1) ---
    if mid_col < width: # Check if there is a right half
        right_half_input = input_grid[:, mid_col:]

        if right_half_input.size > 0:
            # Find background color for the right half
            c_right_bg = find_most_frequent_color(right_half_input)

            # Store calculated dominant colors for columns mid to width-2
            # This is needed to determine C_prev for the last column calculation.
            dominant_colors_cache = {}

            # Process columns from mid_col up to width - 2
            for j_abs in range(mid_col, width - 1):
                input_col = input_grid[:, j_abs]
                # Find non-background colors and their row indices in this column
                non_bg_colors_with_indices = []
                for r in range(height):
                    if input_col[r] != c_right_bg:
                        non_bg_colors_with_indices.append((input_col[r], r))

                # Determine the dominant color for the column
                if not non_bg_colors_with_indices:
                    # If column only contains background color, fill with background color
                    c_dom = c_right_bg
                else:
                    # Find dominant color using frequency and tie-breaking rules
                    c_dom = find_dominant_color_with_tie_break(non_bg_colors_with_indices)

                # Fill the output column and cache the result
                output_grid[:, j_abs] = c_dom
                dominant_colors_cache[j_abs] = c_dom

            # Process the last column (j_abs = width - 1)
            if width > 0: # Check grid width again just in case
                last_col_idx_abs = width - 1
                # Ensure last column is actually part of the right half before processing
                if last_col_idx_abs >= mid_col:
                    last_col = input_grid[:, last_col_idx_abs]

                    # Determine C_prev (the fill color of the previous column in the right half)
                    prev_col_idx = last_col_idx_abs - 1
                    if prev_col_idx >= mid_col and prev_col_idx in dominant_colors_cache:
                         # Get the cached dominant color of the column at width-2
                         c_prev = dominant_colors_cache[prev_col_idx]
                    else:
                         # If previous column doesn't exist in the right half (i.e., last col is the first col of right half)
                         # or if something went wrong with caching, use C_right_bg as a fallback.
                         c_prev = c_right_bg

                    # Find non-background pixels in the last input column
                    non_bg_last_with_indices = []
                    non_bg_colors_last_col = []
                    for r in range(height):
                        color = last_col[r]
                        if color != c_right_bg:
                            non_bg_last_with_indices.append((color, r))
                            non_bg_colors_last_col.append(color)

                    if not non_bg_last_with_indices:
                        # If last column has no non-background colors, fill with C_prev
                        output_grid[:, last_col_idx_abs] = c_prev
                    else:
                        # Find C1 = numerically highest non-bg color in this column
                        c1 = max(non_bg_colors_last_col)

                        # Find r_low = max row index of any non-bg pixel in this column
                        r_low = max(item[1] for item in non_bg_last_with_indices)

                        # C2 is the color used for the bottom part, defaults to C_prev
                        c2 = c_prev

                        # Fill the output's last column based on C1, r_low, and C2
                        output_grid[:r_low + 1, last_col_idx_abs] = c1 # Fill rows 0 to r_low (inclusive) with C1
                        if r_low + 1 < height: # Check if there are rows below r_low
                           output_grid[r_low + 1:, last_col_idx_abs] = c2 # Fill rows r_low+1 to end with C2

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()