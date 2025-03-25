"""
1.  **Initialization:** Create an output grid with a height three times the input grid's height and a width twice the input grid's width. Initialize all its elements to 0 (black).

2.  **Row Iteration:** For each row in the input grid:

    a. **Reverse:** Create a reversed version of the current input row.

    b. **Interleave:** Create an interleaved row by taking elements from the original row and its reversed version. The original row's elements are placed at even indices (0, 2, 4...), and the reversed row's elements at odd indices (1, 3, 5...).

    c. **Placement (Corrected):**
    In the output grid, place the interleaved row at the row index 3 \* (current input row index).
    Place the same interleaved row at row index 3 \* (current input row index) + 1.
    Place the all black row at row index 3 \* (current input row index) + 2.

3.  **Output:** The `output_grid` is the result of the transformation.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each row of the input grid
    for i in range(input_height):
        # Get the current input row
        input_row = input_grid[i]

        # Reverse the input row
        reversed_row = input_row[::-1]

        # Interleave the original and reversed rows
        interleaved_row = np.empty(output_width, dtype=int)
        interleaved_row[0::2] = input_row
        interleaved_row[1::2] = reversed_row

        # Calculate the starting row index for the output
        start_row = i * 3

        # Place the interleaved row twice and a black row once
        output_grid[start_row, :] = interleaved_row
        output_grid[start_row + 1, :] = interleaved_row
        output_grid[start_row + 2, :] = np.zeros(output_width, dtype=int)

    return output_grid