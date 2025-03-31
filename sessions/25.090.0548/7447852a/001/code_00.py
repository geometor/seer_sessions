import numpy as np
from collections import deque

"""
Identify white pixels (0) that are 'enclosed' by red pixels (2) and cannot reach the grid boundary by moving horizontally or vertically through other white pixels. Change these enclosed white pixels to yellow (4). Leave all other pixels (red pixels and white pixels connected to the boundary) unchanged.

1. Copy the input grid to create the output grid.
2. Find all white pixels located on the boundary (edges) of the grid.
3. Perform a flood fill (BFS or DFS) starting from these boundary white pixels, marking all reachable white pixels. Only move horizontally or vertically.
4. Iterate through the grid. Any white pixel that was not reached during the flood fill is considered enclosed.
5. Change the color of these enclosed white pixels to yellow in the output grid.
6. Return the modified output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by flood-filling white areas connected to the boundary
    and changing the color of unconnected (enclosed) white areas to yellow.
    """
    # Convert input list of lists to numpy array for easier handling
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # Define colors
    WHITE = 0
    RED = 2
    YELLOW = 4

    # Keep track of visited white cells reachable from the boundary
    visited = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # Find initial white cells on the boundary
    for r in range(height):
        if grid[r, 0] == WHITE and not visited[r, 0]:
            queue.append((r, 0))
            visited[r, 0] = True
        if grid[r, width - 1] == WHITE and not visited[r, width - 1]:
            queue.append((r, width - 1))
            visited[r, width - 1] = True
            
    for c in range(width):
        if grid[0, c] == WHITE and not visited[0, c]:
            queue.append((0, c))
            visited[0, c] = True
        if grid[height - 1, c] == WHITE and not visited[height - 1, c]:
             queue.append((height - 1, c))
             visited[height - 1, c] = True

    # Perform BFS (flood fill) from boundary white cells
    while queue:
        r, c = queue.popleft()

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is white and not visited
                if grid[nr, nc] == WHITE and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    # Iterate through the grid and change unconnected white cells to yellow
    for r in range(height):
        for c in range(width):
            # If a cell is white but was not visited by the flood fill (not connected to boundary)
            if grid[r, c] == WHITE and not visited[r, c]:
                output_grid[r, c] = YELLOW # Change it to yellow

    # Convert back to list of lists if necessary, depending on expected output format
    # return output_grid.tolist() 
    return output_grid
