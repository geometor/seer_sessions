import numpy as np

"""
Transforms a 3x3 input grid into a 15x15 output grid based on the following rules:

1.  Determine the input grid dimensions (assumed 3x3) and calculate output dimensions (input dimensions * 5).
2.  Initialize a 15x15 output grid filled entirely with white (0) pixels.
3.  Store the original 3x3 input grid pattern.
4.  Calculate the padding needed to center the 3x3 input pattern within a 5x5 block (padding = 1).
5.  Iterate through each pixel of the 3x3 input grid at position (row `r_in`, column `c_in`).
6.  If the input pixel at (`r_in`, `c_in`) is gray (5):
    a. Calculate the top-left corner (`R_out`, `C_out`) in the output grid for placing the centered 3x3 input pattern. This position is (`r_in` * 5 + padding, `c_in` * 5 + padding).
    b. Copy the *entire original 3x3 input grid pattern* onto the output grid starting at position (`R_out`, `C_out`), overwriting any pixels already present in that 3x3 area.
7.  After iterating through all input pixels, the final state of the output grid represents the result. Pixels initially set to white remain white unless overwritten.
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
    
    # Basic check for input dimensions, although ARC examples usually conform
    if input_np.shape != (3, 3):
        # Handle error or unexpected input size if necessary
        # For this problem, we assume 3x3
        pass 
        
    in_h, in_w = input_np.shape

    # Define scaling factor
    scale_factor = 5
    
    # Calculate padding to center the 3x3 input within a 5x5 block
    # padding = (scale_factor - in_h) // 2 
    padding = 1 

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
                # for placing the centered 3x3 input pattern
                out_r_start = r_in * scale_factor + padding
                out_c_start = c_in * scale_factor + padding

                # Calculate the bottom-right corner coordinates (exclusive)
                # for the 3x3 area to be overwritten
                out_r_end = out_r_start + in_h
                out_c_end = out_c_start + in_w

                # Ensure the slice dimensions match the input grid dimensions
                # This check is mostly for safety, assuming input is always 3x3
                if (out_r_end - out_r_start == in_h) and (out_c_end - out_c_start == in_w):
                    # Copy the *original* 3x3 input grid pattern into the 
                    # calculated position in the output grid, overwriting 
                    # existing values.
                    output_grid[out_r_start:out_r_end, out_c_start:out_c_end] = input_np
                else:
                    # Handle potential dimension mismatch if necessary
                    pass

    # Convert the output numpy array back to a list of lists for the expected format
    return output_grid.tolist()