"""
Examine the input grid. Find the center pixel. Determine if all pixels in the grid are the same value as the center pixel. If all pixels are the same color as the center, create a 1x1 output grid containing the center pixel's color. If not all the pixels have the same value, create a 1x1 output grid containing a blue pixel (1).
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    
    # get center pixel
    center_pixel = input_array[rows//2, cols//2]

    # check if all pixels are the same as the center pixel
    all_same_color = np.all(input_array == center_pixel)

    # Create output grid
    if all_same_color:
        output_grid = np.array([[center_pixel]])
    else:
        output_grid = np.array([[1]])

    return output_grid.tolist()