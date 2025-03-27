"""
Transforms an input grid into an output grid by expanding its width and shifting each row diagonally.
1. Determines the height (H) and width (W_in) of the input grid.
2. Calculates the new width (W_out) as W_in + H - 1.
3. Creates an output grid of size H x W_out, filled with white pixels (0).
4. Iterates through each row 'r' of the input grid (from 0 to H-1).
5. Calculates a horizontal shift for row 'r' as (H - 1) - r.
6. Copies the content of input row 'r' into the output grid's row 'r' starting at the calculated shift column index.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a diagonal shift transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)

    # 1. Determine the height (H) and width (W_in) of the input grid.
    H, W_in = input_grid_np.shape

    # 2. Calculate the required width increase and the new width (W_out).
    width_increase = H - 1
    W_out = W_in + width_increase

    # 3. Create a new output grid with dimensions H x W_out, initializing all pixels to white (0).
    output_grid = np.zeros((H, W_out), dtype=int)

    # 4. Iterate through each row of the input grid.
    for r in range(H):
        # 5. Calculate the horizontal shift amount for the current row 'r'.
        shift = (H - 1) - r

        # 6. Copy the pixels from the input grid's row 'r' into the output grid's row 'r',
        #    starting at column index 'shift'.
        # Ensure the slice boundaries are correct.
        output_grid[r, shift : shift + W_in] = input_grid_np[r, :]

    # 7. Return the completed output grid.
    return output_grid.tolist() # Convert back to list of lists if required by the environment
