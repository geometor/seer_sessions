"""
Transforms an input grid by replacing '0' pixels with the color of adjacent non-zero pixels, stopping propagation at the boundaries of different colored regions.  Handles contested pixels (those with multiple different colored neighbors) by prioritizing colors that create closed "islands".
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

def is_closed_island(grid, r, c, color):
    """
    Checks if a '0' pixel at (r, c) is completely surrounded by 'color' pixels
    in the input_grid, forming a closed "island."
    """
    rows, cols = grid.shape
    visited = set()
    queue = [(r, c)]
    visited.add((r,c))

    while queue:
        curr_r, curr_c = queue.pop(0)

        neighbors = get_neighbors(grid, curr_r, curr_c)
        for nr, nc in neighbors:
            if (nr, nc) not in visited:
                if grid[nr, nc] == 0:
                  queue.append((nr,nc))
                  visited.add((nr, nc))
                elif grid[nr, nc] != color:
                    # If a neighbor isn't the target color or 0, it is not closed.
                    return False
    return True
    

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Iterative Filling (Single Neighbor)
    for _ in range(max(rows, cols)):  # Max iterations to ensure full propagation
        new_output_grid = np.copy(output_grid)
        for r in range(rows):
            for c in range(cols):
                if output_grid[r, c] == 0:
                    neighbors = get_neighbors(output_grid, r, c)
                    neighboring_colors = set()
                    for nr, nc in neighbors:
                        if output_grid[nr, nc] != 0:
                            neighboring_colors.add(output_grid[nr, nc])

                    if len(neighboring_colors) == 1:
                        new_output_grid[r, c] = neighboring_colors.pop()
        output_grid = new_output_grid

    # Contested Pixel Resolution (Multiple Neighbors)
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:
                neighbors = get_neighbors(output_grid, r, c)
                neighboring_colors = set()
                for nr, nc in neighbors:
                    if output_grid[nr, nc] != 0:
                        neighboring_colors.add(output_grid[nr, nc])

                if len(neighboring_colors) > 1:
                    for color in neighboring_colors:
                        if is_closed_island(input_grid, r, c, color):
                            output_grid[r,c] = color
                            break #prioritize first island color

    return output_grid