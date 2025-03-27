"""
Transform an input grid into a larger output grid by replacing each pixel 
of the input grid with a 3x3 block in the output grid. 
If the input pixel is white (0), the corresponding 3x3 block in the output 
is entirely white (0). If the input pixel is non-white, the corresponding 
3x3 block in the output is a copy of the entire original input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Scales up an input grid where each pixel's value determines the content 
    of a 3x3 subgrid in the output.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the input grid
    H, W = input_np.shape
    
    # Calculate the dimensions of the output grid (3 times input dimensions)
    output_H = H * H # Based on YAML 
    output_W = W * W # Based on YAML
    
    # Revisit based on NL description: Output dimensions should be H*3, W*3
    output_H = H * 3
    output_W = W * 3

    # Create a new output grid initialized with white (0) pixels
    output_grid = np.zeros((output_H, output_W), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(H):
        for c in range(W):
            # Get the color of the current input pixel
            pixel_color = input_np[r, c]

            # Check if the input pixel is non-white
            if pixel_color != 0:
                # Calculate the top-left corner coordinates for the 3x3 block in the output grid
                # Correction: The block to be copied is HxW (size of input), not 3x3.
                start_row = r * H # Based on YAML and initial interpretation. Let's re-check.
                start_col = c * W # Based on YAML and initial interpretation. Let's re-check.

                # Revisit based on NL description and examples (3x3 input -> 9x9 output):
                # The block starts at (r*3, c*3) and has size H x W (3x3 in examples)
                start_row = r * 3
                start_col = c * 3
                
                # Define the slice in the output grid where the input grid will be copied
                # The size of the slice should match the input grid dimensions (H x W)
                end_row = start_row + H
                end_col = start_col + W
                
                # Copy the entire original input grid into the calculated block
                output_grid[start_row:end_row, start_col:end_col] = input_np
            # else: If the input pixel is white (0), the corresponding block in the 
            # output grid remains white (0), which is the initial state. No action needed.

    return output_grid.tolist() # Return as list of lists as per ARC standard