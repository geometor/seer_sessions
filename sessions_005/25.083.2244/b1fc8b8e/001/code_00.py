"""
The transformation extracts the central 4x4 section of the 6x6 input grid.
Then, it creates a 5x5 output grid with a cross-like pattern of azure (8) pixels,
copying values where the pattern and central section intersect. The rest of the output grid is filled with white (0) pixels.
"""

import numpy as np

def transform(input_grid):
    # Crop the input grid to the central 4x4 region.
    cropped_grid = input_grid[1:5, 1:5]

    # Initialize the 5x5 output grid with all white (0) pixels.
    output_grid = np.zeros((5, 5), dtype=int)
    
    # Define the cross pattern indices (row, col) for azure (8) pixels.
    cross_pattern = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                      (0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
                      (1, 0), (1, 2), (1, 4),
                      (3, 0), (3, 2), (3, 4)]

    # Fill in the output grid: azure for the cross, cropped input values where they match
    for r, c in cross_pattern:
        if 0 <= r < 5 and 0 <= c < 5:  # Boundary check (theoretically always true)
            # if position in pattern and within the central section
            if (r in [1,3] and 0 <= c-1 < 4) or \
               (c in [1,3] and 0 <= r-1 < 4) :
                output_grid[r,c] = cropped_grid[r-1 if r in [1,3] else r, c -1 if c in [1,3] else c]
            else:
                output_grid[r, c] = 8


    return output_grid