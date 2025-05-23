"""
The transformation involves changing the color of each cell based on both its position (specifically, its column) in the grid and its initial color. A column-specific color transformation rule is applied.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Define column-specific color mappings.
    column_mappings = {
        0: {3: 4, 2: 6, 5: 1, 8: 8},
        1: {1: 5, 3: 4, 8: 9},
        2: {2: 6, 8: 9, 2: 2} #2 can map to 6 or 2, priority is based on order in map.
    }

    # Iterate through each pixel of the grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Get the input color and column.
            input_color = input_grid[i, j]
            column = j

            # Apply column-specific mapping.
            if column in column_mappings:
                if input_color in column_mappings[column]:
                    output_grid[i, j] = column_mappings[column][input_color]
                #If input not in mapping, don't change the value.

    return output_grid