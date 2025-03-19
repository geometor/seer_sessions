"""
1.  **Identify Background:** The background color is maroon (9).
2.  **Identify Foreground:** The foreground consists of blue (1) pixels.
3.  **Check for Blue Pixel Connectivity:** Iterate through all pixels. For each blue pixel, check if it is connected to *any* other blue pixel. Connectivity includes horizontal, vertical, and diagonal neighbors.
4.  **Change Color of Connected Blue Pixels:** If a blue pixel is adjacent to at least one other blue pixel (horizontally, vertically, or diagonally), change its color to azure (8).
5.  **Preserve Other Pixels:**  All other pixels, including isolated blue pixels, remain unchanged.
"""

import numpy as np

def is_connected(grid, r, c):
    """Helper function to check for adjacent blue pixels, including diagonals."""
    rows, cols = grid.shape
    if grid[r,c] != 1:
        return False

    # Check adjacent cells (up, down, left, right, and diagonals)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 1:
                return True
    return False

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is blue (1)
            if input_grid[r, c] == 1:
                # Check connectivity (including diagonals)
                if is_connected(input_grid, r, c):
                    output_grid[r, c] = 8

    return output_grid