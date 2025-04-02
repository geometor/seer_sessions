```python
import numpy as np

"""
This task identifies horizontally isolated non-white pixels within each row of the input grid and expands them into horizontal lines of length 3 in the output grid, centered at the original pixel's location. Existing horizontal lines of length 3 or longer remain unchanged. The transformation is color-agnostic and operates independently on each row.
"""

def is_horizontally_isolated(grid, r, c):
    """
    Checks if a non-white pixel at (r, c) is horizontally isolated.
    A pixel is isolated if its immediate left and right neighbors within the row
    are either the background color (0) or outside the grid boundaries.
    """
    height, width = grid.shape
    pixel_color = grid[r, c]

    # A white pixel cannot be isolated in this context
    if pixel_color == 0:
        return False

    # Check left neighbor
    left_is_different = True
    if c > 0:
        if grid[r, c - 1] == pixel_color:
            left_is_different = False

    # Check right neighbor
    right_is_different = True
    if c < width - 1:
        if grid[r, c + 1] == pixel_color:
            right_is_different = False

    return left_is_different and right_is_different

def transform(input_grid):
    """
    Transforms the input grid by expanding horizontally isolated non-white pixels
    into horizontal lines of length 3.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array if necessary
    input_grid = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is non-white and horizontally isolated
            if input_grid[r, c] != 0 and is_horizontally_isolated(input_grid, r, c):
                pixel_color = input_grid[r, c]
                
                # Modify the output grid to create a 3-pixel horizontal line
                # centered at the isolated pixel's position (r, c).
                # Ensure modifications stay within grid boundaries.
                
                # Set the center pixel (original isolated pixel position)
                output_grid[r, c] = pixel_color
                
                # Set the left pixel if within bounds
                if c > 0:
                    output_grid[r, c - 1] = pixel_color
                    
                # Set the right pixel if within bounds
                if c < width - 1:
                    output_grid[r, c + 1] = pixel_color

    return output_grid.tolist() # Convert back to list of lists if required by the environment
```