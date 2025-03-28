import numpy as np

"""
Transforms a 3x3 input grid into a 9x9 output grid based on a recursive pattern.

1. Determine the dimensions of the input grid (assumed to be 3x3).
2. Create an output grid that is 3 times larger in both height and width (9x9), initialized with white (0).
3. Identify the single non-white color ('primary_color') present in the input grid.
4. Treat the entire input grid as a 'pattern_grid'.
5. Iterate through each cell (r, c) of the input grid:
    a. If the cell input_grid[r][c] contains the 'primary_color':
        i. Calculate the top-left coordinates (out_r, out_c) = (r * 3, c * 3) for the corresponding 3x3 block in the output grid.
        ii. Copy the 'pattern_grid' (the original 3x3 input) into this 3x3 block of the output grid, starting at (out_r, out_c).
    b. If the cell input_grid[r][c] is white (0), the corresponding 3x3 block in the output grid remains white (as initialized).
6. Return the completed 9x9 output grid.
"""

def find_primary_color(grid):
    """Finds the single non-zero color in the grid."""
    unique_colors = np.unique(grid)
    primary_colors = unique_colors[unique_colors != 0]
    if len(primary_colors) == 1:
        return primary_colors[0]
    elif len(primary_colors) == 0:
        # Handle case where grid is all white (though not expected based on examples)
        return 0 # Or raise an error? Based on examples, there's always one.
    else:
        # Handle case with multiple non-white colors (not expected)
        raise ValueError("Input grid contains more than one non-white color.")


def transform(input_grid):
    """
    Applies the recursive pattern transformation.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get input dimensions
    H_in, W_in = input_np.shape
    
    # Define scale factor (fixed at 3 based on examples)
    scale_factor = 3
    
    # Calculate output dimensions
    H_out = H_in * scale_factor
    W_out = W_in * scale_factor
    
    # Initialize output grid with background color (white = 0)
    output_grid = np.zeros((H_out, W_out), dtype=int)
    
    # Identify the primary color used in the input grid
    try:
        primary_color = find_primary_color(input_np)
    except ValueError as e:
        print(f"Error processing input: {e}")
        # Decide how to handle error: return empty grid, input grid, or raise further?
        # For now, returning an empty grid matching output size.
        return output_grid.tolist() 

    # The input grid itself acts as the pattern to be copied
    pattern_grid = input_np
    
    # Iterate through each cell of the input grid
    for r in range(H_in):
        for c in range(W_in):
            # Check if the current input cell contains the primary color
            if input_np[r, c] == primary_color:
                # Calculate the top-left corner for the block in the output grid
                out_r_start = r * scale_factor
                out_c_start = c * scale_factor
                
                # Define the slice in the output grid to place the pattern
                out_r_end = out_r_start + H_in
                out_c_end = out_c_start + W_in
                
                # Copy the pattern_grid into the calculated block of the output grid
                output_grid[out_r_start:out_r_end, out_c_start:out_c_end] = pattern_grid
                
            # If input_np[r, c] is 0 (white), do nothing, as the output block is already initialized to 0.

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()