"""
1. Examine the first column of the input grid.
2. Identify all pixels in this column that are not yellow.
3. Create a new grid. The height and width of this grid will be twice the number of non-yellow pixels found in step 2.
4. Stack the identified non-yellow pixels from the input's first column at the top of the output's first column.
5. Below these, add an equal number of maroon (9) pixels.
6. Fill any remaining cells in the output grid with yellow (4) pixels.
"""

import numpy as np

def transform(input_grid):
    # Extract the first column of the input grid
    first_column = input_grid[:, 0]

    # Identify non-yellow pixels in the first column
    non_yellow_pixels = [pixel for pixel in first_column if pixel != 4]
    num_non_yellow = len(non_yellow_pixels)

    # Calculate the dimensions of the output grid
    output_size = 2 * num_non_yellow
    
    # Initialize the output grid with the calculated dimensions, filled with yellow (4)
    output_grid = np.full((output_size, output_size), 4, dtype=int)


    # Construct the first column of the output grid
    row_index = 0
    # Place non-yellow pixels
    for pixel in non_yellow_pixels:
        output_grid[row_index, 0] = pixel
        row_index += 1

    # Add maroon (9) pixels
    for _ in range(num_non_yellow):
        output_grid[row_index, 0] = 9
        row_index += 1

    return output_grid