import numpy as np
from copy import deepcopy

"""
Transform a 7x7 grid of digits based on local transformations within 3x3 subgrids.
The transformation rule involves identifying 3x3 blocks composed entirely of non-7 digits.
For each such block:
1. Rotate the block 90 degrees clockwise.
2. Swap the corner elements: top-left (0,0) with bottom-right (2,2).
3. Swap the other corner elements: top-right (0,2) with bottom-left (2,0).
Cells with the digit 7 remain unchanged.
"""

def is_active_block(block: np.ndarray) -> bool:
    """Checks if a 3x3 block contains any 7s."""
    return not np.any(block == 7)

def transform_block(block: np.ndarray) -> np.ndarray:
    """Applies the rotation and corner swaps to a 3x3 block."""
    # 1. Rotate 90 degrees clockwise
    rotated_block = np.rot90(block, k=-1) # k=-1 for clockwise

    # Make a copy to perform swaps
    transformed_block = rotated_block.copy()

    # 2. Swap top-left (0,0) with bottom-right (2,2)
    transformed_block[0, 0], transformed_block[2, 2] = rotated_block[2, 2], rotated_block[0, 0]

    # 3. Swap top-right (0,2) with bottom-left (2,0)
    # Note: Use the already swapped values if the previous swap affected these corners,
    # but in this specific sequence, the corners involved in step 2 are distinct
    # from those in step 3 *after rotation*.
    # Let's re-check the logic. Swaps happen *after* rotation.
    # The values at the corners of rotated_block are used for the swap targets
    # in transformed_block.
    transformed_block[0, 2], transformed_block[2, 0] = rotated_block[2, 0], rotated_block[0, 2]


    return transformed_block


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    Identifies active 3x3 blocks (no 7s), transforms them (rotate, swap corners),
    and updates the grid.
    """
    # Convert input to numpy array for easier slicing and operations
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid.
    # Background 7s are handled automatically.
    output_array = input_array.copy()

    rows, cols = input_array.shape

    # Iterate through all possible top-left corners (r, c) of 3x3 blocks
    # The maximum row index for the top-left corner is rows - 3
    # The maximum col index for the top-left corner is cols - 3
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Extract the 3x3 subgrid
            block = input_array[r:r+3, c:c+3]

            # Check if it's an active block (contains no 7s)
            if is_active_block(block):
                # Transform the active block
                transformed_subgrid = transform_block(block)
                # Place the transformed block back into the output grid
                output_array[r:r+3, c:c+3] = transformed_subgrid

    # Convert the result back to a list of lists
    output_grid = output_array.tolist()
    return output_grid
