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
            - If there's a tie in frequency, compare the tied colors based on the row index of their lowest occurrence (maximum row index) in the column. The color whose lowest instance is further down (larger row index) wins the tie.
            - If there's still a tie (multiple colors have their lowest instance on the same maximum row), choose the color with the lowest numerical value among them.
        iv. Fill the entire output column `j` with this dominant color `C_dom`.
    c. Process the last column (`j = width - 1`):
        i. Identify all non-`C_right_bg` pixels `(color, row_index)` in the input's last column.
        ii. If no such non-background pixels exist, fill the output's last column entirely with `C_right_bg`.
        iii. If non-background pixels exist:
            - Find the pixel `(C_top, r_top)` among them that has the minimum row index (`r_top`).
            - Find the pixel `(C_bot, r_bot)` among them that has the maximum row index (`r_bot`). Note: `C_bot` is the color at the maximum row index, not necessarily the color with the highest value.
            - Fill the output's last column from row 0 down to `r_top` (inclusive) with the color `C_top`.
            - Fill the output's last column from row `r_top + 1` down to the last row with the color `C_bot`.
"""

def find_most_frequent_color(grid_part):
    """
    Finds the most frequent color in a grid or subgrid.
    Tie-breaking: lowest numerical value wins.
    """
    if grid_part.size == 0:
        return 0 # Default for empty part
    counts = Counter(grid_part.flatten())
    if not counts:
         if grid_part.size > 0:
             # Should only happen if grid contains only one element type
             return grid_part.flat[0] 
         else:
             return 0 # Should be covered by size check, but safety first

    most_common = counts.most_common()
    max_count = most_common[0][1]
    # Find all colors with the maximum count
    tied_colors = [color for color, count in most_common if count == max_count]
    # Return the minimum color value among those tied
    return min(tied_colors)


def find_dominant_color_with_tie_break(column_colors_with_indices):
    """
    Finds the dominant color in a list of (color, index) tuples from a column.
    Dominant is most frequent. 
    Tie-break 1: Color whose lowest instance (max index) is largest (appears further down).
    Tie-break 2: Lowest numerical color value if max indices are also tied.
    """
    # This function assumes column_colors_with_indices is not empty,
    # the caller should handle the empty case.
    
    colors = [item[0] for item in column_colors_with_indices]
    counts = Counter(colors)
    
    most_common = counts.most_common()
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
            # indices should not be empty if color is in tied_colors
            max_row_indices[color] = max(indices) 
        
        # Find the maximum 'max_row_index' among the tied colors
        max_last_row = -1
        for color in tied_colors:
            if max_row_indices[color] > max_last_row:
                max_last_row = max_row_indices[color]
        
        # Identify colors that achieve this maximum last row index
        colors_at_max_row = [color for color in tied_colors if max_row_indices[color] == max_last_row]

        if len(colors_at_max_row) == 1:
             # Tie broken by lowest position
             return colors_at_max_row[0]
        else:
             # Final tie-break: lowest color value among those still tied
             return min(colors_at_max_row)


def transform(input_grid):
    """
    Applies the described transformation rules to the input grid.
    """
    input_grid = np.array(input_grid, dtype=int)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    
    # Determine the midpoint column for splitting
    mid_col = width // 2

    # --- Process Left Half (Columns 0 to mid_col - 1) ---
    if mid_col > 0: # Check if there is a left half
        left_half_input = input_grid[:, :mid_col]
        if left_half_input.size > 0:
             c_left = find_most_frequent_color(left_half_input)
             output_grid[:, :mid_col] = c_left
    
    # --- Process Right Half (Columns mid_col to width - 1) ---
    if mid_col < width: # Check if there is a right half
        right_half_input = input_grid[:, mid_col:]
        
        if right_half_input.size > 0:
            # Find background color for the right half
            c_right_bg = find_most_frequent_color(right_half_input)

            # Process columns from mid_col up to width - 2
            # Loop uses absolute column index j_abs
            for j_abs in range(mid_col, width - 1): 
                input_col = input_grid[:, j_abs]
                
                # Find non-background colors and their row indices
                non_bg_colors_with_indices = []
                for r in range(height):
                    if input_col[r] != c_right_bg:
                        non_bg_colors_with_indices.append((input_col[r], r))

                if not non_bg_colors_with_indices:
                    # If column only contains background color, fill output with background color
                    output_grid[:, j_abs] = c_right_bg
                else:
                    # Determine the dominant color using frequency and tie-breaking rules
                    c_dom = find_dominant_color_with_tie_break(non_bg_colors_with_indices)
                    # Fill the entire output column with the dominant color
                    output_grid[:, j_abs] = c_dom

            # Process the last column (j_abs = width - 1)
            if width > 0: # Ensure grid isn't empty
                last_col_idx_abs = width - 1
                # Check if the last column is actually part of the right half
                if last_col_idx_abs >= mid_col: 
                    last_col = input_grid[:, last_col_idx_abs]
                    
                    # Find non-background colors and their row indices in the last column
                    non_bg_last_with_indices = []
                    for r in range(height):
                        if last_col[r] != c_right_bg:
                            non_bg_last_with_indices.append((last_col[r], r))

                    if not non_bg_last_with_indices:
                        # If only background exists, fill output with background color
                        output_grid[:, last_col_idx_abs] = c_right_bg
                    else:
                        # Find the top-most non-background pixel (color and row)
                        # min(_, key=lambda) finds the item with the minimum value according to the key function (item[1] is row index)
                        c_top, r_top = min(non_bg_last_with_indices, key=lambda item: item[1])
                        
                        # Find the bottom-most non-background pixel (color and row)
                        # max(_, key=lambda) finds the item with the maximum value according to the key function (item[1] is row index)
                        c_bot, r_bot = max(non_bg_last_with_indices, key=lambda item: item[1]) 

                        # Fill the output column based on top and bottom colors/rows
                        output_grid[:r_top + 1, last_col_idx_abs] = c_top # Fill from row 0 to r_top (inclusive)
                        if r_top + 1 < height: # Check if there are rows below r_top to fill
                           output_grid[r_top + 1:, last_col_idx_abs] = c_bot # Fill from row r_top + 1 to the end

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()