import numpy as np
from typing import List, Set, Tuple

"""
Transforms an input grid of integers by upscaling it based on the number of unique integers present.

1.  Parse the input list of lists into a NumPy array `input_np`.
2.  Find all unique integer values present within `input_np`.
3.  Count the number of these unique values to determine the scaling factor, `S`.
4.  If `S` is 1, return the original input grid as no scaling is needed.
5.  Get the dimensions of `input_np`: `input_rows` and `input_cols`.
6.  Calculate the dimensions for the `output_grid`: `output_rows = input_rows * S` and `output_cols = input_cols * S`.
7.  Create a new NumPy array `output_np` with the calculated `output_rows` and `output_cols`, using the same data type as the input.
8.  Iterate through each cell of `input_np` using its row index `r` (from 0 to `input_rows - 1`) and column index `c` (from 0 to `input_cols - 1`).
9.  For each input cell `input_np[r, c]`, get its integer value `v`.
10. Identify the target block in `output_np`: this block covers rows from `r * S` to `(r * S) + S - 1` and columns from `c * S` to `(c * S) + S - 1`.
11. Fill every cell within this target block in `output_np` with the value `v`.
12. After processing all cells from `input_np`, convert `output_np` back into a standard Python list of lists.
13. Return the resulting list of lists.
"""


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Upscales an input grid based on the count of its unique elements.

    Args:
        input_grid: A list of lists representing the 2D input grid of integers.

    Returns:
        A list of lists representing the upscaled 2D output grid.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_np = np.array(input_grid, dtype=int)

    # Find unique values in the input grid
    unique_values: np.ndarray = np.unique(input_np)

    # Determine the scaling factor based on the number of unique values
    scaling_factor: int = len(unique_values)

    # If scaling factor is 1, the output is identical to the input
    if scaling_factor == 1:
        # Return the original list of lists format
        return input_grid

    # Get the dimensions (rows, columns) of the input grid
    input_rows: int
    input_cols: int
    input_rows, input_cols = input_np.shape

    # Calculate the dimensions of the output grid
    output_rows: int = input_rows * scaling_factor
    output_cols: int = input_cols * scaling_factor

    # Create the output grid (NumPy array), initialized with zeros or empty
    # Using the same dtype as the input is important
    output_np = np.zeros((output_rows, output_cols), dtype=input_np.dtype)

    # Iterate through each cell of the input grid
    for r in range(input_rows):
        for c in range(input_cols):
            # Get the value from the current input cell
            value: int = input_np[r, c]

            # Calculate the starting row and column index for the block in the output grid
            row_start: int = r * scaling_factor
            col_start: int = c * scaling_factor

            # Calculate the ending row and column index for the block (exclusive)
            row_end: int = row_start + scaling_factor
            col_end: int = col_start + scaling_factor

            # Fill the corresponding S x S block in the output grid with the value
            output_np[row_start:row_end, col_start:col_end] = value

    # Convert the final NumPy array back to a list of lists
    output_grid: list[list[int]] = output_np.tolist()

    return output_grid
