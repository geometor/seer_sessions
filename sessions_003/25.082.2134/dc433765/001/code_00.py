"""
1.  **Identify Key Pixels:** Locate all pixels with the value 3 (green) and 4 (yellow) within the input grid.

2.  **Shift Green Left one:** If there is a value 3, shift it one space left. If value is 0 in that space, change it to 3. If there is a value there, do not change it.

3. **Shift all green above:** If there is a value 3, copy it to the row above, in the same column. If there is a value there, do not change it.

4.  **Preserve Other Pixels:** All other pixels, including those with the value 0 (white), remain unchanged in their original positions.

5. **The output grid will shift by 1 unit**: Green moves from under to to yellow, from above to beside.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid to find green (3) and yellow (4) pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 3:
                # Shift green left one, if possible
                if c > 0 and output_grid[r, c-1] == 0:
                    output_grid[r, c-1] = 3
                    if (c+1 >= cols or output_grid[r,c+1] !=0):
                      output_grid[r,c] = 0

                # move green up
                if r > 0 and output_grid[r-1, c] == 0:
                    output_grid[r - 1, c] = 3
                    if (r+1 >= rows or output_grid[r+1,c] != 0):
                        output_grid[r,c] = 0

    return output_grid.tolist()