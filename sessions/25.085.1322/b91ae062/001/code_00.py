import numpy as np
import collections

"""
Upscales an input grid based on the number of unique non-white colors.

1.  Count the number of distinct non-white (color values 1 through 9) pixels 
    present in the input grid. Let this count be `N`.
2.  Determine the dimensions of the input grid (height `H_in`, width `W_in`).
3.  Calculate the dimensions of the output grid: height `H_out = H_in * N`, 
    width `W_out = W_in * N`.
4.  Create the output grid with dimensions `H_out` x `W_out`.
5.  Iterate through each pixel of the input grid at `(row, col)`.
6.  Let the color of the input pixel be `C`.
7.  In the output grid, fill the square block of size `N x N`, whose top-left 
    corner is at `(row * N, col * N)`, entirely with the color `C`.
8.  Return the completed output grid.
"""

def calculate_scaling_factor(grid_np):
    """
    Calculates the scaling factor N by counting unique non-white colors.
    """
    # Flatten the grid to easily find unique values
    flat_grid = grid_np.flatten()
    # Filter out white pixels (value 0)
    non_white_pixels = flat_grid[flat_grid != 0]
    # Find unique non-white colors
    unique_colors = np.unique(non_white_pixels)
    # The scaling factor N is the count of these unique colors
    n = len(unique_colors)
    # Handle the edge case where the grid might be all white
    # Based on examples, N is always at least 1 if there are non-white cells.
    # If the grid is *entirely* white, N will be 0. The examples don't show
    # this case. Assuming N must be at least 1 if any scaling is done.
    # If N=0, perhaps return 1 to avoid 0-sized output? Or is it guaranteed N>=1?
    # Let's assume N will be >= 1 based on the provided examples. If an all-white
    # input yields N=0, the scaling logic breaks. We'll proceed assuming N>=1.
    # If N actually results in 0, the code might raise an error later or produce
    # an empty grid depending on numpy version. Let's enforce N=1 if it's 0.
    if n == 0:
       # If there are no non-white colors, check if the grid contains *any* cells.
       # If it's non-empty and all white, perhaps N should be 1?
       # Let's follow the rule strictly first: N is the count.
       # But output dimensions would be 0x0. Let's default N to 1 in this case.
       # This means an all-white input maps to an identical all-white output.
        return 1 
    return n

def transform(input_grid):
    """
    Transforms the input grid by scaling each pixel into an NxN block,
    where N is the count of unique non-white colors in the input grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Step 1: Calculate the scaling factor N
    n = calculate_scaling_factor(input_np)
    
    # Step 2: Determine input dimensions
    h_in, w_in = input_np.shape
    
    # Step 3: Calculate output dimensions
    h_out = h_in * n
    w_out = w_in * n
    
    # Step 4: Create the output grid (initialized with zeros - white)
    # It's safer to initialize, although all cells should be overwritten.
    output_np = np.zeros((h_out, w_out), dtype=int)
    
    # Step 5 & 6 & 7: Iterate through input pixels and fill output blocks
    for r in range(h_in):
        for c in range(w_in):
            # Get the color of the current input pixel
            color = input_np[r, c]
            
            # Calculate the top-left corner of the corresponding block in the output grid
            start_row = r * n
            start_col = c * n
            
            # Fill the N x N block in the output grid with the color
            output_np[start_row : start_row + n, start_col : start_col + n] = color
            
    # Step 8: Convert numpy array back to list of lists for the required output format
    output_grid = output_np.tolist()
    
    return output_grid
