import numpy as np
from collections import deque

"""
The transformation rule involves a flood fill operation originating from blue (1) pixels.
1. Initialize the output grid as a direct copy of the input grid.
2. Identify all pixels in the input grid that are blue (1). These form the initial "frontier" for the fill.
3. Identify all non-white (0) pixels (including the initial blue ones and any other colors like yellow (4)). These act as barriers or starting points and should not be overwritten, nor should the fill pass through them. Mark all these non-white pixels as "visited" initially.
4. Use a breadth-first search (BFS) approach starting from the initial blue pixels:
    a. While the frontier (queue) is not empty, take a pixel coordinate (r, c) from it.
    b. Examine its four cardinal neighbors (up, down, left, right).
    c. For each neighbor (nr, nc):
        i. Check if it's within the grid boundaries.
        ii. Check if it has already been visited.
        iii. If the neighbor is within bounds and not visited (meaning it must be a white pixel in the input):
            - Change the color of this neighbor pixel in the *output* grid to blue (1).
            - Mark the neighbor as visited.
            - Add the neighbor's coordinate to the frontier.
5. Continue the BFS until the frontier is empty.
6. Return the modified output grid.
"""


def transform(input_grid):
    """
    Performs a flood fill starting from blue pixels, expanding into adjacent
    white pixels, and stopping at grid boundaries or any non-white pixels (which act as barriers).

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
    # Keep track of visited cells to avoid cycles and redundant processing.
    # Initialize visited with all non-white cells; these are barriers or starting points.
    visited = set()

    # Scan the grid to find starting points (blue) and barriers (non-white)
    for r in range(height):
        for c in range(width):
            coord = (r, c)
            pixel_value = input_grid[r, c]

            if pixel_value == 1:  # Blue pixel (start point)
                # Check if already visited prevents adding duplicates if blue areas touch barriers
                if coord not in visited:
                    frontier.append(coord)
                    visited.add(coord)
            elif pixel_value != 0: # Any non-white pixel is a barrier
                 visited.add(coord) # Add barrier coordinates to visited

    # Define the 4 cardinal directions for neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Perform the flood fill (BFS)
    while frontier:
        r, c = frontier.popleft() # Get current pixel coordinates from the front of the queue

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc # Calculate neighbor coordinates

            # Check 1: Is the neighbor within grid boundaries?
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_coord = (nr, nc)

                # Check 2: Has the neighbor already been visited?
                # Visited includes initial blue, barriers (like yellow), and already filled white cells.
                if neighbor_coord not in visited:
                    # If we reach here, the neighbor MUST be white in the input and not yet processed.

                    # Fill the pixel blue in the output grid
                    output_grid[nr, nc] = 1
                    # Mark as visited
                    visited.add(neighbor_coord)
                    # Add to the frontier to explore from it later
                    frontier.append(neighbor_coord)

    return output_grid