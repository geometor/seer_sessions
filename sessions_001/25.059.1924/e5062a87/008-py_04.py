"""
1.  **Identify Initial Seeds:** Locate all red (2) pixels in the input grid. These are the starting points for expansion.

2.  **Iterative Expansion:** For each initial red pixel and *every* subsequently changed pixel:
    *   Examine its eight neighboring pixels (horizontal, vertical, and diagonal).
    *   If a neighboring pixel is gray (5), change it to red (2) in the output grid.

3.  **Termination Condition:** Repeat step 2 until no more gray pixels adjacent to any red pixels can be found. The expansion stops when there are no gray pixels neighboring any red pixels.
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
    """Transforms the input grid by iteratively expanding red pixels into adjacent gray areas."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find initial red pixels
    red_pixels = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 2:
                red_pixels.append((r, c))

    # Iterative expansion
    while True:
        new_red_pixels = []
        for r, c in red_pixels:
            neighbors = get_neighbors(output_grid, r, c)
            for nr, nc in neighbors:
                if output_grid[nr, nc] == 5:
                    output_grid[nr, nc] = 2
                    new_red_pixels.append((nr, nc))
        
        if not new_red_pixels:  # Termination condition: No new red pixels were added
            break
        
        red_pixels.extend(new_red_pixels) # Add the newly changed pixels for next iteration's expansion

    return output_grid