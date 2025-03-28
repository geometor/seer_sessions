import numpy as np

"""
Transforms a 3x3 input grid into a 9x9 output grid.

1.  Identify the single non-white color ('primary_color') in the 3x3 input grid.
2.  Create an 'inverted_pattern' grid (3x3) by taking the input grid and swapping the 'primary_color' with white (0).
3.  Initialize a 9x9 output grid filled with white (0).
4.  Iterate through each cell (r, c) of the 3x3 input grid:
    a. If the input cell input_grid[r][c] is white (0):
        i. Calculate the top-left coordinates (out_r, out_c) = (r * 3, c * 3) for the corresponding 3x3 block in the output grid.
        ii. Copy the 'inverted_pattern' grid into this 3x3 block of the output grid.
    b. If the input cell input_grid[r][c] contains the 'primary_color':
        i. The corresponding 3x3 block in the output grid remains white (as initialized).
5.  Return the completed 9x9 output grid.
"""

def find_primary_color(grid):
    """
    Finds the single non-zero (non-white) color in the grid.
    Assumes exactly one such color exists based on task examples.
    """
    unique_colors = np.unique(grid)
    primary_colors = unique_colors[unique_colors != 0]
    if len(primary_colors) == 1:
        return primary_colors[0]
    elif len(primary_colors) == 0:
        # Handle case where grid is all white - return 0 as per convention
        # although this case might not be valid for this specific task's logic.
        return 0 
    else:
        # This case is not expected based on the examples provided for this task.
        # If it occurs, the logic might be misinterpreting the task.
        # For now, raise an error to indicate unexpected input.
        raise ValueError("Input grid should contain exactly one non-white color.")

def create_inverted_pattern(grid, primary_color):
    """
    Creates a new grid by swapping the primary_color and white(0) in the input grid.
    """
    # Ensure we don't modify the original grid
    inverted = grid.copy() 
    
    # Create boolean masks for swapping
    is_primary = (inverted == primary_color)
    is_white = (inverted == 0)
    
    # Perform the swap
    inverted[is_primary] = 0
    inverted[is_white] = primary_color
    
    return inverted

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    
    # Validate input shape (optional but good practice)
    if input_np.shape != (3, 3):
        # Handle error: Return input? Empty grid? Raise error?
        # Based on task description, assume 3x3 input.
        # If not, returning input might be safest fallback.
        print(f"Warning: Expected 3x3 input, got {input_np.shape}. Returning original input.")
        return input_grid
        
    # Get input dimensions
    H_in, W_in = input_np.shape
    
    # Define scale factor (fixed at 3 based on analysis)
    scale_factor = 3
    
    # Calculate output dimensions
    H_out = H_in * scale_factor
    W_out = W_in * scale_factor
    
    # Initialize output grid with the background color (white = 0)
    output_grid = np.zeros((H_out, W_out), dtype=int)
    
    # 1. Identify the primary color
    try:
        primary_color = find_primary_color(input_np)
        # Handle the edge case where input is all white (primary_color=0)
        if primary_color == 0:
             # If input is all white, inverted is all white.
             # Placing white blocks for white input cells means output is all white.
             return output_grid.tolist() 
             
    except ValueError as e:
        print(f"Error processing input: {e}")
        # Return an empty grid of the expected output size in case of error.
        return output_grid.tolist() 

    # 2. Create the inverted pattern grid
    inverted_pattern_np = create_inverted_pattern(input_np, primary_color)
    
    # 4. Populate Output Blocks based on input grid values
    for r in range(H_in):
        for c in range(W_in):
            # Determine the top-left corner for the block in the output grid
            out_r_start = r * scale_factor
            out_c_start = c * scale_factor
            
            # Define the slice for the output block
            out_r_end = out_r_start + H_in # H_in is 3 (pattern height)
            out_c_end = out_c_start + W_in # W_in is 3 (pattern width)
                
            # 4a. If the input cell is white (0), place the inverted pattern
            if input_np[r, c] == 0:
                output_grid[out_r_start:out_r_end, out_c_start:out_c_end] = inverted_pattern_np
                
            # 4b. If the input cell is the primary color, do nothing (block remains white)
            # No explicit 'else' needed as the grid is initialized to 0.

    # 5. Return the completed output grid, converted back to list of lists format
    return output_grid.tolist()