"""
1. Identify Target Color: Focus on pixels with the color value 6 (magenta).
2. Isolate Target Pixels: Disregard all pixels that are not magenta.
3. Construct Bounding Grid: Create the smallest possible rectangular grid that contains all the magenta pixels, removing any completely empty rows or columns that resulted from removing the non-magenta pixels.
4. Output: Return the resulting condensed grid of only magenta pixels.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Isolate Target Pixels: Create a boolean mask where True indicates magenta pixels.
    magenta_mask = (input_array == 6)

    # Find the coordinates of all magenta pixels.
    magenta_coords = np.argwhere(magenta_mask)

    # If no magenta pixels are found, return an empty grid or a specific default value.
    if magenta_coords.size == 0:
        return []  # Or any other suitable default, like np.zeros((0,0))

    # Construct Bounding Grid: Find the min and max row and column indices to determine the bounding rectangle.
    min_row = magenta_coords[:, 0].min()
    max_row = magenta_coords[:, 0].max()
    min_col = magenta_coords[:, 1].min()
    max_col = magenta_coords[:, 1].max()

    # Extract the relevant section from the magenta mask using array slicing.
    output_grid = magenta_mask[min_row:max_row + 1, min_col:max_col + 1]
    
    # convert boolean output to integer grid of just magenta
    output_grid = output_grid.astype(int) * 6

    return output_grid.tolist()