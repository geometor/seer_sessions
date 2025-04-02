import numpy as np

"""
Identifies vertical magenta lines (color 6) that span the grid height.
Determines a vertical column range based on these lines:
- If two lines are found at c1 and c2 (c1 < c2), the range is [c1, c2].
- If one line is found at c, the range is [0, c] if red pixels (color 2) exist in columns 0 to c-1,
  or [c, width-1] if red pixels exist in columns c+1 to width-1. If red pixels exist on both sides
  (not observed in examples), or only within column c, the behavior is based on the side with red pixels closest to the line or potentially favoring one side if ambiguous (let's assume it picks the side containing any red pixel). The implementation will check left first, then right.
- If no lines are found, no changes are made.

Within the determined vertical column range [min_col, max_col]:
- Find all red pixels (color 2).
- If red pixels are found, determine the minimum (min_row) and maximum (max_row) row index among them.
- Fill the rectangular region defined by [min_row, max_row] and [min_col, max_col]
  by changing all orange pixels (color 7) within this rectangle to magenta (color 6).
  Existing red and magenta pixels within the region remain unchanged.
"""

def find_magenta_lines(grid):
    """Finds columns composed entirely of magenta (6)."""
    height, width = grid.shape
    line_cols = []
    for c in range(width):
        if np.all(grid[:, c] == 6):
            line_cols.append(c)
    return line_cols

def transform(input_grid):
    """
    Applies the described transformation to the input grid.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # 1. Identify vertical magenta lines
    magenta_line_cols = find_magenta_lines(input_grid)
    num_lines = len(magenta_line_cols)

    min_col = -1
    max_col = -1

    # 2. Determine the vertical range (columns) for filling
    if num_lines == 2:
        min_col = magenta_line_cols[0]
        max_col = magenta_line_cols[1]
    elif num_lines == 1:
        line_col = magenta_line_cols[0]
        # Check for red pixels to the left of the line
        red_exists_left = np.any(input_grid[:, 0:line_col] == 2)
        # Check for red pixels to the right of the line
        red_exists_right = np.any(input_grid[:, line_col+1:width] == 2)
        # Check for red pixels within the line column itself (might be relevant if no red outside)
        # red_exists_in_line_col = np.any(input_grid[:, line_col] == 2) # Unused for now based on examples

        if red_exists_left:
             min_col = 0
             max_col = line_col
        elif red_exists_right:
             min_col = line_col
             max_col = width - 1
        # If red exists only IN the line column, or neither side (edge case not in examples)
        # Current logic based on examples implies fill happens towards the side WITH red pixels.
        # If neither side has red pixels strictly outside the line, no fill based on examples.
        # Let's refine: If red is *only* on the left, fill left. If *only* on the right, fill right.
        # If red is on *both* sides (unlikely per examples), need tie-break - let's stick to the first found side (left)
        # If red is *neither* left nor right (could be in the line col, or nowhere), no fill.
        if not red_exists_left and not red_exists_right:
             # Check if any red pixels exist within the column bounds defined by the line itself
             # If red pixels *only* exist within the line column c, the examples don't clearly define behaviour.
             # Example 4 has red inside the column bounds [3, 4] and the fill happens there.
             # Example 3 has red inside the column bounds [0, 2] and the fill happens there.
             # Let's assume if red exists *anywhere* relative to the line, we pick that side.
             # Re-evaluating the single line case based on observation:
             # It seems sufficient to check if ANY red pixel exists left of OR AT the line column when setting the left boundary,
             # and ANY red pixel exists right of OR AT the line column when setting the right boundary.

             red_indices_left_or_at = np.argwhere(input_grid[:, 0:line_col+1] == 2)
             red_indices_right_or_at = np.argwhere(input_grid[:, line_col:width] == 2)

             if red_indices_left_or_at.size > 0:
                 min_col = 0
                 max_col = line_col
             elif red_indices_right_or_at.size > 0:
                 min_col = line_col
                 max_col = width - 1
             # If still no red found relative to the line, do nothing.


    elif num_lines == 0:
        # No magenta lines, return the original grid
        return output_grid
    # else num_lines > 2 is not expected based on examples

    # If no valid column range was determined (e.g., single line with no relevant red pixels)
    if min_col == -1 or max_col == -1:
        return output_grid

    # 3. Find red pixels within the determined vertical range [min_col, max_col]
    red_pixel_rows = []
    # Iterate only through the selected columns
    for c in range(min_col, max_col + 1):
        for r in range(height):
            if input_grid[r, c] == 2:
                red_pixel_rows.append(r)

    # 4. Determine horizontal bounds if red pixels were found
    if not red_pixel_rows:
        # No red pixels found in the relevant columns, no fill needed
        return output_grid

    min_row = min(red_pixel_rows)
    max_row = max(red_pixel_rows)

    # 5. Fill the identified region
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            # Check the original input grid's color
            if input_grid[r, c] == 7: # If orange
                output_grid[r, c] = 6 # Change to magenta

    return output_grid