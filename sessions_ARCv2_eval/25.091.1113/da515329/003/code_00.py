import numpy as np
from collections import deque

"""
Performs a flood fill starting from the white (0) border cells of the input grid.
Azure (8) cells in the input act as impassable barriers.
The output grid marks all cells reachable from the white border cells (without crossing barriers) as azure (8).
All other cells in the output grid, including the original barrier locations and any enclosed white areas, become white (0).
"""

def transform(input_grid):
    """
    Applies a flood fill from the white border cells, constrained by azure barriers.

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        numpy.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output_grid with white (0) - this will be the final grid
    output_grid = np.zeros((height, width), dtype=int)

    # Identify barrier locations (azure pixels in input) for quick lookup
    # We don't need a separate set if we check input_grid directly during BFS
    # barrier_locations = set()
    # for r in range(height):
    #     for c in range(width):
    #         if input_grid[r, c] == 8:
    #             barrier_locations.add((r, c))

    # Initialize queue for Breadth-First Search (BFS) and visited set
    queue = deque()
    # visited set keeps track of cells added to queue/processed to prevent cycles and redundant work
    visited = set()
    # reachable_locations set stores all cells reachable from the border
    # We can directly modify the output grid instead of using a separate set
    # reachable_locations = set()

    # --- Seeding the BFS ---
    # Iterate through all border cells
    for r in range(height):
        for c in [0, width - 1]:  # Left and right borders
            # Check if the border cell is NOT a barrier (i.e., is white 0) and hasn't been visited
            if input_grid[r, c] == 0 and (r, c) not in visited:
                visited.add((r, c))
                queue.append((r, c))
                # Mark this starting cell as reachable in the output grid
                output_grid[r, c] = 8

    for c in range(1, width - 1):  # Top and bottom borders (excluding corners already checked)
         for r in [0, height - 1]:
            # Check if the border cell is NOT a barrier and hasn't been visited
            if input_grid[r, c] == 0 and (r, c) not in visited:
                visited.add((r, c))
                queue.append((r, c))
                # Mark this starting cell as reachable in the output grid
                output_grid[r, c] = 8

    # --- Performing the Flood Fill (BFS) ---
    # Define 4-way adjacent neighbors movements
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    while queue:
        # Get the next cell to process
        r, c = queue.popleft()

        # Explore its neighbors
        for dr, dc in moves:
            nr, nc = r + dr, c + dc

            # Check 1: Is the neighbor within the grid boundaries?
            if 0 <= nr < height and 0 <= nc < width:
                # Check 2: Has the neighbor already been visited?
                if (nr, nc) not in visited:
                    # Check 3: Is the neighbor NOT a barrier in the input grid?
                    if input_grid[nr, nc] == 0:
                        # If all checks pass, this neighbor is reachable
                        visited.add((nr, nc)) # Mark as visited
                        queue.append((nr, nc)) # Add to queue for further exploration
                        # Mark this reachable cell in the output grid
                        output_grid[nr, nc] = 8

    # After the BFS, output_grid contains azure (8) for all reachable cells
    # and retains the initial white (0) for barriers and unreachable areas.
    return output_grid