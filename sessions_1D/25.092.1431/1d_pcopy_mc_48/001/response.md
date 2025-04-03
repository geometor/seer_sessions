```python
"""
Identifies horizontally isolated non-white pixels ('dots') in the input grid.
For each identified dot at position (r, c) with color C, it expands it into a 
horizontal line of length 3 (pixels at (r, c-1), (r, c), (r, c+1)) in the 
output grid, using the same color C. 
Boundary conditions are handled, ensuring the line stays within the grid width.
All other pixels, including background (white) and existing horizontal lines 
of length 3 or other shapes, are copied unchanged from the input to the output.
"""

import numpy as np

def is_horizontally_isolated(grid, r, c):
    """
    Checks if a non-white pixel at (r, c) is horizontally isolated.
    A pixel is horizontally isolated if its left and right neighbors (if they exist)
    are not of the same color.
    """
    height, width = grid.shape
    color = grid[r, c]

    # Should not be called for white pixels, but check just in case
    if color == 0:
        return False

    # Check left neighbor
    left_isolated = True
    if c > 0:  # If not on the left edge
        if grid[r, c - 1] == color:
            left_isolated = False

    # Check right neighbor
    right_isolated = True
    if c < width - 1:  # If not on the right edge
        if grid[r, c + 1] == color:
            right_isolated = False

    return left_isolated and right_isolated

def transform(input_grid):
    """
    Transforms the input grid by expanding horizontally isolated pixels ('dots')
    into horizontal lines of length 3.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]

            # Check if the pixel is non-white and horizontally isolated ('dot')
            if color != 0 and is_horizontally_isolated(input_np, r, c):
                # Expand the dot into a horizontal line of length 3 in the output grid
                # Center pixel (original dot position)
                output_grid[r, c] = color
                # Left pixel (if within bounds)
                if c > 0:
                    output_grid[r, c - 1] = color
                # Right pixel (if within bounds)
                if c < width - 1:
                    output_grid[r, c + 1] = color

    # Return the modified grid
    return output_grid.tolist()

```