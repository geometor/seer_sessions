"""
1.  **Identify:** Locate all blue (1) and red (2) pixels within the input grid.
2.  **Iterate:** For *each* blue and red pixel found:
3.  **Fill Right:** In the same row as the identified pixel, fill all cells to the right of the pixel with the same color as the pixel (blue or red, respectively). Continue filling to the end of that row.
4.  **Output:** The output grid preserves all the original blue and red pixel positions and fills the cells to the right.
"""

import numpy as np

def find_all_pixels(grid, color):
    """Finds the coordinates of all occurrences of a specified color."""
    positions = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == color:
                positions.append((r, c))
    return positions

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find all blue and red pixels
    blue_pixels = find_all_pixels(input_grid, 1)
    red_pixels = find_all_pixels(input_grid, 2)

    # Iterate through blue pixels and fill right
    for r, c in blue_pixels:
        output_grid[r, c] = 1  # Preserve original blue pixel
        for x in range(c + 1, cols):
            output_grid[r, x] = 1

    # Iterate through red pixels and fill right
    for r, c in red_pixels:
        output_grid[r, c] = 2  # Preserve original red pixel
        for x in range(c + 1, cols):
            output_grid[r, x] = 2

    return output_grid