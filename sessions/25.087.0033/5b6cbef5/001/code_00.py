"""
This transformation creates a larger output grid by conditionally tiling the input grid based on its own pixel values.

1. Determine the dimensions (height H_in and width W_in) of the input grid.
2. Calculate the output grid dimensions: H_out = H_in * H_in, W_out = W_in * W_in.
3. Create a new output grid of size H_out x W_out, initialized entirely with the background color (white, 0).
4. Iterate through each pixel (r, c) of the input grid.
5. Check the color of the input pixel at (r, c).
6. If the input pixel color is NOT the background color (0):
   - Calculate the top-left corner of the corresponding block in the output grid: (start_row = r * H_in, start_col = c * W_in).
   - Copy the entire original input grid into the H_in x W_in block of the output grid starting at (start_row, start_col).
7. If the input pixel color IS the background color (0), the corresponding block in the output grid remains filled with the background color (as initialized).
8. Return the completed output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by conditionally tiling it into a larger grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # 1. Determine input dimensions
    input_h, input_w = input_grid.shape
    
    # 2. Calculate output dimensions
    output_h = input_h * input_h
    output_w = input_w * input_w
    
    # 3. Create and initialize the output grid with background color (0)
    output_grid = np.zeros((output_h, output_w), dtype=int)
    background_color = 0
    
    # 4. Iterate through each pixel of the input grid
    for r in range(input_h):
        for c in range(input_w):
            # 5. Check the color of the input pixel
            pixel_color = input_grid[r, c]
            
            # 6. If the pixel color is not background
            if pixel_color != background_color:
                # Calculate the top-left corner for the block in the output grid
                start_row = r * input_h
                start_col = c * input_w
                
                # Define the block region in the output grid
                end_row = start_row + input_h
                end_col = start_col + input_w
                
                # Copy the entire input grid into this block
                output_grid[start_row:end_row, start_col:end_col] = input_grid
                
            # 7. If the pixel color is background, the block remains 0 (already initialized)
            # No explicit action needed here.
            
    # 8. Return the completed output grid
    return output_grid