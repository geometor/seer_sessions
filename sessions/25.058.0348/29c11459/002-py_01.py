"""
1.  **Identify Key Pixels:** Locate the non-zero pixels on the second row of the input grid. In this case these pixels are blue (1) and red (2).
2.  **Find Center:** Determine the horizontal center column of the grid. In the 11 column example, that column is 5 (starting index 0).
3.  **Insert Center Pixel**: insert a gray pixel (5) in the center column of the second row of the output grid.
4.  **Expand Left:** Working outwards from the center of the second row of the input, going *left*, replace all the zeros in the output with the value of the original blue pixel. Stop before hitting another non zero entry.
5.  **Expand Right:** Working outwards from the center of the second row of the input, going *right*, replace all the zero in the output with the value of the original red pixel. Stop before hitting another non zero entry.
6.  **Copy other rows:** All other rows in the input grid remain unchanged in the output grid.
"""

import numpy as np

def get_non_zero_pixels(row):
    #returns the index of the non-zero pixels in a row
    return np.nonzero(row)[0]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_col = cols // 2

    # Identify non-zero pixels in the second row (index 1)
    second_row = input_grid[1]
    non_zero_indices = get_non_zero_pixels(second_row)


    # Insert Center Pixel
    output_grid[1, center_col] = 5

    # Expand Left
    if len(non_zero_indices)>0:
        left_pixel_val=input_grid[1,non_zero_indices[0]]
        for i in range(center_col - 1, -1, -1):
            if output_grid[1,i]==0:
                output_grid[1, i] = left_pixel_val
            else:
                break


        # Expand Right
        right_pixel_val = input_grid[1,non_zero_indices[-1]]
        for i in range(center_col + 1, cols):
            if output_grid[1,i] == 0:
                output_grid[1, i] = right_pixel_val
            else:
                break


    return output_grid