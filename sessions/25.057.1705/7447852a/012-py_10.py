"""
1.  **Identify Red Pixels:** Locate all pixels with the color red (value 2) in the input grid.

2.  **Rightward Adjacency Check:** For each red pixel, check if there's a white pixel (value 0) immediately to its right.

3.  **Conditional Change:** If a white pixel is found to the right of a red pixel, change that white pixel to yellow (value 4).

4.  **Preserve Other Pixels:** All other pixels, including red pixels and white pixels not directly to the right of a red pixel, remain unchanged.

5.  **Output:** The resulting grid is the output, containing potentially modified yellow pixels based on the rightward adjacency rule.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:  # Find red pixels
                # Check adjacency to the right
                if c < cols - 1 and input_grid[r, c+1] == 0:
                    output_grid[r, c+1] = 4  # Change adjacent white pixel to yellow

    return output_grid