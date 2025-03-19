"""
The transformation rule involves simplifying a 7x7 input grid into a 3x3 output grid. The input grid contains white (0) and red (2) pixels. The output grid contains white (0) and blue (1) pixels. The output represents a simplified version of the input, where each cell in the 3x3 output indicates the presence (blue) or absence (white) of red pixels within a corresponding region of the 7x7 input.
"""

import numpy as np

def transform(input_grid):
    # Initialize the 3x3 output grid with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Define the size of the regions in the input grid
    # 7 / 3 = ~2.33. Regions will be 2 or 3 rows/cols.
    row_splits = [2, 5]  # 0:2, 2:5, 5:7
    col_splits = [2, 5]  # 0:2, 2:5, 5:7
    
    # Iterate through each region of input and corresponding cell of output
    for i, row_start in enumerate([0] + row_splits):
        row_end = row_splits[i] if i < len(row_splits) else 7
        for j, col_start in enumerate([0] + col_splits):
            col_end = col_splits[j] if j < len(col_splits) else 7
            
            # Extract region
            region = input_grid[row_start:row_end, col_start:col_end]
            
            # Check for presence of "ink" (non-white, i.e., red pixels)
            if np.any(region != 0):
                output_grid[i, j] = 1  # Set to blue (1)

    return output_grid