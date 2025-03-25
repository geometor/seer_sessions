```python
"""
The transformation constructs an output grid where each row of the input grid is reversed, interleaved, and then repeated three times to form three rows in the output. The output grid's height is three times the input's height, and the width is double the input's width. Every third row of output is all black (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with dimensions three times height and two times width of input.
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through input grid rows.
    for i in range(input_height):
        # Get the current input row.
        input_row = input_grid[i]

        # Reverse the input row.
        reversed_row = input_row[::-1]

        # Interleave original and reversed rows.
        interleaved_row = np.empty(output_width, dtype=int)
        interleaved_row[0::2] = input_row
        interleaved_row[1::2] = reversed_row

        # Calculate the starting row index for the output.
        start_row = i * 3

        # Populate three consecutive rows in the output grid.
        output_grid[start_row:start_row + 2, :] = interleaved_row
        output_grid[start_row + 2, :] = np.zeros(output_width, dtype=int) # black row

    return output_grid
```