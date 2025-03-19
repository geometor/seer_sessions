"""
The transformation rule can be summarized as follows:

1.  **Color Check:** Iterate through each pixel of the input grid.
2.  **Conditional Replacement:**
    *   If a pixel is grey (5), change it to white (0).
    *   Otherwise, keep the original color.
3. **Output**: The final output grid contains the modified pixel values.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel and replace 5 with 0.
    output_grid[output_grid == 5] = 0

    return output_grid