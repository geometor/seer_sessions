"""
Takes an input grid, creates an output grid with twice the height and the same width.
The top half of the output grid is a copy of the input grid.
The bottom half of the output grid is a vertically reflected (flipped upside down) copy of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the vertical reflection and concatenation transformation.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the height (H) and width (W) of the input grid
    H, W = input_np.shape
    
    # Initialize the output grid with twice the height and the same width, filled with zeros initially
    output_grid = np.zeros((2 * H, W), dtype=int)
    
    # Step 1 & 3: Copy the input grid into the top half of the output grid
    # Rows 0 to H-1
    output_grid[0:H, :] = input_np
    
    # Step 2 & 4: Create a vertically reflected version of the input grid
    # This flips the rows: the first row becomes the last, the second becomes second-to-last, etc.
    reflected_grid = np.flipud(input_np) # flipud = flip up-down
    
    # Step 5: Copy the reflected grid into the bottom half of the output grid
    # Rows H to 2*H - 1
    output_grid[H:2*H, :] = reflected_grid
    
    # Step 6: Return the resulting grid
    return output_grid.tolist() # Convert back to list of lists if required by the environment
