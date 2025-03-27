"""
The transformation propagates magenta (6) from existing magenta pixels to adjacent orange (7) pixels. 
The propagation is guided by the presence of red (2) pixels, but does not require the new magenta pixel to be directly adjacent to red. 
The propagation can occur horizontally, vertically, and diagonally. The propagation stops when no more orange pixels are adjacent to 
magenta, considering the entire configuration.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterative propagation of magenta.
    while True:
        changed = False
        new_grid = np.copy(output_grid)  # Work on a copy to process each step correctly
        for r in range(rows):
            for c in range(cols):
                if output_grid[r, c] == 7:  # Check if it's orange.
                    # Check for adjacency to magenta (horizontally, vertically, or diagonally).
                    adjacent_to_magenta = False
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if output_grid[nr, nc] == 6:
                                adjacent_to_magenta = True
                                break

                    if adjacent_to_magenta:
                        new_grid[r,c] = 6
                        changed = True


        output_grid = new_grid
        if not changed:  # Stop if no changes occurred in this iteration.
            break

    return output_grid