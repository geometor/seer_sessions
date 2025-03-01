"""
1.  **Identify Azure:** Locate the single azure (8) pixel in the input grid.
2.  **Target Row:** Identify the row that contains the azure pixel.
3.  **Fill with Black:** Change all pixels in the target row to black (0).
4.  **Preserve Azure:** Ensure the azure pixel's location and color remain unchanged.
"""

import numpy as np

def find_pixel(grid_np, color):
    """Finds the location of a pixel of the given color.  Assumes only one exists."""
    locations = np.argwhere(grid_np == color)
    if len(locations) > 0:
        return locations[0]  # Return the first location found
    return None

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    input_np = np.array(input_grid)
    rows, cols = input_np.shape
    output_np = input_np.copy() # start with a copy, to preserve the azure pixel

    # 1. Identify Azure and 2. Target Row
    azure_location = find_pixel(input_np, 8)
    if azure_location is None:
        return output_np.tolist() # No azure pixel, return input unchanged

    target_row = azure_location[0]

    # 3. Fill with Black (and implicitly 4. Preserve Azure)
    for c in range(cols):
        output_np[target_row, c] = 0

    return output_np.tolist()