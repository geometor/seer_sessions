"""
1.  **Identify the Object:** Locate all orange (7) pixels in the input grid.
2.  **Surround with Azure:** For each orange (7) pixel:
    a. Change any directly adjacent pixels (up, down, left, right, and diagonal) to azure (8).
3.  **Wrap around:** If an orange pixel touches the edge of the grid, extend the surrounding azure color to the opposite side of the grid as needed.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Find all orange pixels.
    orange_pixels = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 7:
                orange_pixels.append((r, c))

    # Iterate through orange pixels and surround with azure.
    for r, c in orange_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                nr, nc = r + dr, c + dc

                # Wrap around logic
                if nr < 0:
                    nr = rows - 1
                elif nr >= rows:
                    nr = 0

                if nc < 0:
                    nc = cols - 1
                elif nc >= cols:
                    nc = 0

                output_grid[nr, nc] = 8

    return output_grid