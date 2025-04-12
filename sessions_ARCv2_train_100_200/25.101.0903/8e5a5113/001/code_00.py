"""
Transforms the input grid by rotating the top-left 3x3 block and placing the rotated versions into specific locations in the grid.

1. Initialize the output grid as a copy of the input grid.
2. Identify the 3x3 subgrid located at the top-left corner of the input grid (rows 0-2, columns 0-2). Call this the `source_block`.
3. Rotate the `source_block` 90 degrees clockwise. Call this `rotated_block_90`.
4. Rotate the `source_block` 180 degrees. Call this `rotated_block_180`.
5. Place the `rotated_block_90` into the output grid at rows 0-2, columns 4-6, overwriting the existing white pixels.
6. Place the `rotated_block_180` into the output grid at rows 0-2, columns 8-10, overwriting the existing white pixels.
7. Return the modified output grid.
"""

import numpy as np

def rotate_clockwise_90(grid_array: np.ndarray) -> np.ndarray:
    """Rotates a numpy array 90 degrees clockwise."""
    return np.rot90(grid_array, k=-1)

def rotate_180(grid_array: np.ndarray) -> np.ndarray:
    """Rotates a numpy array 180 degrees."""
    return np.rot90(grid_array, k=2)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described rotation and placement transformation to the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Initialize output_grid as a copy of the input grid
    output_array = np.copy(input_array)

    # Identify the source_block (top-left 3x3)
    source_block = input_array[0:3, 0:3]

    # Rotate the source_block 90 degrees clockwise
    rotated_block_90 = rotate_clockwise_90(source_block)

    # Rotate the source_block 180 degrees
    rotated_block_180 = rotate_180(source_block)

    # Place the rotated_block_90 into the output grid (rows 0-2, columns 4-6)
    output_array[0:3, 4:7] = rotated_block_90

    # Place the rotated_block_180 into the output grid (rows 0-2, columns 8-11)
    output_array[0:3, 8:11] = rotated_block_180

    # Convert the result back to a list of lists
    output_grid = output_array.tolist()

    return output_grid