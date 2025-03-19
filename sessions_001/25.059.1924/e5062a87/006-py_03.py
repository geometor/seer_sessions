"""
1.  **Identify Initial Seeds:** Locate all red (2) pixels in the input grid *before* any changes are made.

2.  **Single Expansion:** For each initial red pixel:
    *   Examine its eight neighboring pixels (horizontal, vertical, and diagonal).
    *   If a neighboring pixel is gray (5), change it to red (2) in the output grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the coordinates of the eight neighbors of a pixel."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row = row + i
            neighbor_col = col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def transform(input_grid):
    """Transforms the input grid by expanding red pixels into adjacent gray areas once."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Find initial red pixels
    initial_red_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:
                initial_red_pixels.append((r, c))
    
    # Expand from initial red pixels
    for r, c in initial_red_pixels:
        neighbors = get_neighbors(input_grid, r, c)  # Use input_grid for neighbor checking
        for nr, nc in neighbors:
            if input_grid[nr, nc] == 5:  # Check the input_grid for gray pixels
                output_grid[nr, nc] = 2  # Modify the output_grid

    return output_grid