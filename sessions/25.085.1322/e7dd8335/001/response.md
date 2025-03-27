```python
"""
Identifies the connected blue object (color 1) in the input grid.
Determines the vertical extent (min and max rows) of this object.
Calculates the horizontal midpoint row index based on the vertical extent.
Creates a copy of the input grid.
Iterates through the grid, changing any blue pixel (color 1) located in a row strictly below the calculated midpoint row to red (color 2).
Pixels at or above the midpoint row, and all other pixels, remain unchanged.
Returns the modified grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing the color of the lower half of the blue object to red.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    
    # 1. Identify all pixels with the color blue (1)
    blue_pixels = np.argwhere(input_grid_np == 1)

    # Handle case where there are no blue pixels
    if blue_pixels.size == 0:
        return output_grid # Return the unchanged grid

    # 2. Determine the minimum (min_row) and maximum (max_row) row indices
    min_row = np.min(blue_pixels[:, 0])
    max_row = np.max(blue_pixels[:, 0])

    # 3. Calculate the horizontal midpoint row index
    # Using integer division // which performs floor implicitly for positive results
    mid_row = (min_row + max_row) // 2 
    
    # 4. Output grid is already initialized as a copy

    # 5-7. Iterate through pixels and apply transformation
    rows, cols = input_grid_np.shape
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is blue (1) AND its row is below the midpoint
            if input_grid_np[r, c] == 1 and r > mid_row:
                # Change the color in the output grid to red (2)
                output_grid[r, c] = 2
            # Otherwise, the pixel in output_grid retains its original color (already copied)

    # 8. Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if needed by the environment
```