import numpy as np

"""
The transformation rule operates as follows:

1.  Determine the dimensions (height `H` and width `W`) of the input grid.
2.  Create an output grid with dimensions 3*H by 3*W, initialized with the background color white (0).
3.  Imagine the output grid as a 3x3 grid of blocks, where each block has the same dimensions (H x W) as the input grid.
4.  Iterate through each pixel `(r, c)` of the input grid.
5.  If the pixel `input_grid[r][c]` is white (0), then copy the entire original input grid into the corresponding block in the output grid. The block corresponding to input pixel `(r, c)` is located at the top-left corner `(r * H, c * W)` in the output grid.
6.  If the pixel `input_grid[r][c]` is non-white (any color other than 0), the corresponding block in the output grid remains filled with white (0).
7.  The final output grid is the result of placing copies of the input grid into the blocks corresponding to white pixels in the input grid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the rule: copies the input grid into 
    locations specified by the white pixels (0) of the input grid, scaled up 3x.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input grid to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    h_in, w_in = input_np.shape

    # Calculate output grid dimensions
    h_out = h_in * 3
    w_out = w_in * 3

    # Initialize output grid with white (0)
    output_grid = np.zeros((h_out, w_out), dtype=int)

    # Iterate through each cell of the input grid
    for r in range(h_in):
        for c in range(w_in):
            # Check if the input pixel is white (0)
            if input_np[r, c] == 0:
                # Calculate the top-left corner coordinates for the block in the output grid
                start_row = r * h_in
                start_col = c * w_in
                
                # Define the slice for the target block
                row_slice = slice(start_row, start_row + h_in)
                col_slice = slice(start_col, start_col + w_in)
                
                # Copy the entire input grid into the designated block
                output_grid[row_slice, col_slice] = input_np
            # If the input pixel is non-white, the corresponding block in the 
            # output grid remains white (0) as initialized. No action needed.

    # Convert the final NumPy array back to a list of lists
    return output_grid.tolist()
