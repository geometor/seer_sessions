"""
Transforms an input grid by propagating colors downwards within each column, starting from the original positions of colors in the input grid. Black (0) acts as an empty space and is not propagated.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid, converting to list for mutability
    output_grid = np.copy(input_grid).tolist()
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each column
    for c in range(cols):
        #find non-zero colors present in current column, order does not matter.
        colors = set()
        for r in range(rows):
           if input_grid[r][c]!=0:
              colors.add(input_grid[r][c])
        #Iterate through rows in column
        for r in range(rows):
            color = input_grid[r][c]
            #propogate if color is not zero
            if color != 0:
                #fill down
                for i in range(r,rows):
                    if output_grid[i][c] == 0 or output_grid[i][c] == color:
                        output_grid[i][c] = color
                    else:
                        break  # Stop propagation if a different non-zero color is encountered



    return output_grid