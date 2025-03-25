"""
Transforms the input grid by reflecting each pixel across the main diagonal and creating a 2x2 block of the same color at the reflected position. The color value used for the 2x2 block is taken from the original pixel's location before reflection.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid as per the description.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through every pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            # Get the color of the original pixel
            original_color = input_grid[r, c]

            # Reflect: Swap row and column indices
            reflected_r, reflected_c = c, r

            # Create 2x2 block with reflected position as top-left
            for i in range(2):
                for j in range(2):
                    if 0 <= reflected_r + i < rows and 0 <= reflected_c + j < cols:
                        output_grid[reflected_r + i, reflected_c + j] = original_color

    return output_grid.tolist()