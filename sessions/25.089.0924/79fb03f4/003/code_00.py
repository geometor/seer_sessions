"""
Perform a flood fill operation starting from all blue (1) pixels in the input grid.
The fill color is blue (1) and it expands into adjacent (up, down, left, right) 
white (0) pixels. The fill stops at the grid boundaries or any non-white (0) 
pixels (e.g., gray 5, azure 8), which act as barriers. All original non-white 
pixels retain their color and position.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a flood fill operation starting from blue pixels (1).

    Args:
        input_grid (list of lists): The input grid representing pixel colors.

    Returns:
        list of lists: The transformed grid with white areas connected to blue pixels
                       filled with blue, bounded by non-white pixels or grid edges.
    """
    # Convert input to numpy array for easier indexing and manipulation
    np_input_grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(np_input_grid)
    height, width = output_grid.shape

    # Initialize queue for BFS flood fill
    queue = deque()
    
    # Initialize a set to track visited coordinates. 
    # Add all non-white pixels initially, as they are boundaries or starting points 
    # and should not be filled or added to the queue again.
    visited = set()
    for r in range(height):
        for c in range(width):
            if output_grid[r, c] != 0:
                visited.add((r, c))
                # If it's a blue pixel (1), add it to the queue to start the fill from here
                if output_grid[r, c] == 1:
                    queue.append((r, c))

    # Perform Breadth-First Search (BFS) flood fill
    while queue:
        r, c = queue.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor has not been visited. 
                # Since all non-white cells were added initially, 
                # a non-visited cell must be white (0).
                if (nr, nc) not in visited:
                    # Change color to blue (1)
                    output_grid[nr, nc] = 1
                    # Mark as visited
                    visited.add((nr, nc))
                    # Add to queue for further exploration
                    queue.append((nr, nc))

    # Convert the result back to a list of lists
    return output_grid.tolist()