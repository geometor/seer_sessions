"""
1.  **Identify Boundary:** Find all pixels with the colors blue (1) and azure (8) within the input grid.
2.  **Determine Bounding Box:**  Calculate the minimum and maximum row and column indices of these blue and azure pixels. This defines a rectangular bounding box.
3.  **Extract Subgrid:** Create a new grid that is a copy of the section of the *original input grid* that falls *within* the bounding box.  This includes *all* colors present in that region, not only the blues and azures.
4. **Output:** The new, cropped grid is the output.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # find all blue and azure cells
    blue_azure_indices = np.where((input_grid == 1) | (input_grid == 8))
    #blue_azure_coords = list(zip(blue_azure_indices[0], blue_azure_indices[1])) # Not needed

    # compute the minimum bounding box
    min_row = np.min(blue_azure_indices[0])
    max_row = np.max(blue_azure_indices[0])
    min_col = np.min(blue_azure_indices[1])
    max_col = np.max(blue_azure_indices[1])

    # Extract the subgrid using array slicing.  This copies ALL elements
    # within the bounding box.
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid