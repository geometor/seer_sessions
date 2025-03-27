import numpy as np
from collections import deque

"""
Identify pixels with the seed color (Green, 3) and perform a flood fill operation 
on adjacent pixels with the fillable color (Orange, 7). The fill stops at grid 
boundaries and pixels with the boundary color (Azure, 8).
"""

def transform(input_grid):
    """
    Applies a flood fill transformation based on seed, fillable, and boundary colors.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Define colors
    boundary_color = 8  # Azure
    seed_color = 3      # Green
    fillable_color = 7  # Orange
    fill_color = 3      # Green

    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Initialize data structures for flood fill
    queue = deque()
    visited = set() # Keep track of visited fillable cells to avoid cycles

    # Find initial seed points and add them to the queue
    # Note: Seed points themselves don't change color, but they initiate the fill.
    # We need to add the *neighbors* of the seed points if they are fillable,
    # or alternatively, add the seed points and let the main loop handle neighbors.
    # Let's add the seed points themselves. The fill logic will then check neighbors.
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == seed_color:
                # Although seed points don't change, we add them to the queue
                # to start the exploration of their neighbors.
                # We also add them to visited to prevent re-adding if they are adjacent to another seed.
                if (r, c) not in visited:
                     queue.append((r, c))
                     visited.add((r, c)) # Mark seed points as visited conceptually

    # Perform Breadth-First Search (BFS) flood fill
    while queue:
        r, c = queue.popleft()

        # Explore the 4 adjacent neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is a fillable color
                if output_grid[nr, nc] == fillable_color:
                     # Check if the neighbor hasn't been visited yet
                    if (nr, nc) not in visited:
                        # Change the neighbor's color to the fill color
                        output_grid[nr, nc] = fill_color
                        # Mark the neighbor as visited
                        visited.add((nr, nc))
                        # Add the neighbor to the queue to explore from it
                        queue.append((nr, nc))
                # Note: We don't need an explicit check for boundary_color here,
                # because the condition `output_grid[nr, nc] == fillable_color`
                # inherently prevents filling across boundaries or other colors.
                # We also mark already-filled (green) neighbors as visited if encountered,
                # to prevent re-adding them to the queue if they were neighbors of the initial seeds.
                elif output_grid[nr, nc] == seed_color or output_grid[nr, nc] == fill_color:
                     if (nr, nc) not in visited:
                         visited.add((nr, nc)) # Mark existing green cells as visited too.


    # Return the modified grid
    return output_grid