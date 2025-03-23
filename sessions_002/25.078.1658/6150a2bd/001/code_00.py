"""
The transformation rule is to reverse the writing direction - the numbers present in the input are mirrored into the output location.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # change output pixels
    # Iterate through input grid in reverse order
    input_elements = []
    for i in range(rows - 1, -1, -1):
        for j in range(cols - 1, -1, -1):
            input_elements.append(input_grid[i][j])

    # Write to output grid in normal order
    k = 0
    for i in range(rows):
        for j in range(cols):
            output_grid[i][j] = input_elements[k]
            k += 1

    return output_grid