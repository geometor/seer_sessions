import numpy as np
from collections import deque

"""
The transformation rule involves a flood fill operation originating from blue (1) pixels.
1. Initialize the output grid as a direct copy of the input grid.
2. Identify all pixels in the input grid that are blue (1). These form the initial "frontier" for the fill and are marked as "visited".
3. Use a breadth-first search (BFS) approach:
    a. While the frontier is not empty, take a pixel coordinate (r, c) from it.
    b. Examine its four cardinal neighbors (up, down, left, right).
    c. For each neighbor (nr, nc):
        i. Check if it's within the grid boundaries.
        ii. Check if it has already been visited.
        iii. Check if the neighbor's color in the *input* grid is white (0).
        iv. If the neighbor is within bounds, not visited, AND is white (0) in the input:
            - Change the color of this neighbor pixel in the *output* grid to blue (1).
            - Mark the neighbor as visited.
            - Add the neighbor's coordinate to the frontier.
        v. If the neighbor is within bounds, not visited, BUT is *not* white (0) in the input (e.g., it's yellow(4) or another color):
            - Mark the neighbor as visited to avoid reprocessing paths leading to it, but do not change its color or add it to the frontier. This effectively makes non-white cells barriers.
4. Continue the BFS until the frontier is empty.
5. Return the modified output grid.
"""

def transform(input_grid):
    """
    Performs a flood fill starting from blue pixels, expanding into adjacent
    white pixels, and stopping at grid boundaries or any non-white pixels.

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
    # Initialize visited with non-white cells initially, as they are barriers
    # and also add initial blue cells as they are the starting points.
    visited = set()

    # Find initial blue pixels and add them to the frontier and visited set
    # Also identify barriers (non-white cells) and add them to visited initially.
    for r in range(height):
        for c in range(width):
            coord = (r, c)
            if input_grid[r, c] == 1:  # Blue pixel (start point)
                if coord not in visited: # Should not happen if logic below is sound, but safe check
                    frontier.append(coord)
                    visited.add(coord)
            elif input_grid[r, c] != 0: # Any non-white pixel is a barrier
                 visited.add(coord)


    # Define the 4 cardinal directions for neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Perform the flood fill (BFS)
    while frontier:
        r, c = frontier.popleft() # Get current pixel coordinates

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc # Calculate neighbor coordinates

            # Check 1: Is the neighbor within grid boundaries?
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_coord = (nr, nc)

                # Check 2: Has the neighbor already been visited?
                # Visited includes initial blue, barriers, and already filled cells.
                if neighbor_coord not in visited:
                    # Check 3: Is the neighbor a white pixel in the *input* grid?
                    # This check is implicitly handled because non-white cells were added to visited initially.
                    # If we reach here, the neighbor MUST be white in the input and not visited.
                    
                    # Fill the pixel blue in the output grid
                    output_grid[nr, nc] = 1
                    # Mark as visited
                    visited.add(neighbor_coord)
                    # Add to the frontier to explore from it later
                    frontier.append(neighbor_coord)

                    # Note: The previous code had an elif condition to add barriers to visited here.
                    # That is now handled by pre-populating visited with all non-white cells.
                    # This simplifies the loop logic slightly.

    return output_grid