"""
The color of the top-right cell propagates downwards, replacing other cell's value.
If other non-zero colors are encountered, they also propagate downwards.
White (0) cells remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Identify the source color from the top-right cell
    source_color = input_grid[0][-1]

    # Iterate through each column
    for col in range(cols):
        # Propagate the source color downwards
        for row in range(rows):
            if output_grid[row][col] == 0:
                continue          
            else:
                source_color = output_grid[row][col] # get current cell's color
                for r in range(row, rows):           # loop remaining rows
                    output_grid[r][col] = source_color  # propogate down

    return output_grid