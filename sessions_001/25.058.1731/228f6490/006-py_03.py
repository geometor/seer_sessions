"""
1.  **Locate:** Find all azure (8) and magenta (6) pixels within the input grid.
2.  **Record:** Store the original positions of the azure and magenta pixels.
3.  **Swap:** For *each* azure pixel, move it to the location of a corresponding magenta pixel. Simultaneously, set the azure pixel's *original* location to white (0).
4. **Swap 2:** For *each* magenta pixel, move it to the location of a corresponding azure pixel. Simultaneously, set the magenta pixel's *original* location to white (0).
5. **Preserve** All other pixels not involved in step 3 or 4 remain at their original color.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    
    # 1. & 2. Locate and Record
    azure_pixels = find_pixels(input_grid, 8)
    magenta_pixels = find_pixels(input_grid, 6)

    # Check if we have exactly two of each
    if len(azure_pixels) != 2 or len(magenta_pixels) != 2:
        return output_grid  # Or raise an exception, depending on desired behavior.

    azure_orig_pos = azure_pixels.copy()
    magenta_orig_pos = magenta_pixels.copy()

    # 3. Swap azure and set original azure positions to 0.
    for i in range(2):
        output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1]] = 8
        output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 0

    # 4. Swap magenta and set original magenta positions to 0.
    for i in range(2):
        output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 6
    
    for i in range(2):
        output_grid[magenta_orig_pos[i][0] , magenta_orig_pos[i][1]] = 0

    return output_grid