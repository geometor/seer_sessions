"""
1.  **Identify Gray Pixels:** Examine each pixel in the input grid. Focus on pixels that are gray (color value 5).
2.  **Check for Linear Gray Neighbors:** For each gray pixel, check its eight neighbors (horizontal, vertical, and diagonal). Determine if there's a straight line of at least three gray pixels (including the center pixel) passing through the center gray pixel. The line can be horizontal, vertical or diagonal.
3.  **Change Color to Green:** If the center gray pixel has this straight line configuration with two additional grey neighbors, change its color to green (color value 3).
4.  **Output:** The output grid is the result of these transformations. All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    rows, cols = input_grid.shape
    output_grid = input_grid.copy()

    def check_line(r, c, dr, dc):
        """Checks for a line of 3 gray pixels in a given direction."""
        if 0 <= r + dr < rows and 0 <= c + dc < cols and input_grid[r + dr, c + dc] == 5:
          if 0 <= r - dr < rows and 0 <= c - dc < cols and input_grid[r-dr, c-dc] == 5:
            return True
        return False

    # Iterate through each cell of the input grid.
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is gray (5).
            if input_grid[r, c] == 5:
                # Check for lines in all directions.
                if check_line(r, c, 1, 0) or \
                   check_line(r, c, 0, 1) or \
                   check_line(r, c, 1, 1) or \
                   check_line(r, c, 1, -1):
                    output_grid[r, c] = 3

    return output_grid