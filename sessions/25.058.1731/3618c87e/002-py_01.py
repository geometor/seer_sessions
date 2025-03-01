"""
The blue pixels in each column are moved to the bottom row, replacing the gray pixels in the bottom row.
Any gray pixels displaced by blue move up one position.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Identify blue and gray pixels in the current column
        blue_indices = np.where(input_grid[:, j] == 1)[0]
        gray_indices = np.where(input_grid[:, j] == 5)[0]

        # Count the number of blue pixels in the column
        num_blue = len(blue_indices)

        # Move blue pixels to the bottom row, replacing gray
        for i in range(num_blue):
            if rows - 1 - i >= 0:  # Check if the row index is within bounds
              output_grid[rows - 1 - i, j] = 1

        #update grey pixels in column
        if len(gray_indices)>0:
            grey_available = True
            grey_to_move_up = len(gray_indices) - num_blue if len(gray_indices) >= num_blue else 0

            if grey_to_move_up > 0:
                counter = 0
                #move only the grey that have not been replaced.
                for g_idx in gray_indices:
                    if input_grid[g_idx,j] == 5: #still grey in input after blue replaced grey on last row.
                        if g_idx-1 >=0:
                           output_grid[g_idx - 1, j] = 5
                        counter = counter +1
                    if counter == grey_to_move_up:
                        break;
        # remove traces of old blue
        for b_idx in blue_indices:
            output_grid[b_idx,j] = 0

    return output_grid.tolist()