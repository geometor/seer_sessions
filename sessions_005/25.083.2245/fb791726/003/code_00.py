"""
The transformation rule involves doubling the width of the input grid. For each row in the input grid that contains at least one non-zero pixel, the pixels in the row are copied to the output grid, and a row of green pixels is added immediately below the copied row in the output grid. The copied pixels maintain their original color.
"""

import numpy as np

def transform(input_grid):
    # Determine Input Dimensions
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Calculate Output Dimensions
    output_width = 2 * input_width

    # Initialize output_grid
    # we will determine height dynamically

    output_grid_list = []

    # Iterate through each row of input
    for row in input_grid:
        # Check if row contains non zero pixels
        if np.any(row != 0):
            # if so, copy the row, shifted to the left of output
            new_row = np.zeros(output_width, dtype=int)
            for i in range(len(row)):
                if row[i] !=0:
                  new_row[i] = row[i]

            output_grid_list.append(new_row)

            # Add green row
            green_row = np.full(output_width, 3, dtype=int)
            output_grid_list.append(green_row)

    # Convert to numpy array
    output_grid = np.array(output_grid_list)

    return output_grid