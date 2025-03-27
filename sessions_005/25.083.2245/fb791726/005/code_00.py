"""
The transformation rule involves doubling the width of the input grid. For each row in the input grid that contains at least one non-zero pixel, the non-zero pixels in the row are copied to a new row in the output grid, maintaining their original color and positions relative to the start of the row. Immediately after this copied row, a row of green pixels is added to the output grid.
"""

import numpy as np

def transform(input_grid):
    # Determine Input Dimensions
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    # Calculate Output Width
    output_width = 2 * input_width

    # Initialize output_grid as a list to dynamically add rows
    output_grid_list = []

    # Iterate through each row of the input
    for row in input_grid:
        # Check if the row contains any non-zero pixels
        if np.any(row != 0):
            # Create a new row with double the width, initialized with zeros
            new_row = np.zeros(output_width, dtype=int)

            # Copy the non-zero pixels to the new row, maintaining original positions
            for i in range(input_width):
                if row[i] != 0:
                    new_row[i] = row[i]

            # Add the new row to the output grid
            output_grid_list.append(new_row)

            # Create a row of green pixels (value 3) with double the width
            green_row = np.full(output_width, 3, dtype=int)

            # Add the green row immediately after the copied row
            output_grid_list.append(green_row)

    # Convert the list of rows to a NumPy array
    output_grid = np.array(output_grid_list)

    return output_grid