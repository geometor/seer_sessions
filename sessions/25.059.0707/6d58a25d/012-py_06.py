"""
1.  **Identify Objects:** Locate all red pixels (value '2') and orange pixels (value '7') within the input grid.
2.  **Preserve Orange Structure:** All the orange '7' in the input grid should be present in the output at the exact position.
3.  **Red Replication:** For every red pixel in the input, create a vertical column in the output. The height of each column will be from row position of that red pixel, down to the bottom of the grid, OR until it hits an orange pixel.
4. **Output Construction:** Place these replicated and the original red pixels, and orange structure into a new grid, preserving the background (value '0') where no other objects are present.

In summary: Copy each red pixel downwards, stopping if an orange pixel is encountered, or the edge of the grid is reached, and keep all orange pixels at original position.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            # Preserve Orange Structure
            if input_grid[r, c] == 7:
                output_grid[r, c] = 7
            # Red Replication
            elif input_grid[r, c] == 2:
                output_grid[r,c] = 2 # preserve original red
                # set current and all lower rows to 2, until orange or bottom
                for r_prime in range(r + 1,rows):
                    if input_grid[r_prime,c] == 7:
                        break # stop at orange
                    output_grid[r_prime, c] = 2

    return output_grid