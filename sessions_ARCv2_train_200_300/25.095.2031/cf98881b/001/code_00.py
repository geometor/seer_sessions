"""
This module transforms a 4x14 input grid into a 4x4 output grid.
The transformation rule involves partitioning the input grid into three 4x4 blocks (A, B, C)
by skipping delimiter columns 4 and 9. The output grid is constructed cell by cell,
prioritizing non-zero values from Block A, then Block B, and finally Block C for each
corresponding cell position.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Combines three 4x4 blocks from a 4x14 input grid into a single 4x4
    output grid based on a priority rule.

    Args:
        input_grid: A list of lists representing the 4x14 input grid.

    Returns:
        A list of lists representing the 4x4 output grid.
    """
    # Convert input list of lists to a NumPy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # Extract the three 4x4 data blocks, skipping delimiter columns 4 and 9
    block_a = input_array[:, 0:4]  # Columns 0, 1, 2, 3
    block_b = input_array[:, 5:9]  # Columns 5, 6, 7, 8
    block_c = input_array[:, 10:14] # Columns 10, 11, 12, 13

    # Get the dimensions for iteration (should be 4x4)
    rows, cols = block_a.shape

    # Initialize the output grid (4x4) with zeros
    output_array = np.zeros((rows, cols), dtype=int)

    # Iterate through each cell position (r, c)
    for r in range(rows):
        for c in range(cols):
            # Retrieve values from the corresponding position in each block
            val_a = block_a[r, c]
            val_b = block_b[r, c]
            val_c = block_c[r, c]

            # Apply the priority logic: A > B > C (for non-zero values)
            if val_a != 0:
                output_array[r, c] = val_a
            elif val_b != 0:
                output_array[r, c] = val_b
            else:
                output_array[r, c] = val_c # Use C if A and B are zero

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
