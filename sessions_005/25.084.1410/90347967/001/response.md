```python
"""
Rotates the input grid by 180 degrees. Each pixel at position (r, c) in the input grid is moved to position (H-1-r, W-1-c) in the output grid, where H is the height and W is the width of the grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates a 2D grid by 180 degrees.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The rotated grid.
    """
    # Convert input to numpy array for easier handling
    grid = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    height, width = grid.shape
    
    # Initialize the output grid with the same dimensions and data type, filled with zeros (or any default value)
    output_grid = np.zeros_like(grid)
    
    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Get the value (color) of the current pixel
            pixel_value = grid[r, c]
            
            # Calculate the corresponding position in the output grid for 180-degree rotation
            new_r = height - 1 - r
            new_c = width - 1 - c
            
            # Assign the pixel value to the new position in the output grid
            output_grid[new_r, new_c] = pixel_value
            
    # Return the completed output grid
    return output_grid

```