```python
"""
Transforms an input NxN grid into a 2Nx2N output grid by assembling four NxN blocks.
The top-left block is the original input grid.
The top-right block is the horizontal flip of the transpose of the input grid.
The bottom-left block is the vertical flip of the transpose of the input grid.
The bottom-right block is the horizontal flip of the vertical flip of the original input grid.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A square list of lists representing the NxN input grid.

    Returns:
        A list of lists representing the 2Nx2N output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    N = input_array.shape[0] # Determine the dimension N

    # Initialize the output grid as a numpy array of size 2N x 2N
    # Using zeros initially, will be filled with correct values
    output_array = np.zeros((2 * N, 2 * N), dtype=int)

    # --- Perform transformations ---

    # 1. Calculate the transpose of the input grid (I_T)
    input_transposed = np.transpose(input_array)

    # 2. Calculate the top-right block (TR_Block): Horizontal flip of I_T
    tr_block = np.fliplr(input_transposed)

    # 3. Calculate the bottom-left block (BL_Block): Vertical flip of I_T
    bl_block = np.flipud(input_transposed)

    # 4. Calculate the bottom-right block (BR_Block): Vertical flip of I, then horizontal flip
    temp_fv = np.flipud(input_array) # FV(I)
    br_block = np.fliplr(temp_fv) # FH(FV(I))

    # --- Assemble the output grid ---

    # 5. Place the original input grid (I) into the top-left quadrant
    output_array[0:N, 0:N] = input_array

    # 6. Place the TR_Block into the top-right quadrant
    output_array[0:N, N:2*N] = tr_block

    # 7. Place the BL_Block into the bottom-left quadrant
    output_array[N:2*N, 0:N] = bl_block

    # 8. Place the BR_Block into the bottom-right quadrant
    output_array[N:2*N, N:2*N] = br_block

    # Convert the final numpy array back to a list of lists for the return value
    output_grid = output_array.tolist()

    return output_grid
```