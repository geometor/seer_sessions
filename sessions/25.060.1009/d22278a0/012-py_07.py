"""
1.  **Determine Grid Dimensions:** Get the number of rows and columns of the input grid.

2.  **Create Checkerboard:** Generate a checkerboard pattern on a grid with the same dimensions as the input, alternating between green (3) and white (0) cells. A cell contains a green (3), if the sum of its row and column indices is even, else it is white (0).

3.  **Find Azure Starting Point:** Locate the azure (8) pixel in the input grid.

4.  **Flood Fill Azure:** Starting from the azure (8) pixel, flood fill outwards, replacing only white (0) cells. The flood fill expands with 8-connectivity (including diagonals). The fill is blocked by and therefore does not replace, the green (3) cells of the checkerboard. If a cell is not white (0), then do not expand to its neighbors.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Create Checkerboard
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                output_grid[r, c] = 3  # Green

    # Find initial azure cell
    azure_start = None
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:  # Azure
                azure_start = (r, c)
                break
        if azure_start:
            break

    # Flood Fill Azure
    if azure_start:
        queue = [azure_start]
        while queue:
            r, c = queue.pop(0)
            if output_grid[r, c] == 0:  # Only fill white cells
                output_grid[r, c] = 8  # Azure
                # Add neighbors to queue (8-connectivity)
                neighbors = [
                    (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
                    (r + 1, c + 1), (r - 1, c - 1), (r + 1, c - 1), (r - 1, c + 1)
                ]
                for nr, nc in neighbors:
                    if 0 <= nr < rows and 0 <= nc < cols:  # Check bounds
                        queue.append((nr, nc))

    return output_grid