"""
Identify all white (0) cells reachable from any white (0) border cell via 4-way adjacent white (0) cells, treating input azure (8) cells as barriers.
Create an output grid of the same size, initially filled with azure (8).
Set all the reachable white cells identified in the previous step to white (0) in the output grid.
All other cells (original barriers and unreachable white cells) remain azure (8) in the output.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a flood fill transformation to identify unreachable areas.

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        numpy.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize queue for Breadth-First Search (BFS)
    queue = deque()
    # visited_locations set keeps track of cells reachable from white border cells
    visited_locations = set()

    # --- Seed the BFS queue with starting points (white border cells) ---
    # Iterate through all border cells
    for r in range(height):
        for c in [0, width - 1]:  # Left and right borders
            # Check if the border cell is white (0) in the input
            if input_grid[r, c] == 0:
                # Only add if not already visited (handles corners)
                if (r, c) not in visited_locations:
                    visited_locations.add((r, c))
                    queue.append((r, c))

    for c in range(1, width - 1):  # Top and bottom borders (excluding corners)
         for r in [0, height - 1]:
            # Check if the border cell is white (0) in the input
            if input_grid[r, c] == 0:
                 if (r, c) not in visited_locations:
                    visited_locations.add((r, c))
                    queue.append((r, c))

    # --- Performing the Flood Fill (BFS) to find all reachable white cells ---
    # Define 4-way adjacent neighbors movements
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    while queue:
        # Get the next cell to process from the front of the queue
        r, c = queue.popleft()

        # Explore its neighbors
        for dr, dc in moves:
            nr, nc = r + dr, c + dc

            # Check 1: Is the neighbor within the grid boundaries?
            if 0 <= nr < height and 0 <= nc < width:
                # Check 2: Is the neighbor white (0) in the input grid (i.e., passable)?
                if input_grid[nr, nc] == 0:
                    # Check 3: Has the neighbor already been visited?
                    if (nr, nc) not in visited_locations:
                        # If all checks pass, this neighbor is reachable and passable
                        visited_locations.add((nr, nc)) # Mark as visited
                        queue.append((nr, nc)) # Add to queue for further exploration

    # --- Construct the output grid ---
    # Initialize output_grid filled entirely with azure (8)
    output_grid = np.full((height, width), 8, dtype=int)

    # Iterate through all the locations that were visited (reachable from border)
    for r, c in visited_locations:
        # Set these reachable locations to white (0) in the output grid
        output_grid[r, c] = 0

    # Cells that were not visited (original barriers or unreachable white cells)
    # remain azure (8) as initialized.
    return output_grid