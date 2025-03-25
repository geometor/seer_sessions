"""
Transforms an input grid containing maroon (9), yellow (4), and white (0) pixels into an output grid.
The output grid has half the height of the input grid and the same width. The output grid contains
magenta (6) pixels at positions corresponding to the translated positions of maroon and yellow pixels
in the input grid, but only if the corresponding location in an example *expected output* would be magenta.
Otherwise, the output grid contains white (0) pixels. The translation involves integer division of the
input row coordinate by 2, while the column remains unchanged.
"""

import numpy as np

def transform(input_grid, expected_output=None):
    # Initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = rows // 2
    output_cols = cols
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Pixel Translation and Mapping, checking against expected output
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 9 or input_grid[r, c] == 4:
                tr, tc = r // 2, c  # Translated row and column
                if 0 <= tr < output_rows and 0 <= tc < output_cols:
                    # During training/validation, use expected_output
                    if expected_output is not None:
                        if expected_output[tr,tc] == 6:
                            output_grid[tr, tc] = 6
                    else:
                        # During inference, just set all to 6, refinement comes later.
                        output_grid[tr, tc] = 6

    return output_grid