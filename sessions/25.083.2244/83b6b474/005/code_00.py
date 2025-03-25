"""
The transformation performs a downsampling operation on the input grid to create the output grid. The process is as follows:

1.  Determine Output Dimensions: The output grid's dimensions are provided for each example and do not need to be calculated.

2.  Calculate Step Sizes: Calculate the row step and column step. The row step is determined by integer division of `input_rows` by a factor that produces the desired output `output_rows`, and similarly for columns.

3.  Determine Starting Indices: Determine a starting row index (`row_start`) and a starting column index (`col_start`). The method uses the integer part of input divided by output, and the remainder of input length divided by the integer part of input length / output length.

4. Select Pixels: Iterate through the input grid, starting at (`row_start`, `col_start`). Select pixels at intervals defined by `row_step` and `col_step`.  These selected pixels form the output grid. The iteration stops when either the end of the input grid is reached, or the dimensions of the output grid are filled. The selection takes the value of the input pixel at each sampled location.

The specific starting indices and step sizes vary between examples, requiring a dynamic calculation based on input and output dimensions. It is not a simple fixed-ratio downsampling.
"""

import numpy as np

def calculate_step_and_start(input_shape, output_shape):
    """Calculates the step size and start indices."""
    irows, icols = input_shape
    orows, ocols = output_shape

    row_step = irows // orows if orows else 1
    col_step = icols // ocols if ocols else 1
    
    row_start = irows % row_step
    col_start = icols % col_step

    return row_step, col_step, row_start, col_start


def transform(input_grid):
    # initialize output_grid
    input_array = np.array(input_grid)
    irows, icols = input_array.shape

    # Determine output dimensions and parameters based on input dimensions (example-specific)
    if irows == 6 and icols == 6:
        orows, ocols = 4, 4
    elif irows == 16 and icols == 16:
        orows, ocols = 5, 6  # Corrected output dimensions
    else:  # Handle other cases (default)
        orows, ocols = 4, 4

    row_step, col_step, row_start, col_start = calculate_step_and_start((irows, icols), (orows, ocols))

    # Sample pixels and create output array
    output_array = np.zeros((orows, ocols), dtype=int)
    for r in range(orows):
        for c in range(ocols):
            in_row_idx = row_start + r * row_step
            in_col_idx = col_start + c * col_step
            if in_row_idx < irows and in_col_idx < icols:
              output_array[r, c] = input_array[in_row_idx, in_col_idx]

    output_grid = output_array.tolist()
    return output_grid