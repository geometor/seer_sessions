"""
1.  **Identify Azure Pixels:** Locate all pixels with the value '8' (azure) within the input grid.

2.  **Conditional Removal**:
    *   Iterate over azure pixels.
    *   If an azure forms a solid rectangle with a width or height greater than one, remove the azure pixels along the bottom edge of that shape.
    *   If an azure pixel has 2 or more non-azure neighbors, remove it.

3.  **Output:** Generate the modified grid, where the selected azure pixels have been replaced with '0' (white).
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

def get_object_bounds(grid, start_row, start_col, color):
    """
    Gets the bounding box of a contiguous object of a given color,
    starting from a given cell.  Uses flood fill algorithm.
    Returns (min_row, max_row, min_col, max_col)
    """

    rows, cols = grid.shape
    min_row, max_row = start_row, start_row
    min_col, max_col = start_col, start_col

    visited = set()
    queue = [(start_row, start_col)]

    while queue:
        row, col = queue.pop(0)

        if (row, col) in visited:
            continue
        visited.add((row, col))

        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

        for nr, nc in get_neighbors(grid, row, col):
            if grid[nr, nc] == color and (nr, nc) not in visited:
                queue.append((nr, nc))
    return (min_row, max_row, min_col, max_col)
    

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    azure = 8

    # Iterate over all azure pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == azure:
                # Remove bottom row of large rectangles
                min_row, max_row, min_col, max_col = get_object_bounds(output_grid, r, c, azure)

                if max_row - min_row > 0 or max_col - min_col > 0:
                    if r == max_row:
                        output_grid[r,c] = 0

                # Remove pixel with 2 or more non-azure neighbors
                neighbor_count = 0
                for nr, nc in get_neighbors(output_grid, r,c):
                    if output_grid[nr, nc] != azure:
                        neighbor_count += 1
                if neighbor_count >= 2:
                    output_grid[r,c] = 0

    return output_grid