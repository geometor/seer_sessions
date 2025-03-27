"""
Identify seed pixels within the input grid, which are pixels with colors other than white (0) or blue (1). For each seed pixel found at coordinates (r, c) with color C, define a 3x3 target area below and centered relative to the seed, covering rows r to r+2 and columns c-1 to c+1. Within this 3x3 area, change the color of pixels in the output grid to C, but only if the corresponding pixel in the original input grid was white (0) or if it is the seed pixel itself. Preserve all other pixels (blue boundaries and background outside fill areas) from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_np[r, c]
            
            # Check if the pixel is a "seed pixel" (not white 0 and not blue 1)
            if pixel_color != 0 and pixel_color != 1:
                seed_color = pixel_color
                seed_r, seed_c = r, c

                # Define the target 3x3 area relative to the seed pixel
                # Rows: r to r+2
                # Columns: c-1 to c+1
                for nr in range(seed_r, seed_r + 3):
                    for nc in range(seed_c - 1, seed_c + 2):
                        
                        # Check if the coordinate (nr, nc) is within the grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            
                            # Check the condition for filling:
                            # Original pixel was white (0) OR it's the seed pixel itself
                            if input_np[nr, nc] == 0 or (nr == seed_r and nc == seed_c):
                                # Update the pixel in the output grid with the seed's color
                                output_grid[nr, nc] = seed_color

    return output_grid.tolist() # Return as list of lists if needed, or keep as np.ndarray
