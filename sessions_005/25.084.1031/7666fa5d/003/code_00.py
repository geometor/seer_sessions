import numpy as np
from collections import deque

# Define background and fill colors for clarity
BACKGROUND_COLOR = 8
FILL_COLOR = 2

"""
Identify all pixels in the input grid that are not the background color (Azure 8). 
These are the "boundary pixels". Then, identify all background pixels (Azure 8) 
that are "enclosed" by these boundary pixels. An enclosed pixel is one that cannot 
reach the border of the grid by moving only through other background pixels 
(horizontally or vertically). Change the color of these enclosed background pixels 
to Red 2. All other pixels (boundary pixels and non-enclosed background pixels) 
retain their original color.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Fills enclosed background regions with Red 2.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid with enclosed areas filled.
    """
    rows, cols = input_grid.shape
    # Initialize output_grid as a copy of the input grid.
    # We will modify this grid directly where needed.
    output_grid = np.copy(input_grid)

    # Create a boolean grid to keep track of visited background pixels
    # during the flood fill. Initialize all to False.
    visited = np.zeros((rows, cols), dtype=bool)

    # Initialize a queue for Breadth-First Search (BFS) flood fill.
    # deque is efficient for pop(0).
    queue = deque()

    # Seed the flood fill from all background pixels on the border.
    # Iterate through top and bottom rows.
    for c in range(cols):
        if input_grid[0, c] == BACKGROUND_COLOR and not visited[0, c]:
            visited[0, c] = True
            queue.append((0, c))
        if rows > 1 and input_grid[rows - 1, c] == BACKGROUND_COLOR and not visited[rows - 1, c]:
            visited[rows - 1, c] = True
            queue.append((rows - 1, c))

    # Iterate through left and right columns (excluding corners already checked).
    for r in range(1, rows - 1):
        if input_grid[r, 0] == BACKGROUND_COLOR and not visited[r, 0]:
            visited[r, 0] = True
            queue.append((r, 0))
        if cols > 1 and input_grid[r, cols - 1] == BACKGROUND_COLOR and not visited[r, cols - 1]:
            visited[r, cols - 1] = True
            queue.append((r, cols - 1))

    # Define the 4 cardinal directions for neighbors (row_change, col_change)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform the BFS flood fill from the border background pixels.
    while queue:
        r, c = queue.popleft() # Get the next pixel to process

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is a background pixel and hasn't been visited
                if input_grid[nr, nc] == BACKGROUND_COLOR and not visited[nr, nc]:
                    # Mark as visited and add to the queue
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    # Now, iterate through the entire grid.
    # Any background pixel that was *not* visited by the flood fill
    # must be enclosed.
    for r in range(rows):
        for c in range(cols):
            # Check if it's a background pixel in the input
            if input_grid[r, c] == BACKGROUND_COLOR:
                # Check if it was NOT reached by the flood fill (i.e., it's enclosed)
                if not visited[r, c]:
                    # Change its color in the output grid to the fill color
                    output_grid[r, c] = FILL_COLOR

    # Return the modified grid
    return output_grid