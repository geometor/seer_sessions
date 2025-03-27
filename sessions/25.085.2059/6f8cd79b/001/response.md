```python
"""
Creates an output grid of the same dimensions as the input grid.
Pixels on the border (first/last row or first/last column) of the output grid are set to azure (8).
Pixels not on the border retain their original color from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Draws an azure border around the input grid, keeping inner pixels the same.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The output grid with an azure border.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions (height, width) of the input grid
    height, width = input_array.shape
    
    # Initialize the output grid as a copy of the input grid
    # This ensures inner pixels retain their original color by default
    output_grid = np.copy(input_array)
    
    # Iterate through each pixel using its row (r) and column (c) index
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is on the border
            # A pixel is on the border if it's in the first row (r=0),
            # last row (r=height-1), first column (c=0), or last column (c=width-1)
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                # If it's a border pixel, set its color to azure (8)
                output_grid[r, c] = 8
                
    # Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if required by the environment

```