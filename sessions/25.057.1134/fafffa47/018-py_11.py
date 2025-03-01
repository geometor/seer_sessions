"""
1.  **Identify Maroon Pixels**: Locate all pixels colored maroon (9) in the input grid.
2.  **Bounding Box**: Determine the smallest rectangular bounding box that encompasses all maroon pixels. The bounding box is defined by `(min_row, max_row, min_col, max_col)` of the maroon pixels' coordinates.
3. **Subgrid Extraction**: Extract a subgrid from the input.
    * if the bounding box has a height and width greater than 0, the subgrid is the region defined by the bounding box
    * if the bounding box has a height and width of zero (all maroon pixels occupy the same location) then the subgrid has a height and width of 1 and represents that location
4.  **Color Transformation**: Within this extracted subgrid, change the color of all maroon (9) pixels to red (2).
5. **Output**: Return the modified subgrid as the output.
"""

import numpy as np

def _find_maroon_pixels_and_bounding_box(grid):
    """finds all maroon pixels and determine a bounding box around it"""
    maroon_pixels = np.argwhere(grid == 9)
    if maroon_pixels.size == 0:
        return None  # Or handle the case of no maroon pixels appropriately

    min_row = maroon_pixels[:, 0].min()
    max_row = maroon_pixels[:, 0].max()
    min_col = maroon_pixels[:, 1].min()
    max_col = maroon_pixels[:, 1].max()

    bounding_box = (min_row, max_row, min_col, max_col)
    return bounding_box

def transform(input_grid):
    # Find the bounding box of maroon pixels
    bounding_box = _find_maroon_pixels_and_bounding_box(input_grid)

    # Handle the case where no maroon pixels are found
    if bounding_box is None:
        return input_grid.copy()  # Or some other default behavior

    min_row, max_row, min_col, max_col = bounding_box

    # Extract the subgrid based on bounding box size.
    if (max_row - min_row > 0) or (max_col - min_col > 0):
        output_grid = input_grid[min_row:max_row+1, min_col:max_col+1].copy()
    else:
         output_grid = input_grid[min_row:min_row+1, min_col:min_col+1].copy()

    # Transform maroon pixels to red within the subgrid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 9:
                output_grid[i, j] = 2

    return output_grid