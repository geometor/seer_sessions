"""
Transforms a 3x3 input grid into a 3x3 output grid. The transformation is performed row-by-row.
For each row in the input grid, the color of the corresponding row in the output grid is determined
by the presence and column index of the first '5' found in the input row. Each row has a different
mapping from '5's column index to output row color.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with zeros
    output_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Iterate through rows of input_grid
    for row_index in range(3):
        input_row = input_grid[row_index]
        output_row = [0, 0, 0]  # Initialize with default value

        # Find the first occurrence of '5' in the input row
        five_indices = [i for i, x in enumerate(input_row) if x == 5]
        if five_indices:
            first_five_index = five_indices[0]

            # Determine output row color based on row index and column index of the first '5'
            if row_index == 0:
                if first_five_index == 0:
                    output_row = [2, 2, 2]
                elif first_five_index == 1:
                    output_row = [4, 4, 4]
                elif first_five_index == 2:
                    output_row = [3, 3, 3]
            elif row_index == 1:
                if first_five_index == 1:
                    output_row = [2, 2, 2]
                elif first_five_index == 2:
                    output_row = [3, 3, 3]
            elif row_index == 2:
                if first_five_index == 0:
                    output_row = [3, 3, 3]
                elif first_five_index == 1:
                    output_row = [4, 4, 4]
                elif first_five_index == 2:
                    output_row = [2, 2, 2]

        output_grid[row_index] = output_row

    return output_grid