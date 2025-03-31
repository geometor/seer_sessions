"""
Perform a flood fill operation starting from green (3) pixels. 
The fill color is green (3).
The fill only affects white (0) pixels.
Red (2) pixels act as barriers and are not changed or crossed.
The original green (3) pixels also remain unchanged.
The fill spreads to 4-directionally adjacent (up, down, left, right) white pixels.
The fill stops at grid boundaries and red pixels.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a flood fill starting from green pixels (3), filling white pixels (0) 
    and stopping at red pixels (2) and grid boundaries.
    
    Args:
        input_grid (list of lists or np.ndarray): The input grid.
        
    Returns:
        np.ndarray: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = input_np.copy()
    height, width = input_np.shape

    # Initialize a queue for BFS flood fill
    queue = deque()
    
    # Keep track of visited cells to avoid cycles and redundant work
    visited = set()

    # Find initial green pixels (starting points) and add them to the queue and visited set
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 3:
                start_point = (r, c)
                if start_point not in visited:
                    queue.append(start_point)
                    visited.add(start_point)

    # Define 4-directional neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Perform Breadth-First Search (BFS) based flood fill
    while queue:
        # Get the current cell from the front of the queue
        r, c = queue.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor has not been visited yet
                if (nr, nc) not in visited:
                    # Check if the neighbor in the *original* grid is white (0), which is fillable
                    if input_np[nr, nc] == 0:
                        # Change the color of the neighbor in the output grid to green (3)
                        output_grid[nr, nc] = 3
                        # Mark the neighbor as visited
                        visited.add((nr, nc))
                        # Add the neighbor to the queue to process its neighbors later
                        queue.append((nr, nc))
                    # Also add red pixels to visited so we don't try to process them
                    elif input_np[nr, nc] == 2:
                         visited.add((nr, nc))


    return output_grid.tolist() # Return as list of lists if required by the framework