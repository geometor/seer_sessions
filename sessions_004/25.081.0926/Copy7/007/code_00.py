"""
1.  Identify Lines: Examine the grid and identify "lines" of pixels. A line is a set of adjacent pixels of the same color, either horizontally or vertically.
2.  Black Pixel Replacement: If a black pixel is immediately to the right of a colored line, and a different colored line exist to the right of this black pixel, then the color of the black pixel is conditionally updated.
3.  Conditional update: The color to update with matches the color of the line to the left of the black pixel.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        for c in range(cols):
            # Identify Black Pixel
            if input_grid[r, c] == 0:
                # Check for colored line to the left
                if c > 0 and input_grid[r, c-1] != 0:
                    left_color = input_grid[r, c-1]
                    # Check for different colored line to the right
                    if c + 1 < cols and input_grid[r,c+1] != 0 and input_grid[r,c+1] != left_color:
                       output_grid[r, c] = left_color
    return output_grid