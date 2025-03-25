```python
"""
1.  **Expansion:** Each pixel in the input grid is transformed into a 2x2 block of pixels in the output grid.

2.  **Marker:** The top-left pixel of each 2x2 block is *always* set to azure (8).

3. **Zero Fill**:
    - The top-right pixel of each 2x2 block is set to black (0).
    - The bottom-left pixel of each 2x2 block is set to black (0).

4.  **Original Value Replication/Zero Preservation:**
    - If the original input pixel is *not* zero, the bottom-right pixel of the 2x2 block is set to the original pixel's value.
    - If the original input pixel *is* zero, the bottom right pixel of the 2x2 block remains zero (is not modified from the initialization).
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # Double Dimensions: Calculate output grid dimensions.
    output_height = input_height * 2
    output_width = input_width * 2

    # initialize output_grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid.
    for i in range(input_height):
        for j in range(input_width):
            # 2x2 Block Transformation: Determine the corresponding 2x2 block in the output.
            row_start = i * 2
            col_start = j * 2

            # Marker Pixel Placement: Set the top-left pixel of the 2x2 block to azure.
            output_grid[row_start, col_start] = 8

            # Zero Fill: top-right and bottom-left pixels of the 2x2 block are *always* set to 0.
            output_grid[row_start, col_start + 1] = 0  # Top-right
            output_grid[row_start + 1, col_start] = 0  # Bottom-left

            # Original value replication / Zero Preservation:
            if input_grid[i, j] != 0:
                output_grid[row_start + 1, col_start + 1] = input_grid[i, j]

    return output_grid
```
