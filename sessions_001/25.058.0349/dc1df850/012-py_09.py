"""
1.  **Identify** all red pixels in the input grid.
2.  **For each** red pixel:
    *   **If** the red pixel is in the top row (row 0), attempt to create a single blue pixel to its left. If this position is out of bounds (column < 0), do nothing.
    *   **Else (if** the red pixel is *not* in the top row), create a 3x3 square of blue pixels. The red pixel will be at the center of the *top edge* of this blue square.
3. Remove all the original red pixels.
4. The final output grid consists of only the created blue pixels and any remaining original pixels that are not red.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid) # Initialize with all zeros

    # Find all red pixels
    red_pixels = find_pixels(input_grid, 2)

    for r, c in red_pixels:
        if r == 0:
            # Create a blue pixel to the left of the red pixel on the top row
            if c - 1 >= 0:
                output_grid[r, c - 1] = 1
        else:
            # Create a 3x3 blue square with the red pixel at the center of the top edge
            for i in range(r , r + 3):  # Corrected row range
                for j in range(c - 1, c + 2):
                    if 0 <= i < height and 0 <= j < width:
                        output_grid[i, j] = 1
        # No need to explicitly remove red pixels, as output_grid starts empty

    return output_grid