"""
1.  **Initialization:** Begin with the output grid being an exact copy of the input grid.

2.  **Blue Pixel Identification:** Iterate through each pixel of the *input* grid. Identify pixels that are blue (color value 1).

3.  **3x3 Pattern Application:** For *each* blue pixel found:
    *   Overwrite the corresponding pixel in the *output* grid with a '1' (blue).
    *   If possible (i.e., not exceeding grid boundaries), set pixels in the *output* grid relative to the blue pixel's location as follows:
        *   One pixel up and one pixel to the left: set to 2 (red).
        *   One pixel up: set to 7 (orange).
        *   One pixel up and one pixel to the right: set to 6 (magenta).
        *   One pixel to the left: set to 8 (gray).

4. **Pixels Not Modified:** If a pixel is not part of the 3x3 transformation triggered by any blue pixel in the input, the output retains its input value.

5. **Overlapping Transformations:** If multiple blue pixels trigger transformations that would modify the same location, the transformation associated with the final processed blue applies.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)  # Initialize with a copy of input

    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:  # Blue pixel found
                # Apply 3x3 transformation, overwriting existing pixels
                if r > 0 and c > 0:
                    output_grid[r-1, c-1] = 2  # Top-left
                if r > 0:
                    output_grid[r-1, c] = 7  # Top-center
                if r > 0 and c < cols - 1:
                    output_grid[r-1, c+1] = 6  # Top-right
                if c > 0:
                    output_grid[r, c-1] = 8  # Left-center
                output_grid[r, c] = 1  # Center remains blue

    return output_grid