import numpy as np

"""
Accept the input grid as a two-dimensional array.
Create a new output grid of the same dimensions as the input grid.
Iterate through each cell of the input grid, identified by its row index r and column index c.
For each input cell at (r, c), take its value.
Place this value into the output grid at the position (c, r) (swapping the row and column indices).
After iterating through all input cells, the output grid contains the transformed result. Return the output grid.
This operation is equivalent to a matrix transpose.
"""

def transform(input_grid):
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Perform the matrix transpose operation.
    # This swaps the rows and columns: the element at input[r][c] moves to output[c][r].
    output_array = input_array.T

    # Convert the resulting NumPy array back to a list of lists format if required
    # (often the case in these challenges)
    output_grid = output_array.tolist()

    return output_grid