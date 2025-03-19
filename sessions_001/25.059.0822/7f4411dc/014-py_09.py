"""
1.  **Identify Magenta Pixels:** Find all pixels colored magenta (6) in the input grid.

2.  **Preserve Contiguous Blocks:** If magenta pixels form a contiguous block (horizontally or vertically adjacent) of *any* size, preserve all pixels within that block.

3.  **All Other Pixels:** All other pixels (non-magenta) in the output grid should be white (0).
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))  # Up
    if r < rows - 1:
        neighbors.append((r + 1, c))  # Down
    if c > 0:
        neighbors.append((r, c - 1))  # Left
    if c < cols - 1:
        neighbors.append((r, c + 1))  # Right
    return neighbors

def flood_fill(grid, r, c, visited):
    """Performs a flood fill to identify a contiguous block of magenta pixels."""
    rows, cols = grid.shape
    if (r, c) in visited or grid[r, c] != 6:
        return []

    block = []
    stack = [(r, c)]
    visited.add((r,c))

    while stack:
        current_r, current_c = stack.pop()
        block.append((current_r, current_c))

        for neighbor_r, neighbor_c in get_neighbors(grid, current_r, current_c):
            if (neighbor_r, neighbor_c) not in visited and grid[neighbor_r, neighbor_c] == 6:
                stack.append((neighbor_r, neighbor_c))
                visited.add((neighbor_r, neighbor_c))
    return block

def transform(input_grid):
    """
    Transforms the input grid based on the rules.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)  # Initialize with white (0)

    # Identify all magenta pixels
    magenta_pixels = [(r, c) for r in range(rows) for c in range(cols) if input_grid[r, c] == 6]
    visited = set()


    # contiguous blocks
    for r, c in magenta_pixels:
        if (r,c) not in visited:
            magenta_block = flood_fill(input_grid, r, c, visited)
            if len(magenta_block) > 0: # if any size, preserve
                for pixel_r, pixel_c in magenta_block:
                    output_grid[pixel_r, pixel_c] = 6

    return output_grid.tolist()