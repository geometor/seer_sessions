"""
The transformation takes each color present in the top row of the input grid, if any, and extends those colors downwards, filling any white (0) cells below, until the bottom of the grid, or another color, is reached.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extending colors in the top row downwards.
    """
    output_grid = np.array(input_grid, dtype=int)  # Ensure we work with a NumPy array for easier manipulation.
    rows, cols = output_grid.shape

    # Iterate through each column.
    for j in range(cols):
        # Find the top-most non-zero color in the current column.
        top_color = 0
        for i in range(rows):
            if output_grid[i, j] != 0:
                top_color = output_grid[i, j]
                break  # Stop searching once the top color is found

        # If a non-zero color was found, propagate it downwards.
        if top_color != 0:
            fill = False
            for i in range(rows):
                if output_grid[i,j] == top_color:
                    fill = True
                if fill:
                    if output_grid[i, j] == 0:
                        output_grid[i, j] = top_color
                    elif output_grid[i,j] != top_color:
                        fill = False


    return output_grid.tolist()