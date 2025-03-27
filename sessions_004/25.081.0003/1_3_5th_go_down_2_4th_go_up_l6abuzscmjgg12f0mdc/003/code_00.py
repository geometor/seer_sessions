"""
Transforms an input grid by reflecting its non-zero elements across the main diagonal (top-left to bottom-right). 
If multiple elements map to the same position after reflection, they are stacked vertically in the rows above the reflected position.
The output grid expands to accommodate the stacking of the reflected pixels.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Calculate the expansion required
    expansion = 0
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0 and r > c:
                expansion +=1

    # Initialize the output_grid with expanded size
    output_rows = rows + expansion
    output_grid = np.zeros((output_rows, cols), dtype=int)


    # Iterate through the input grid and reflect non-zero pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                new_r, new_c = c, r

                # check for existing stacked pixels and stack
                if output_grid[new_r,new_c] == 0:
                    output_grid[new_r, new_c] = input_grid[r, c]
                else:
                    # Stack upwards. Find an empty slot above new_r.
                    stack_row = new_r -1
                    while stack_row >= 0 and output_grid[stack_row, new_c] != 0 :
                        stack_row -= 1
                    if stack_row >=0:
                        output_grid[stack_row,new_c] = input_grid[r,c]

    return output_grid.tolist()