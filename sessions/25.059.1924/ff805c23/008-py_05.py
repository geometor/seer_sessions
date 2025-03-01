"""
Identify the smallest subgrid containing all pixels of color 0 and 3 in the input grid.
Resize this subgrid to 5x5, centering it within the output grid.
The output grid is the resized 5x5 subgrid, keeping only the 0 and 3 pixels, and setting others to 0.
"""

import numpy as np

def get_subgrid(input_grid):
    # Find coordinates of pixels with color 0 or 3
    coords = np.where((input_grid == 0) | (input_grid == 3))
    if len(coords[0]) > 0:
        # Find min and max row/col to define the subgrid
        min_row, min_col = np.min(coords, axis=1)
        max_row, max_col = np.max(coords, axis=1)
        subgrid = input_grid[min_row:max_row + 1, min_col:max_col + 1]
        return subgrid, min_row, min_col
    else:
        return np.array([]), -1, -1  # Return empty array if no 0 or 3 pixels

def transform(input_grid):
    # Get the subgrid containing all 0 and 3 pixels
    subgrid, _, _ = get_subgrid(input_grid)

    # Initialize a 5x5 output grid filled with 0s
    output_grid = np.zeros((5, 5), dtype=int)

    if subgrid.size > 0:  # Check if subgrid is not empty
        # Calculate centering offsets
        row_offset = (5 - subgrid.shape[0]) // 2
        col_offset = (5 - subgrid.shape[1]) // 2

        # Iterate through the subgrid and copy 0 and 3 pixels to output_grid with centering
        for i in range(subgrid.shape[0]):
            for j in range(subgrid.shape[1]):
                if subgrid[i, j] == 0 or subgrid[i, j] == 3:
                    #check if within output grid boundary
                    if 0 <= i + row_offset < 5 and 0 <= j + col_offset < 5:
                      output_grid[i + row_offset, j + col_offset] = subgrid[i, j]

    return output_grid