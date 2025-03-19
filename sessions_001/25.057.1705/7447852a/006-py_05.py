"""
1.  **Identify Red Pixels:** Locate all pixels with the value '2' (red) within the input grid.
2.  **Identify White Pixels:** Locate all pixels with the value of '0' (white) within the input grid.
3.  **Adjacent Transformation:** For each white pixel, check if it is directly adjacent (horizontally or vertically, but *not* diagonally) to any red pixel.
4.  **Change to Yellow:** If a white pixel is adjacent to a red pixel, change its value to '4' (yellow) in the output grid.
5.  **Preserve Other Pixels:** All other pixels that are not white and adjacent to a red pixel retain their original values in the output grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Identify '2's (red pixels)
    red_pixels = [(r, c) for r in range(rows) for c in range(cols) if input_grid[r, c] == 2]

    # Iterate through all white pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:  # Check if it's a white pixel
                # Check for adjacent red pixels
                for neighbor_row, neighbor_col in get_neighbors(input_grid, r, c):
                    if input_grid[neighbor_row, neighbor_col] == 2:
                        output_grid[r, c] = 4  # Change to yellow
                        break  # Move to the next white pixel after finding one adjacency

    return output_grid.tolist()