import numpy as np
from collections import deque

"""
Identify the initial blue (1) object(s) in the input grid.
Perform a flood fill (using 4-way adjacency) starting from these blue pixels.
The fill expands into adjacent white (0) pixels.
The expansion is blocked by grid boundaries and yellow (4) pixels.
The final output grid contains the original yellow pixels, the original blue pixels, and the newly filled blue pixels.
"""

def transform(input_grid):
    """
    Performs a flood fill starting from blue pixels, expanding into white pixels,
    and stopping at grid boundaries or yellow pixels.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Initialize a queue for the flood fill (Breadth-First Search)
    frontier = deque()
    # Keep track of visited cells to avoid cycles and redundant processing
    visited = set()

    # Find initial blue pixels and add them to the frontier and visited set
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 1:  # Blue pixel
                coord = (r, c)
                if coord not in visited:
                    frontier.append(coord)
                    visited.add(coord)
                    # Ensure initial blue pixels are blue in the output (already true due to copy)
                    # output_grid[r, c] = 1

    # Define the 4 cardinal directions for neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Perform the flood fill
    while frontier:
        r, c = frontier.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_coord = (nr, nc)

                # Check if the neighbor has already been visited
                if neighbor_coord not in visited:
                    # Check if the neighbor is a white pixel in the *input* grid
                    # The fill should only propagate through white cells.
                    # Yellow cells (4) act as barriers implicitly because we only check for white (0).
                    if input_grid[nr, nc] == 0: # White pixel
                        # Change the neighbor pixel in the output grid to blue
                        output_grid[nr, nc] = 1
                        # Mark as visited
                        visited.add(neighbor_coord)
                        # Add to the frontier to explore from it later
                        frontier.append(neighbor_coord)
                    # If the neighbor is not white (e.g., yellow, black, or already blue from input),
                    # we don't fill it, but we should mark it as visited if it's not already,
                    # to prevent revisiting paths that lead to it. This is particularly important
                    # if barriers (like yellow) should completely stop exploration past them.
                    # Let's add non-white, non-visited neighbors to visited set so we don't reconsider them.
                    elif input_grid[nr, nc] != 1: # Don't re-add initial blue pixels unnecessarily
                         visited.add(neighbor_coord)


    return output_grid