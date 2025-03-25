"""
Expand a 3x3 input grid to a 9x9 output grid by replicating the entire input
grid at locations corresponding to non-zero cells in the input.  Each non-zero
cell in the input becomes the center of a 3x3 copy of the original input within
the output.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros((9, 9), dtype=int)  # Initialize 9x9 output

    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] != 0:
                # Calculate the center position in the output grid
                center_row = i * 3 + 1
                center_col = j * 3 + 1

                # Place the 3x3 input grid centered at the calculated position
                for row_offset in range(-1, 2):
                    for col_offset in range(-1, 2):
                        output_row = center_row + row_offset
                        output_col = center_col + col_offset

                        # Check bounds to avoid errors
                        if 0 <= output_row < 9 and 0 <= output_col < 9:
                            input_row = row_offset + 1
                            input_col = col_offset + 1
                            output_grid[output_row, output_col] = input_grid[input_row, input_col]

    return output_grid.tolist()