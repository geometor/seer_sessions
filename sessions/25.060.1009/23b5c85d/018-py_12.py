"""
1.  Identify Magenta Pixels: Locate all pixels with the color value 6 (magenta) within the input grid.
2.  Determine Bounding Box: Find the minimum and maximum row and column indices occupied by the magenta pixels. This defines the smallest rectangular region containing all magenta pixels.
3.  Extract Subgrid: Extract the rectangular subgrid from the *input grid* corresponding to the bounding box. This subgrid includes all pixels (of any color) within the bounding box, not just the magenta ones.
4. Return: return the subgrid
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Identify Magenta Pixels: Create a boolean mask where True indicates magenta pixels.
    magenta_mask = (input_array == 6)

    # Find the coordinates of all magenta pixels.
    magenta_coords = np.argwhere(magenta_mask)

    # If no magenta pixels are found, return an empty grid.
    if magenta_coords.size == 0:
        return []

    # Determine Bounding Box: Find the min and max row and column indices.
    min_row = magenta_coords[:, 0].min()
    max_row = magenta_coords[:, 0].max()
    min_col = magenta_coords[:, 1].min()
    max_col = magenta_coords[:, 1].max()

    # Extract Subgrid: Extract the relevant section from the *input* grid.
    output_grid = input_array[min_row:max_row + 1, min_col:max_col + 1]

    return output_grid.tolist()