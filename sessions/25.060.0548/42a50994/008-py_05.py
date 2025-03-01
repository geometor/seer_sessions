"""
1.  **Identify Azure Objects:** Locate all contiguous groups of azure (8) pixels in the input grid.  These form distinct objects.
2.  **Remove Objects:** Remove *all* pixels of *all* identified azure objects.
3.  **Output:** The output grid is the input grid with all azure pixels replaced with white (0) pixels.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def get_object_pixels(grid, start_row, start_col, color):
    """
    Gets the pixels of a contiguous object of a given color,
    starting from a given cell. Uses flood fill algorithm.
    Returns a list of (row, col) tuples.
    """

    rows, cols = grid.shape
    pixels = []
    visited = set()
    queue = [(start_row, start_col)]

    while queue:
        row, col = queue.pop(0)

        if (row, col) in visited:
            continue
        visited.add((row, col))
        pixels.append((row, col))

        for nr, nc in get_neighbors(grid, row, col):
            if grid[nr, nc] == color and (nr, nc) not in visited:
                queue.append((nr, nc))
    return pixels

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    azure = 8

    # Iterate over all pixels
    for r in range(rows):
        for c in range(cols):
            # Identify and remove azure objects
            if output_grid[r, c] == azure:
                object_pixels = get_object_pixels(output_grid, r, c, azure)
                for row, col in object_pixels:
                    output_grid[row, col] = 0  # Remove all pixels in the object

    return output_grid