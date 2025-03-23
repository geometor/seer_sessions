"""
The transformation rule involves identifying horizontal lines of contiguous pixels of the same color in the input grid, reversing each line, and then placing these reversed lines as columns in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reversing each horizontal line of same-color pixels and placing them as columns in the output grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through each row to identify horizontal lines
    for i in range(rows):
        row = input_grid[i]
        start = 0
        while start < cols:
            end = start
            while end < cols and row[end] == row[start]:
                end += 1
            # Extract the horizontal line
            line = row[start:end]

            # Reverse the line
            reversed_line = line[::-1]

            # Place the reversed line in the corresponding column of the output grid
            for j, pixel in enumerate(reversed_line):
                if i < rows:
                    output_grid[j, i] = pixel

            start = end

    return output_grid.tolist()