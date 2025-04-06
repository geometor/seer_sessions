"""
Transforms an input grid based on a comparison rule applied across a central separator column.

1.  Identifies a central vertical column in the input grid consisting solely of the digit '1'.
2.  Splits the input grid into a 'Left Grid' (columns left of the separator) and a 'Right Grid' (columns right of the separator).
3.  Creates an 'Output Grid' with dimensions matching the Left/Right Grids.
4.  For each cell position (r, c) in the Output Grid:
    - Compares the corresponding digits in the Left Grid and Right Grid at (r, c).
    - If both digits are 0, the Output Grid cell (r, c) is set to 8.
    - Otherwise, the Output Grid cell (r, c) is set to 0.
"""

import numpy as np
from typing import List

def find_separator_column(grid: np.ndarray) -> int:
    """Finds the index of the column containing only 1s."""
    num_rows, num_cols = grid.shape
    for c in range(num_cols):
        if np.all(grid[:, c] == 1):
            return c
    raise ValueError("Separator column (all 1s) not found in the input grid.")

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_array.shape

    # Find the separator column index
    separator_col_index = find_separator_column(input_array)

    # Extract the left and right subgrids
    left_subgrid = input_array[:, :separator_col_index]
    right_subgrid = input_array[:, separator_col_index + 1:]

    # Ensure left and right subgrids have the same dimensions
    if left_subgrid.shape != right_subgrid.shape:
        raise ValueError("Left and right subgrids must have the same dimensions.")

    # Initialize the output grid with zeros, matching the subgrid dimensions
    output_rows, output_cols = left_subgrid.shape
    output_array = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through each cell position corresponding to the subgrids
    for r in range(output_rows):
        for c in range(output_cols):
            # Get the values from the left and right subgrids
            left_value = left_subgrid[r, c]
            right_value = right_subgrid[r, c]

            # Apply the transformation rule: 8 if both are 0, else 0
            if left_value == 0 and right_value == 0:
                output_array[r, c] = 8
            # else: output_array[r, c] remains 0 (initialized value)

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
