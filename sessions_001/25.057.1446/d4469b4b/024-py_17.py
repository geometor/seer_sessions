"""
The transformation rule operates on a 5x5 input grid and produces a 3x3 output grid. For each 3x3 section of the input, from top-left to bottom right:

1.  **Center Pixel Rule:** If there is one blue (1) in center, then the output pixel will be a gray(5). If more than one blue, consider rule 2.
2. **Corner Rule**: If there is a blue(1) in a corner of a subgrid, it sets the respective corner in the output grid to gray(5).
3. **White Background:** If the input has no blues, the output will be a white (0).

In summary, we are building 3x3 sections that are overlapping.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 5x5 input grid into a 3x3 output grid based on the rules described above.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize output grid with white (0)

    # Iterate through the 3x3 overlapping regions
    for i in range(3):
        for j in range(3):
            # Define the 3x3 region in the input grid
            row_start = i
            row_end = i + 3
            col_start = j
            col_end = j + 3
            
            region = input_grid[row_start:row_end, col_start:col_end]

            # Check for corner rule
            if region[0, 0] == 1:
                output_grid[0,0] = 5
            if region[0, 2] == 1:
                output_grid[0,2] = 5
            if region[2, 0] == 1:
                output_grid[2,0] = 5
            if region[2, 2] == 1:
                output_grid[2,2] = 5

            # Center Pixel Rule
            if np.sum(region == 1) == 1:
                if region[1,1] == 1:
                    output_grid[i,j] = 5


    return output_grid.tolist()