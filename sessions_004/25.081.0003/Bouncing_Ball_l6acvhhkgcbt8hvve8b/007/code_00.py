"""
1.  **Identify:** Locate all pixels with the color yellow (4) and red (2) within the input grid.

2.  **Condition Check:** Determine if *all* of the following conditions are met:
    *   All yellow pixels are in the same column.
    *   All red pixels are in the same column.
    *   The column containing yellow pixels is the same as the column containing red pixels.
    *   All yellow pixels are positioned vertically *above* all red pixels.

3.  **Conditional Transformation:**
    *   If *all* conditions in step 2 are TRUE, the output grid is identical to the input grid. No changes are made.
    *   If *any* condition in step 2 is FALSE, swap the vertical positions (row indices) of *all* yellow pixels with the vertical positions of *all* red pixels, while keeping their horizontal positions (column indices) the same. That is, if a yellow pixel is at (r1, c1) and a red pixel is at (r2, c2), after swapping the yellow pixel *that had that column* will be at (r2, c1) and the red pixel *that had that column* will be at (r1, c2).
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of pixels with the specified color."""
    return np.argwhere(grid == color)

def are_in_same_column(pixels):
    """Checks if all pixels are in the same column."""
    if len(pixels) == 0:
        return True  # Vacuously true for empty lists
    first_col = pixels[0][1]
    return all(p[1] == first_col for p in pixels)

def are_yellow_above_red(yellow_pixels, red_pixels):
    """Checks if all yellow pixels are above all red pixels."""
    if len(yellow_pixels) == 0 or len(red_pixels) == 0:
        return True # vacuously true
    return all(y[0] < r[0] for y in yellow_pixels for r in red_pixels)

def transform(input_grid):
    """Transforms the input grid according to the swapping rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    yellow_pixels = find_pixels_by_color(input_grid, 4)
    red_pixels = find_pixels_by_color(input_grid, 2)

    # Condition Check
    same_column_yellow = are_in_same_column(yellow_pixels)
    same_column_red = are_in_same_column(red_pixels)
    same_column_both = (same_column_yellow and same_column_red and
                         (len(yellow_pixels) == 0 or len(red_pixels) == 0 or yellow_pixels[0][1] == red_pixels[0][1]))
    yellow_above_red = are_yellow_above_red(yellow_pixels, red_pixels)

    all_conditions_met = same_column_yellow and same_column_red and same_column_both and yellow_above_red

    # Conditional Transformation
    if all_conditions_met:
        return output_grid  # No change
    else:
        # Swap all yellow and red pixels
        for y_r, y_c in yellow_pixels:
          output_grid[y_r, y_c] = 0 # clear
        for r_r, r_c in red_pixels:
          output_grid[r_r, r_c] = 0 # clear

        for y_r, y_c in yellow_pixels:
            for r_r, r_c in red_pixels:
                if y_c == r_c: # find matching column red pixel
                    output_grid[r_r, y_c] = 4
                    break

        for r_r, r_c in red_pixels:
          for y_r, y_c in yellow_pixels:
            if r_c == y_c: # find matching column yellow pixel
              output_grid[y_r,r_c] = 2
              break

    return output_grid