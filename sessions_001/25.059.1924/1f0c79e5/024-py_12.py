"""
1.  **Initialization:** Create an output grid filled with white pixels(0).
2.  **Shape Definition:** Define the "E" shape as a pattern: a vertical line of 7 pixels and three horizontal lines (top, middle, and bottom), each 3 pixels long, connected to the vertical line.
3.  **Drawing the Shape:**
    *   Start drawing at the top-left corner (0, 0) of the output grid.
    *   Draw the vertical line of the "E": Fill 7 pixels downwards with orange (7).
    *   Draw the top horizontal line: From the top of the vertical line, fill 3 pixels to the right with orange (7).
    *   Draw the middle horizontal line: From the 4th pixel down on the vertical line, fill 3 pixels to the right with orange (7).
    *    Draw the bottom horizontal line: From the bottom of the vertical line, fill 3 pixels to the right with orange (7).
4.  **Output:** The output grid contains the completed "E" shape in orange at the top-left corner. The rest of the output grid should remain background (white).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Draw the vertical line of the "E" (7 pixels down)
    for i in range(min(7, rows)):
        output_grid[i, 0] = 7

    # Draw the top horizontal line (3 pixels right)
    for i in range(min(3, cols)):
        output_grid[0, i] = 7

    # Draw the middle horizontal line (3 pixels right, starting from the 4th pixel down)
    for i in range(min(3, cols)):
        if 3 < rows:
          output_grid[3, i] = 7

    # Draw the bottom horizontal line (3 pixels right, starting from the 7th pixel down)
    for i in range(min(3, cols)):
        if 6 < rows :
          output_grid[6, i] = 7

    return output_grid