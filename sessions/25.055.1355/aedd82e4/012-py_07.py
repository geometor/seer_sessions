"""
1.  **Preserve Reds:** All red pixels in the input grid remain red in the output grid.
2.  **Initial Blue:** White pixels directly adjacent (horizontally or vertically) to a red pixel become blue. These initial blue pixels are "spreading centers".
3. **Limited Propagation:** White pixels that are directly adjacent (horizontally and vertically) to any "spreading center" change to blue, becoming spreading centers *only* if they are adjacent to the original red or to pixels that were adjacent to red. The propagation only goes one step away from the initial blue created.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Gets the valid neighbors (up, down, left, right) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))
    if r < rows - 1:
        neighbors.append((r + 1, c))
    if c > 0:
        neighbors.append((r, c - 1))
    if c < cols - 1:
        neighbors.append((r, c + 1))
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Create sets to store coordinates
    red_pixels = set()
    initial_blue_pixels = set()

    # Identify red pixels and initial blue candidates
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 2:  # Red pixel
                red_pixels.add((r, c))
            elif output_grid[r, c] == 0: # White pixel
                for nr, nc in get_neighbors(output_grid, r, c):
                    if output_grid[nr, nc] == 2:
                        initial_blue_pixels.add((r, c))
                        break  # Once a white is adjacent to red, it's in the set

    # Set initial blue pixels
    for r, c in initial_blue_pixels:
        output_grid[r, c] = 1
        
    # Propagate one step
    new_blue_pixels = set()
    for r, c in initial_blue_pixels:
        for nr, nc in get_neighbors(output_grid, r, c):
            if output_grid[nr, nc] == 0:
                new_blue_pixels.add((nr,nc))

    for r,c in new_blue_pixels:
        output_grid[r,c] = 1

    return output_grid