"""
The transformation rule can be summarized as follows:

1.  **Initial Scan:** Examine the entire input grid, noting the positions of all colors.
2.  **Color Substitution:**
    *   Replace all occurrences of color '5' (grey) with color '0' (white).
3. **Influence and propagation:**
    * scan for all colors that are not 0
    * build lists of contiguous, horizontal pixels
    * compare each grouping to the output, find corresponding grouping, if any
        * 2,2,2 -> 2,2,2
        * 8,6 -> 6,6
        * 6,6 -> 6,6
        * 5,8,8 -> 8,6,6 - unclear, not enough data
        * 5 -> 0, 2 -> 2, 8->8,8,8
4.  Iterate through the original positions of color '8'. For each '8':
    *   Check for a '6' from the group.
        *    Change '8' to '6'.
    *   Propagate, replace the '8' with '6' in the output grid.
5. The 2's stay.
6. Copy other values, adjusting the output.
"""

import numpy as np

def find_contiguous_groups(grid):
    """Finds contiguous horizontal groups of non-zero pixels."""
    groups = []
    for row in grid:
        current_group = []
        for pixel in row:
            if pixel != 0:
                current_group.append(pixel)
            elif current_group:
                groups.append(current_group)
                current_group = []
        if current_group:  # Append last group in row, if any.
             groups.append(current_group)
    return groups


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Replace all 5s with 0s.
    output_grid[output_grid == 5] = 0

    # find groups
    input_groups = find_contiguous_groups(input_grid)
    #print(input_groups)

    # process groups
    for r, row in enumerate(input_grid):
      for c, pixel in enumerate(row):
          if pixel == 8:
            if c+1 < len(row) and row[c+1] == 6:
                output_grid[r,c] = 6

    return output_grid