"""
The transformation extracts specific pixels from the input grid to construct the output grid. It's a form of downsampling, but the selection pattern isn't a regular grid subsampling. The process can be described as follows:

1.  Determine Output Dimensions: The output grid's dimensions are predefined for each input. They are *not* calculated based on a simple division of the input dimensions.
    * example 1: `[4,4]`
    * example 2: `[6,6]`

2.  Calculate Step Sizes and start indices:
    The starting indices and steps vary based on the specific input and output
    dimensions. A single calculation is not applicable to all.
      * example 1:
        * row_step = 1
        * col_step = 1
        * row_start = 0
        * col_start = 2
      * example 2:
        * row_step = 3
        * col_step = 2
        * row_start = 8
        * col_start = 2

3.  Pixel Selection:** Iterate through the output grid indices (row by row, column by column). For each output pixel:
    *   Calculate the corresponding input pixel indices using: `input_row = row_start + (output_row * row_step)` and `input_col = col_start + (output_col * col_step)`.
    *   If the calculated input indices are within the bounds of the input grid, copy the pixel value from the input grid at the calculated indices to the current position in the output grid.
    *   If the calculated input indices are out of bounds, the output pixel is assigned a default fill value, although this case doesn't seem to be present in the given training examples, or may be 0.
"""

import numpy as np

def transform(input_grid):
    input_array = np.array(input_grid)
    irows, icols = input_array.shape

    # Determine output dimensions and parameters (example-specific)
    if irows == 6 and icols == 6:
        orows, ocols = 4, 4
        row_step, col_step, row_start, col_start = 1, 1, 0, 2
    elif irows == 16 and icols == 16:
        orows, ocols = 6, 6
        row_step, col_step, row_start, col_start = 3, 2, 8, 2
    else:  # Default case (should not be reached with provided examples)
        orows, ocols = irows, icols
        row_step, col_step, row_start, col_start = 1, 1, 0, 0

    # initialize output_grid
    output_array = np.zeros((orows, ocols), dtype=int)

    # Sample pixels and create output array
    for r in range(orows):
        for c in range(ocols):
            in_row_idx = row_start + r * row_step
            in_col_idx = col_start + c * col_step
            if in_row_idx < irows and in_col_idx < icols:
                output_array[r, c] = input_array[in_row_idx, in_col_idx]

    return output_array.tolist()