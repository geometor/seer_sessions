"""
The transformation extracts a repeating sub-pattern from the input grid. The sub-pattern itself is
surrounded by a complex border.  The border appears to use alternating stripes of different
colors, but the exact colors in the border are not essential for finding the
inner pattern. The output pattern is tiled within a larger rectangle. The key is identifying one instance of the sub-pattern within the larger input.

1. **Identify Border:** The border in Example 1 is composed of alternating stripes of 1, 3, 5, 7, and 9. The inner region has colors 1, 2, 3, 6, 7, 8, and 9. In Example 2, the outer "border" consists of rows of 0, 2, 4, 6, 8. The border is not a consistent, solid background.

2. **Find Repeating Sub-Pattern:**  Instead of cropping, we look for repetition *within* a candidate output object.

3. **Extract Sub-Pattern:** Once the repeating unit is found, reconstruct the output based on its full, repeating structure.

"""

import numpy as np
from collections import Counter

def get_dimensions(grid):
    return np.array(grid).shape

def analyze_grid(grid):
    grid_array = np.array(grid)
    unique_colors = np.unique(grid_array)
    color_counts = Counter(grid_array.flatten())
    return unique_colors.tolist(), color_counts

def find_repeating_subpattern(grid):
    """
    Attempts to find a repeating subpattern within the grid.
    Returns the subpattern as a list of lists, or None if no clear repetition is found.
    """
    grid = np.array(grid)
    rows, cols = grid.shape

    # Iterate through possible subpattern sizes
    for sub_rows in range(1, rows // 2 + 1):  # Subpattern height
        for sub_cols in range(1, cols // 2 + 1):  # Subpattern width
            if rows % sub_rows == 0 and cols % sub_cols == 0:
                subpattern = grid[:sub_rows, :sub_cols]
                valid_subpattern = True

                # Check if the entire grid can be tiled by this subpattern
                for i in range(0, rows, sub_rows):
                    for j in range(0, cols, sub_cols):
                        if not np.array_equal(grid[i:i+sub_rows, j:j+sub_cols], subpattern):
                            valid_subpattern = False
                            break  # Exit inner loop on mismatch
                    if not valid_subpattern:
                        break # Exit outer loop

                if valid_subpattern:
                    return subpattern.tolist()

    return None  # No repeating subpattern found

def transform(input_grid):
    # Find repeating sub-pattern
    subpattern = find_repeating_subpattern(input_grid)

    if subpattern:

        # remove any border rows and cols
        input_grid = np.array(input_grid) # ensure input is numpy array
        unique_input_colors = analyze_grid(input_grid)[0]
        unique_output_colors = analyze_grid(subpattern)[0]
        border_colors = [c for c in unique_input_colors if c not in unique_output_colors]

        # Find rows/cols to keep using color
        rows_to_keep = np.any(~np.isin(input_grid, border_colors), axis=1)
        cols_to_keep = np.any(~np.isin(input_grid, border_colors), axis=0)
      
        cropped_grid = input_grid[rows_to_keep, :]
        cropped_grid = cropped_grid[:, cols_to_keep]      
        cropped_subpattern = find_repeating_subpattern(cropped_grid)
        if cropped_subpattern is not None:
           return cropped_subpattern
        else:
           return subpattern

    else:
        return input_grid  # Return original if no subpattern found