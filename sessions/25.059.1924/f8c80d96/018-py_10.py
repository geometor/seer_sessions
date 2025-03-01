"""
1.  **Border Processing:** Identify the pixels in the outermost rows and columns of the input grid. Change any white (0) pixels in these border positions to gray (5).

2.  **Interior Processing - Shape Replication:**
    * Identify the existing single red (2) pixel. This represents the "seed" of a shape.

    * Identify all of the interior white pixels (those not on the border, which are not changed in the first step).

    * Replicate the shape defined by the red pixel to all interior white pixels, such that the replicated shape is connected. The original single red pixel defines the bottom-right corner of the final shape.

3. **Red Preservation:** The original red pixel must remain in its original position.
"""

import numpy as np

def get_border_pixels(grid):
    """
    Returns a set of (row, col) tuples representing the border pixels.
    """
    rows, cols = grid.shape
    border_pixels = set()
    for r in range(rows):
        border_pixels.add((r, 0))
        border_pixels.add((r, cols - 1))
    for c in range(1, cols - 1):  # Avoid double-counting corners
        border_pixels.add((0, c))
        border_pixels.add((rows - 1, c))
    return border_pixels


def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Border Processing
    border_pixels = get_border_pixels(output_grid)
    for r, c in border_pixels:
        if output_grid[r, c] == 0:
            output_grid[r, c] = 5

    # 2. Interior Processing - Shape Replication
    red_positions = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 2:
                red_positions.append((r, c))
                break  # There should only be one red pixel

    if len(red_positions) > 0:
       red_row, red_col = red_positions[0]

    # determine the size of the shape
       shape_height = red_row + 1
       shape_width = red_col + 1

       for r in range(rows):
            for c in range(cols):
                # check it is an interior white pixel
                if (r,c) not in border_pixels and output_grid[r,c] == 0:
                    # check if the pixel should be within the replicated shape
                    if r <= red_row and c <= red_col:
                      output_grid[r,c] = 2

    return output_grid