import numpy as np
from collections import deque

"""
Identifies contiguous regions of white pixels (0) enclosed by blue pixels (1)
and changes their color to red (2). This is achieved by performing a flood fill
from the boundary white pixels to identify all 'exterior' white pixels. Any
white pixel not reached by the flood fill is considered 'enclosed' and is
recolored.
"""

def transform(input_grid):
    """
    Fills enclosed white regions with red.

    Args:
        input_grid (list[list[int]]): The input 2D grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()  # Initialize output_grid as a copy
    height, width = grid.shape

    # Constants for colors
    background_color = 0  # white
    boundary_color = 1  # blue
    fill_color = 2  # red

    # Keep track of visited white pixels connected to the boundary
    visited = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # Add all boundary white pixels to the queue and mark as visited
    for r in range(height):
        for c in [0, width - 1]:  # Left and right boundaries
            if grid[r, c] == background_color and not visited[r, c]:
                visited[r, c] = True
                queue.append((r, c))
    for c in range(width):
        for r in [0, height - 1]: # Top and bottom boundaries
            if grid[r, c] == background_color and not visited[r, c]:
                visited[r, c] = True
                queue.append((r, c))

    # Perform Breadth-First Search (BFS) to find all reachable white pixels (exterior)
    while queue:
        r, c = queue.popleft()

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is white and not visited
                if grid[nr, nc] == background_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    # Iterate through the grid and change enclosed white pixels to red
    for r in range(height):
        for c in range(width):
            # If a pixel is white and was not visited by the BFS, it's enclosed
            if grid[r, c] == background_color and not visited[r, c]:
                output_grid[r, c] = fill_color

    # Convert back to list of lists before returning
    return output_grid.tolist()