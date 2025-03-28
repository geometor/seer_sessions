import numpy as np

"""
Transforms a 3x3 input grid into a 15x15 output grid based on the following rules:

1. Initialize a 15x15 output grid filled entirely with white (0) pixels.
2. Identify the input grid pattern (the original 3x3 input).
3. Iterate through each pixel of the 3x3 input grid at position (row `r_in`, column `c_in`).
4. If the input pixel at (`r_in`, `c_in`) is gray (5):
    a. Calculate the top-left corner (`R_out`, `C_out`) for placing the 3x3 input pattern centered within the corresponding 5x5 block in the output grid. This position is (`r_in` * 5 + 1, `c_in` * 5 + 1).
    b. Copy the entire 3x3 input grid pattern onto the output grid starting at position (`R_out`, `C_out`), overwriting any pixels already present in that 3x3 area.
5. After iterating through all input pixels, the final state of the output grid represents the result. Pixels initially set to white remain white unless overwritten.
"""

def transform(input_grid):
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid (list[list[int]]): A 3x3 grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed 15x15 grid as a list of lists.
    """
    # Convert input to numpy array for easier manipulation and store it
    input_np = np.array(input_grid, dtype=int)
    in_h, in_w = input_np.shape

    # Define scaling and padding constants
    scale_factor = 5
    padding = 1 # Offset to center the 3x3 pattern in a 5x5 block

    # Calculate output dimensions
    out_h = in_h * scale_factor
    out_w = in_w * scale_factor

    # Initialize the output grid with white (0) pixels
    output_grid = np.zeros((out_h, out_w), dtype=int)

    # Iterate through each pixel of the input grid
    for r_in in range(in_h):
        for c_in in range(in_w):
            # Check if the current input pixel is gray (5)
            if input_np[r_in, c_in] == 5:
                # Calculate the top-left corner coordinates in the output grid
                # for placing the centered input pattern
                out_r_start = r_in * scale_factor + padding
                out_c_start = c_in * scale_factor + padding

                # Calculate the bottom-right corner coordinates (exclusive)
                out_r_end = out_r_start + in_h
                out_c_end = out_c_start + in_w

                # Copy the original 3x3 input grid pattern into the calculated position
                # in the output grid, overwriting existing values.
                output_grid[out_r_start:out_r_end, out_c_start:out_c_end] = input_np

    # Convert the output numpy array back to a list of lists for the expected format
    return output_grid.tolist()