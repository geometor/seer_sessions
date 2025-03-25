"""
Replace all occurrences of colors blue(1), red(2), green(3), and azure(8) with grey(5) in the grid. Leave all other colors unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Define the trigger colors that will be replaced
    trigger_colors = [1, 2, 3, 8]

    # Iterate through each cell of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the current cell's value is in the trigger_colors list
            if output_grid[i, j] in trigger_colors:
                # Change the cell's value to 5 (grey)
                output_grid[i, j] = 5

    return output_grid