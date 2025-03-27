"""
Transforms an input grid by embedding it diagonally into a larger output grid.
Each row `r` of the input grid is shifted horizontally to the right by `(input_height - 1) - r` columns.
The new areas created in the output grid are filled with the white pixel (value 0).
The output grid's height is the same as the input, and its width is `input_width + input_height - 1`.
"""

import numpy as np

def transform(input_grid):
    """
    Embeds the input grid diagonally into a larger grid.

    Args:
        input_grid (list of lists or np.ndarray): The input 2D grid.

    Returns:
        np.ndarray: The transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the input grid
    H, W = input_np.shape
    
    # Calculate the width of the output grid
    output_width = W + H - 1
    
    # Create a new output grid with dimensions H by output_width, filled with white (0)
    output_grid = np.zeros((H, output_width), dtype=int)
    
    # Iterate through each row of the input grid
    for r in range(H):
        # Calculate the horizontal shift amount for the current row r
        # The shift decreases as the row index r increases
        shift = (H - 1) - r
        
        # Copy the pixels from the input grid's row r into the output grid's row r,
        # starting at the calculated shift column index.
        # The slice output_grid[r, shift:shift + W] selects the target columns in the output row.
        # The slice input_np[r, :] selects the entire row from the input.
        output_grid[r, shift:shift + W] = input_np[r, :]
        
    # Return the resulting grid
    return output_grid.tolist() # Return as list of lists to match ARC standard if needed, though numpy is often used.
                                # Keeping as numpy array as it's generally more convenient for ARC tasks.
                                # Let's stick to numpy array output as per common practice in ARC solvers.
    # return output_grid 
