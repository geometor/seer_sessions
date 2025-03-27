"""
Transforms an input grid by embedding it diagonally into a larger output grid.

The transformation involves the following steps:
1. Determine the height (H) and width (W) of the input grid.
2. Calculate the dimensions of the output grid: height remains H, width becomes W + H - 1.
3. Create the output grid and initialize all its cells with the 'white' color (0).
4. Iterate through each row 'r' of the input grid (from 0 to H-1).
5. For each row 'r', calculate a horizontal shift 's' = H - 1 - r. This shift decreases for lower rows.
6. Copy the pixels from the input row 'r' (columns 'c' from 0 to W-1) to the output grid at row 'r', starting at column 'c + s'.
7. The resulting grid, containing the diagonally shifted input grid padded with 'white', is the final output.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a diagonal shift transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Determine the height (H) and width (W) of the input grid.
    H, W = input_np.shape
    
    # 2. Calculate the width of the output grid. Height remains H.
    output_width = W + H - 1
    output_height = H
    
    # 3. Create the output grid and initialize with 'white' (0).
    output_np = np.zeros((output_height, output_width), dtype=int)
    
    # 4. Iterate through each row 'r' of the input grid.
    for r in range(H):
        # 5. Calculate the horizontal shift 's' for the current row 'r'.
        shift = H - 1 - r
        
        # 6. Copy pixels from input row 'r' to output row 'r' with the calculated shift.
        # Iterate through each column 'c' in the input grid row.
        for c in range(W):
            # Get the pixel value from the input grid.
            pixel_value = input_np[r, c]
            # Place the pixel value into the output grid at the shifted position.
            output_np[r, c + shift] = pixel_value
            
    # Convert the numpy array back to a list of lists for the final output format.
    output_grid = output_np.tolist()
    
    # 7. Return the resulting grid.
    return output_grid
