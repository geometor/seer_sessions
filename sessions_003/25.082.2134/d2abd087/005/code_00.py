"""
Transforms an input grid by identifying connected regions of gray (5) pixels (gray islands) and coloring them in a checkerboard pattern of red (2) and blue (1). The starting color for each island is determined by examining its surrounding colored neighbors, ensuring a global checkerboard pattern across islands.
"""

import numpy as np
from collections import deque

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a pixel (including diagonals)."""
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def determine_start_color(grid, row, col, visited):
    """Determines the starting color (1 or 2) for a gray island using BFS."""
    queue = deque([(row, col)])
    visited_bfs = set()
    visited_bfs.add((row, col))

    while queue:
        r, c = queue.popleft()

        neighbors = get_neighbors(grid, r, c)
        for nr, nc in neighbors:
            if (nr, nc) not in visited_bfs:
                visited_bfs.add((nr, nc))
                if grid[nr][nc] == 1:
                    return 2  # Adjacent to blue, start with red
                elif grid[nr][nc] == 2:
                    return 1  # Adjacent to red, start with blue
                elif grid[nr][nc] == 5 and (nr, nc) not in visited:
                    queue.append((nr,nc))
    return 1  # No colored neighbors found, default to blue

def flood_fill(grid, row, col, target_color, replacement_color, visited):
    """Performs a flood fill operation, directly applying the replacement color."""
    rows, cols = len(grid), len(grid[0])
    if (row < 0 or row >= rows or col < 0 or col >= cols or
            (row, col) in visited or grid[row][col] != target_color):
        return
    visited.add((row, col))
    grid[row][col] = replacement_color

    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        flood_fill(grid, r, c, target_color, replacement_color, visited)


def transform(input_grid):
    # Initialize output_grid as a *copy* of the input
    output_grid = np.copy(input_grid).tolist()
    rows, cols = len(output_grid), len(output_grid[0])

    # Keep track of visited pixels (for flood fill)
    visited = set()

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Process only unvisited gray pixels
            if output_grid[r][c] == 5 and (r, c) not in visited:
                # Determine checkerboard start color using BFS
                start_color = determine_start_color(output_grid, r, c, visited)

                # Flood fill with the determined color
                flood_fill(output_grid, r, c, 5, start_color, visited)

    return output_grid