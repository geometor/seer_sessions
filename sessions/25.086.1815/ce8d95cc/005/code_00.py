import numpy as np
from typing import List, Tuple, Optional, Dict
from collections import Counter

"""
Compresses an input grid by extracting significant rows and columns and arranging 
them into a new grid that represents their intersections and connecting segments.

1.  Identify Significant Rows: Scan the input grid row by row. A row is 
    considered "significant" if it either contains more than one distinct 
    non-white color OR if the entire row consists of a single non-white color. 
    Record the indices of these significant rows in order.
2.  Identify Significant Columns: Scan the input grid column by column. A column 
    is considered "significant" if it contains any non-white pixel located in 
    a row whose index was *not* identified as a significant row in step 1. 
    Record the indices of these significant columns in order.
3.  Determine Output Dimensions: Calculate the output grid height as 
    `2 * (number of significant rows) + 1` and the width as 
    `2 * (number of significant columns) + 1`.
4.  Initialize Output Grid: Create an output grid of the calculated dimensions, 
    filled entirely with white (color 0).
5.  Populate Output Grid: Iterate through each cell `(r_out, c_out)` of the 
    output grid:
    *   Intersection Points (r_out is odd, c_out is odd): Find the 
        corresponding significant row index `r_in = sig_rows[r_out // 2]` and 
        significant column index `c_in = sig_cols[c_out // 2]`. Fill the output 
        cell `(r_out, c_out)` with the color from the input grid at 
        `input[r_in, c_in]`.
    *   Horizontal Segments (r_out is odd, c_out is even): Find the 
        corresponding significant row index `r_in = sig_rows[r_out // 2]`. 
        Examine the pixels in this input row `input[r_in, :]` located at column 
        indices that are *not* significant columns. Identify the most frequent 
        non-white color among these pixels. Fill the output cell `(r_out, c_out)` 
        with this dominant color (if no such non-white pixels exist, leave it 
        white).
    *   Vertical Segments (r_out is even, c_out is odd): Find the 
        corresponding significant column index `c_in = sig_cols[c_out // 2]`. 
        Examine the pixels in this input column `input[:, c_in]` located at 
        row indices that are *not* significant rows. Identify the most frequent 
        non-white color among these pixels. Fill the output cell `(r_out, c_out)` 
        with this dominant color (if no such non-white pixels exist, leave it 
        white).
    *   Corner Points (r_out is even, c_out is even): Leave the output cell 
        white (0).
6.  Return the populated output grid.
"""

def find_significant_rows(grid: np.ndarray) -> List[int]:
    """
    Identifies significant rows based on the criteria:
    - Contains more than one distinct non-white color.
    - Is entirely filled with the same single non-white color.
    Returns a list of significant row indices.
    """
    sig_rows = []
    height, width = grid.shape
    for r in range(height):
        row = grid[r, :]
        non_white_pixels = row[row != 0]
        unique_non_white = np.unique(non_white_pixels)

        if len(unique_non_white) > 1:
            # Criterion 1: More than one distinct non-white color
            sig_rows.append(r)
        elif len(unique_non_white) == 1:
            # Check if it's a single non-white color
            # Criterion 2: Entire row is this single non-white color
            if len(non_white_pixels) == width:
                 sig_rows.append(r)
    return sig_rows

def find_significant_columns(grid: np.ndarray, sig_row_indices: List[int]) -> List[int]:
    """
    Identifies significant columns based on the criteria:
    - Contains at least one non-white pixel at a row index that is NOT significant.
    Returns a list of significant column indices.
    """
    sig_cols = []
    height, width = grid.shape
    sig_row_set = set(sig_row_indices)

    for c in range(width):
        column = grid[:, c]
        found_non_white_outside_sig_row = False
        for r in range(height):
            if grid[r, c] != 0 and r not in sig_row_set:
                found_non_white_outside_sig_row = True
                break # Found one, no need to check further in this column
        if found_non_white_outside_sig_row:
            sig_cols.append(c)
    return sig_cols

def find_most_frequent(colors: List[int]) -> Optional[int]:
    """
    Finds the most frequent color in a list of colors.
    Returns the color, or None if the list is empty.
    Handles ties by returning the smallest color index (arbitrary but consistent).
    """
    if not colors:
        return None
    
    counts = Counter(colors)
    # Find the maximum count
    max_count = 0
    for color in counts:
        if counts[color] > max_count:
            max_count = counts[color]
            
    # Find all colors with the maximum count
    most_common_colors = [color for color, count in counts.items() if count == max_count]
    
    # If there's a tie, return the smallest color index among the most frequent
    if not most_common_colors: # Should not happen if input list is not empty
         return None
    return min(most_common_colors)


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the grid compression transformation.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Identify Significant Rows
    sig_rows = find_significant_rows(grid)
    sig_row_set = set(sig_rows) # For faster lookups

    # 2. Identify Significant Columns
    sig_cols = find_significant_columns(grid, sig_rows)
    sig_col_set = set(sig_cols) # For faster lookups

    # 3. Determine Output Dimensions
    output_height = 2 * len(sig_rows) + 1
    output_width = 2 * len(sig_cols) + 1

    # 4. Initialize Output Grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 5. Populate Output Grid
    for r_out in range(output_height):
        is_sig_row_line = r_out % 2 != 0 # Corresponds to a significant row index

        for c_out in range(output_width):
            is_sig_col_line = c_out % 2 != 0 # Corresponds to a significant column index

            if is_sig_row_line and is_sig_col_line:
                # Case: Intersection Point (r_out odd, c_out odd)
                r_idx_in_list = r_out // 2
                c_idx_in_list = c_out // 2
                if 0 <= r_idx_in_list < len(sig_rows) and 0 <= c_idx_in_list < len(sig_cols):
                    r_in = sig_rows[r_idx_in_list]
                    c_in = sig_cols[c_idx_in_list]
                    output_grid[r_out, c_out] = grid[r_in, c_in]
                # else: remains 0 (should not happen with valid indices)

            elif is_sig_row_line and not is_sig_col_line:
                # Case: Horizontal Segment (r_out odd, c_out even)
                r_idx_in_list = r_out // 2
                if 0 <= r_idx_in_list < len(sig_rows):
                    r_in = sig_rows[r_idx_in_list]
                    # Collect non-white colors in this row from non-significant columns
                    segment_colors = [grid[r_in, c] for c in range(width) if c not in sig_col_set and grid[r_in, c] != 0]
                    dominant_color = find_most_frequent(segment_colors)
                    output_grid[r_out, c_out] = dominant_color if dominant_color is not None else 0
                # else: remains 0

            elif not is_sig_row_line and is_sig_col_line:
                # Case: Vertical Segment (r_out even, c_out odd)
                c_idx_in_list = c_out // 2
                if 0 <= c_idx_in_list < len(sig_cols):
                    c_in = sig_cols[c_idx_in_list]
                    # Collect non-white colors in this column from non-significant rows
                    segment_colors = [grid[r, c_in] for r in range(height) if r not in sig_row_set and grid[r, c_in] != 0]
                    dominant_color = find_most_frequent(segment_colors)
                    output_grid[r_out, c_out] = dominant_color if dominant_color is not None else 0
                # else: remains 0

            else: # not is_sig_row_line and not is_sig_col_line
                # Case: Background Corner (r_out even, c_out even)
                # Already initialized to 0 (white), so no action needed.
                pass

    # 6. Return Output Grid as list of lists
    return output_grid.tolist()