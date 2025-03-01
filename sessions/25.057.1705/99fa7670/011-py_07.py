"""
1.  **Identify Magenta Pixels:** Locate all pixels with the color value 6 (magenta) in the input grid.
2.  **Duplicate to the Right:** For each magenta pixel found, create a new magenta pixel immediately to its right in the output grid.
3.  **Preserve Original:** The original magenta pixel remains in its input position in the output.
4. **Preserve Other Pixels** All other pixels that are not magenta are not changed.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input_grid
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is magenta (color 6)
            if input_grid[r, c] == 6:
                # Duplicate magenta pixel to the right if within bounds
                if c + 1 < cols:
                    output_grid[r, c+1] = 6

    return output_grid