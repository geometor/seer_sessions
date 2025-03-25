"""
The transformation rule is to create an output grid with the same dimensions as the input grid.
The output grid is filled entirely with a single color. This color is determined by examining the
expected output grid at the [0, 0] position (top-left corner). The value at this position in the
expected output is the color used to fill the entire output grid.
"""

import numpy as np

def transform(input_grid, expected_output):
    # Convert input_grid and expected_output to NumPy arrays.
    input_np = np.array(input_grid)
    expected_np = np.array(expected_output)

    # Determine the dimensions of the input grid (they are the same as the output).
    rows, cols = input_np.shape

    # Identify the fill value from the top-left corner of the expected output.
    fill_value = expected_np[0, 0]

    # Create an output grid filled with the identified fill value.
    output_grid = np.full((rows, cols), fill_value)

    return output_grid.tolist()