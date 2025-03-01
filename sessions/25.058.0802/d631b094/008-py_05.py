"""
1.  **Identify** all pixels with the value '2' (red) in the input grid.
2.  **Extract** and Collect those pixels.
3.  Create new grid one row high and the number of columns is the count of pixels.
4. **Discard** all other pixels
"""

import numpy as np

def transform(input_grid):
    # Extract all pixels with value '2' (red)
    red_pixels = []
    for row_idx, row in enumerate(input_grid):
        for col_idx, pixel in enumerate(row):
            if pixel == 2:
                red_pixels.append(pixel)

    # Create a new grid with dimensions based on the count of red pixels
    if len(red_pixels) >0:
        output_grid = np.full((1, len(red_pixels)), 2)
    else:
       output_grid = np.array([[0]]) #If no red, should be background
    return output_grid