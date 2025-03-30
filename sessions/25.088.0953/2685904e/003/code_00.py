"""
Transforms an input grid based on control information from specific rows and a color frequency condition.

1.  Initialize the output grid as a copy of the input grid.
2.  Identify Control Parameters:
    a.  Examine the first row (row 0). Count azure (8) pixels to get height `H`.
    b.  Find `R_anchor`, the index of the first all-gray (5) row.
    c.  Find `R_source`, the index of the last row with any non-white (0) pixel.
3.  Analyze Source Row Colors:
    a.  Get the colors in row `R_source`.
    b.  Count the frequency of each unique non-white color in this row.
4.  Determine Colors to Draw:
    a.  Create a set `selected_colors`. A color `C` is included if its frequency in the source row equals `H`.
5.  Draw Vertical Lines:
    a.  For each column `c`:
    b.  Get the color `C` at `input_grid[R_source, c]`.
    c.  If `C` is in `selected_colors`:
        i. Draw a vertical line of color `C` in column `c` of the output grid.
        ii. The line spans `H` rows, from row `max(0, R_anchor - H)` up to `R_anchor - 1` (inclusive).
6.  Return the modified output grid.
"""

import numpy as np
from collections import Counter

def find_anchor_row(grid):
    """Finds the index of the first row consisting entirely of gray (5) pixels."""
    height, width = grid.shape
    for r in range(height):
        if np.all(grid[r, :] == 5):
            return r
    return -1 # Indicator that no anchor row was found

def find_source_color_row(grid):
    """Finds the index of the last row containing at least one non-white (0) pixel."""
    height, width = grid.shape
    for r in range(height - 1, -1, -1): # Iterate backwards from bottom row
        if np.any(grid[r, :] != 0):
            return r
    return -1 # Indicator that no source row was found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # 1. Identify Height Control Row (row 0) and count azure pixels (H)
    height_control_row = input_np[0, :]
    H = np.count_nonzero(height_control_row == 8)

    # Handle edge case where H is 0 (no lines to draw)
    if H == 0:
        return output_grid.tolist() # Return the original grid

    # 2. Identify the Anchor Row (first all-gray row)
    R_anchor = find_anchor_row(input_np)
    if R_anchor == -1:
        # Handle error or unexpected input: no anchor row found
        print("Warning: No anchor row (all gray) found.")
        return output_grid.tolist() # Return original grid

    # 3. Identify the Source Color Row (last non-white row)
    R_source = find_source_color_row(input_np)
    if R_source == -1:
         # Handle error or unexpected input: no source row found
         print("Warning: No source row (non-white pixels) found.")
         return output_grid.tolist() # Return original grid

    # 4. Analyze colors in the Source Color Row
    source_row_content = input_np[R_source, :]
    non_white_colors_in_source = source_row_content[source_row_content != 0]

    # Handle case where source row has only white pixels (should technically be caught by find_source_color_row)
    if len(non_white_colors_in_source) == 0:
         return output_grid.tolist() # No colors to analyze or draw

    # Calculate frequency of each non-white color
    color_counts = Counter(non_white_colors_in_source)

    # 5. Determine which colors to draw based on frequency matching H
    selected_colors = {color for color, count in color_counts.items() if count == H}

    # 6. Iterate through columns and draw lines for selected colors
    for c in range(width):
        # Get the source color C for the current column
        C = source_row_content[c]

        # Check if the color C is one of the selected colors
        if C in selected_colors:
            # Determine the start and end rows for the line
            # End row is one above the anchor row (exclusive upper bound for range)
            # Start row is H rows above the end row (inclusive lower bound)
            start_row_inclusive = max(0, R_anchor - H)
            end_row_exclusive = R_anchor

            # Draw the vertical line in the output grid
            for r in range(start_row_inclusive, end_row_exclusive):
                 # Ensure row index is valid (already handled by max(0, ...) but good practice)
                 if r >= 0 and r < height:
                     output_grid[r, c] = C

    # Return the modified grid as a list of lists
    return output_grid.tolist()