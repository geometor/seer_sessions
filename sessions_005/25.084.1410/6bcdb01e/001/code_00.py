import numpy as np
from collections import deque

"""
Identifies connected regions of orange (7) pixels that are adjacent (including diagonally) 
to any initial green (3) pixel. Changes these reachable orange pixels to green (3). 
Azure (8) pixels and grid boundaries act as barriers, preventing the spread of green. 
All other pixels remain unchanged.

The process uses a breadth-first search (BFS) starting from all initial green pixels.
"""

def transform(input_grid):
    """
    Performs a flood fill transformation starting from green pixels.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    np_input = np.array(input_grid, dtype=int)
    output_grid = np_input.copy()
    height, width = np_input.shape

    # Define the colors
    GREEN = 3
    ORANGE = 7
    # AZURE = 8 # Implicit barrier, along with other colors and boundaries

    # Initialize a queue for BFS and a set to track visited cells
    # The queue will store coordinates (row, col) to explore *from*
    # Visited will store coordinates that have been added to the queue (or were initial green)
    # to prevent redundant processing and cycles.
    q = deque()
    visited = set()

    # Find all initial green pixels and add them to the queue and visited set
    # These are the starting points for the expansion.
    for r in range(height):
        for c in range(width):
            if np_input[r, c] == GREEN:
                q.append((r, c))
                visited.add((r, c))

    # Define the 8 directions for neighbors (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Perform BFS
    while q:
        # Get the current cell coordinate to explore from
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is an orange pixel and hasn't been visited/queued yet
                if np_input[nr, nc] == ORANGE and (nr, nc) not in visited:
                    # Mark the neighbor as visited
                    visited.add((nr, nc))
                    # Change the color in the output grid to green
                    output_grid[nr, nc] = GREEN
                    # Add the neighbor to the queue to explore from it later
                    q.append((nr, nc))

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()