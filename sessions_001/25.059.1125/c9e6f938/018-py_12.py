"""
1.  **Locate Orange Pixel:** Find the coordinates (row, column) of the orange pixel (value 7) within the input grid.
2.  **Determine Extension Amount:** Calculate the amount the grid will be extended. This equals `input_width - 1 - original_column`.
3.  **Create Extended Grid:** Create a new output grid. Its height matches the row of the orange pixel (or is adjusted as needed to include the mirrored position if the mirror is on row 0 of output).  Its width is equal to `input_width + (2 * extension_amount)`. This is equivalent to doubling the width, as observed.
4.  **Copy Original Orange Pixel:**  Place an orange pixel (7) in the output grid at the same position as in the input grid.
5. **Mirror Orange Pixel:** Place an orange pixel at the original row number and a column number calculated by adding the extension amount to the `input_width - 1`. This ensures the correct mirrored position relative to the original grid's boundaries. In the cases where there isn't a row 0, then the mirrored pixel will be placed in row 0.
6.  **Fill Remaining Cells:** All other cells in the output grid are filled with white (0).
"""

import numpy as np

def find_orange_pixel(grid):
    # Find the coordinates of the orange pixel (value 7).
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 7:
                return r, c
    return None

def transform(input_grid):
    # Locate Orange Pixel
    orange_pixel_coords = find_orange_pixel(input_grid)
    if orange_pixel_coords is None:
      return input_grid # Should not happen, based on problem definition
    original_row, original_col = orange_pixel_coords

    # Determine Extension Amount
    input_width = input_grid.shape[1]
    extension_amount = input_width - 1 - original_col

    # Create Extended Grid
    new_width = input_width + (2 * extension_amount)
    new_height = max(input_grid.shape[0], 1 if original_row != 0 else input_grid.shape[0]) # accommodate row 0 mirroring
    output_grid = np.zeros((new_height, new_width), dtype=int)


    # Copy Original Orange Pixel
    output_grid[original_row, original_col] = 7

    # Mirror Orange Pixel
    mirrored_row = 0 if original_row !=0 else original_row
    mirrored_col = input_width -1 + extension_amount
    output_grid[mirrored_row, mirrored_col] = 7


    # Fill Remaining Cells (already done by initialization)

    return output_grid