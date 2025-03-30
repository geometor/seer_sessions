```python
"""
Transformation Rule:
1. Create a copy of the input grid to serve as the output grid.
2. Iterate through each pixel of the input grid.
3. If a pixel at (row, col) is not blue (color 1):
    a. Check if there is a pixel to its immediate right (i.e., col + 1 is within the grid width).
    b. If there is a pixel to the right, change the color of the pixel at (row, col + 1) in the output grid to match the color of the pixel at (row, col).
4. The final modified grid is the result.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a transformation where each non-blue pixel 'stamps' its color
    onto the pixel immediately to its right.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape
    
    # Define background color
    background_color = 1 # blue

    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            pixel_color = input_np[r, c]
            
            # Check if the pixel color is not the background color
            if pixel_color != background_color:
                # Calculate the column index of the pixel to the right
                right_col = c + 1
                
                # Check if the right column index is within the grid bounds
                if right_col < width:
                    # Update the pixel to the right in the output grid
                    output_grid[r, right_col] = pixel_color
                    
    return output_grid.tolist() # Return as list of lists if required by ARC environment

```