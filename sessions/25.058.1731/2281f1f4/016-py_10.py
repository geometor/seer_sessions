"""
1.  **Identify the "border":** Locate all '5' (gray) pixels along the top and right edges of the input grid.
2.  **Infill:** For each gray pixel identified, change the color value to a '2' (red) of the pixel that is one step diagonally inward (down and to the left). If the gray pixel is at `(row, col)`, infill the pixel `(row + 1, col - 1)` with red, as long as `row + 1` and `col -1` is still within the grid.
3. Gray pixels remain.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating an inner red border based on the gray border.
    """
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through the grid to find gray border pixels
    for row in range(rows):
        for col in range(cols):
            if input_grid[row][col] == 5:
                # Check if it's on the top or right edge
                if row == 0 or col == cols - 1:
                    # Infill diagonally inward with red (if within bounds)
                    if row + 1 < rows and col - 1 >= 0:
                        output_grid[row + 1][col - 1] = 2

    return output_grid