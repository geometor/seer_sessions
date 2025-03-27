"""
Identify barrier shapes (composed of red and blue pixels), solidify them by changing all blue pixels to red, then perform a flood fill starting from the single green pixel. The flood fill colors reachable azure pixels green, stopping at the solidified red barriers and the grid boundaries.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies the barrier solidification and flood fill transformation.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # --- 1. Solidify Barriers ---
    # Find all blue pixels (color 1) and change them to red (color 2)
    # In these examples, blue pixels only exist as part of barrier structures.
    output_grid[output_grid == 1] = 2

    # --- 2. Find Start Point ---
    # Locate the single green pixel (color 3)
    start_coords_list = np.where(input_grid == 3) # Use input_grid to find original start
    if len(start_coords_list[0]) == 0:
        # Handle cases where there might be no green pixel (though task implies one)
        return output_grid # Or raise an error, depending on requirements
    start_row, start_col = start_coords_list[0][0], start_coords_list[1][0]

    # --- 3. Flood Fill ---
    # Perform flood fill starting from the green pixel
    
    q = deque([(start_row, start_col)]) # Queue for BFS
    visited = set([(start_row, start_col)]) # Keep track of visited cells
    
    while q:
        r, c = q.popleft()

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor has already been visited
                if (nr, nc) not in visited:
                    # Check if the neighbor is not a barrier (red, color 2)
                    if output_grid[nr, nc] != 2:
                        # Mark as visited
                        visited.add((nr, nc))
                        # If the neighbor is azure (background, color 8), change it to green (3)
                        if output_grid[nr, nc] == 8:
                            output_grid[nr, nc] = 3
                        # Add the neighbor to the queue to explore from it
                        # We add it even if it was already green (the start point) or just turned green
                        # to ensure its neighbors are checked.
                        q.append((nr, nc))

    return output_grid