"""
Transforms an input grid by replacing '0' pixels with the color of adjacent non-zero pixels, stopping propagation at the boundaries of different colored regions.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
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
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                neighbors = get_neighbors(input_grid, r, c)
                neighboring_colors = set()
                for nr, nc in neighbors:
                    if input_grid[nr, nc] != 0:
                        neighboring_colors.add(input_grid[nr, nc])

                if len(neighboring_colors) == 1:
                     output_grid[r,c] = neighboring_colors.pop()

    return output_grid