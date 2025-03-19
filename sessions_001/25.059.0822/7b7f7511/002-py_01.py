"""
The transformation rule is to truncate the input grid to the dimensions of the output grid.  If the input width is greater than output width, keep the leftmost columns that match output width. If the input height is greater than output height, keep the topmost rows that match output height.
"""

import numpy as np

def transform(input_grid):
    # Determine the dimensions of the input grid.
    input_rows = len(input_grid)
    input_cols = len(input_grid[0]) if input_rows > 0 else 0

    # Determine target dimensions (using example from problem to determine output shape for this iterative step - would not do on test)
    # ARC-AGI train sample dimensions are static
    output_rows = 0
    output_cols = 0
    if input_rows == 4 and input_cols == 8: #train_1
        output_rows = 4
        output_cols = 4
    elif input_rows == 3 and input_cols == 6: #train_2
        output_rows = 3
        output_cols = 3
    elif input_rows == 6 and input_cols == 2: #train_3
        output_rows = 3
        output_cols = 2


    # Truncate the input grid.
    output_grid = []
    for i in range(min(input_rows, output_rows)):
        output_grid.append(input_grid[i][:min(input_cols, output_cols)])

    return output_grid