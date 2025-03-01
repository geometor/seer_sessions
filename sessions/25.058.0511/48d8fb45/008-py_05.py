"""
1.  **Identify Target Pixels:** Locate all yellow (4) pixels within the input grid.
2.  **Determine Bounding Box:** find the minimum bounding rectangle, this means finding the top-most, left-most, bottom-most and right most yellow pixels.
3.  **Extract Sub-grid:** Extract the region defined by top-most, left-most, bottom-most and right-most rows and columns.
4. return the cropped grid
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)

    # Find coordinates of all yellow pixels (value 4)
    yellow_pixels = np.argwhere(input_array == 4)

    # If no yellow pixels are found, return an empty grid or handle appropriately
    if yellow_pixels.size == 0:
        return np.zeros((0, 0), dtype=int).tolist()

    # Determine the bounding box
    min_row = yellow_pixels[:, 0].min()
    max_row = yellow_pixels[:, 0].max()
    min_col = yellow_pixels[:, 1].min()
    max_col = yellow_pixels[:, 1].max()
   
    # Extract the sub-grid
    output_array = input_array[min_row:max_row+1, min_col:max_col+1]

    return output_array.tolist()