"""
Perform a flood fill operation starting from all initial red pixels (color 2).
The fill color is red (2).
The fill spreads to adjacent (up, down, left, right) white pixels (color 0).
The fill is blocked by azure pixels (color 8) and the grid boundaries.
The original red and azure pixels remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a flood fill starting from red pixels, constrained by azure pixels.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed grid.
    """
    # Convert input grid to a NumPy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Initialize output_grid as a copy of the input
    height, width = grid.shape

    # Initialize a queue for the flood fill algorithm
    queue = deque()

    # Find all initial red pixels (color 2) and add them to the queue
    # These are the starting points for the fill
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 2:
                # We add the initial red seeds to the queue to start the process,
                # but we don't need to change their color as they are already red.
                # The algorithm will explore their neighbors.
                queue.append((r, c))

    # Define the four cardinal directions for neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Perform the flood fill
    while queue:
        r, c = queue.popleft() # Get the next pixel to process

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor pixel in the output_grid is white (0)
                # We check the output_grid because we modify it in place.
                # We don't fill if the neighbor is already red (2) or azure (8)
                if output_grid[nr, nc] == 0:
                    # Change the neighbor's color to red (2)
                    output_grid[nr, nc] = 2
                    # Add the newly colored neighbor to the queue to process its neighbors
                    queue.append((nr, nc))

    # Convert the NumPy array back to a list of lists for the final output
    return output_grid.tolist()