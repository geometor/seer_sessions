"""
1. **Identify Centers:** Locate all non-zero pixels in the input grid. These are the "center" pixels.
2. **Red Center Expansion:** For each pixel with the value '2' (red) in the input grid, place pixels of value '4' (yellow) directly above, below, and to the left and right of it in the output grid. Do not replace the original '2'.
3. **Blue Center Expansion:** For each pixel with the value '1' (blue) in the input grid, place pixels with the value '7' (orange) directly above, below, to the left, and to the right of it in the output grid. Do not replace the original '1'.
4.  **Preserve Zeros:** All '0' (white) pixels in the input that do not have colored pixels placed over them, remain '0' in the output.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    get the neighbor coordinates of the current cell
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Above
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Below
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid
    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            # Find center pixels (non-zero pixels)
            if input_grid[row, col] == 2:
                # Expand red center with yellow (4)
                for r, c in get_neighbors(input_grid, row, col):
                    output_grid[r,c] = 4

            elif input_grid[row, col] == 1:
                # Expand blue center with orange (7)
                for r, c in get_neighbors(input_grid, row, col):
                    output_grid[r, c] = 7
    return output_grid