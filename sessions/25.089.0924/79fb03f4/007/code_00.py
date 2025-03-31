import numpy as np
from collections import deque

def transform(input_grid):
    """
    Performs a flood fill operation starting from all blue (1) pixels in the 
    input grid. The fill color is blue (1) and it expands into adjacent 
    (up, down, left, right) white (0) pixels. The fill stops at the grid 
    boundaries or any non-white (0) pixels (e.g., gray 5, azure 8), which 
    act as barriers. All original non-white pixels retain their color and 
    position.
    """

    # Convert input to numpy array for easier indexing and manipulation
    np_input_grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(np_input_grid)
    height, width = output_grid.shape

    # Initialize queue for Breadth-First Search (BFS) flood fill
    queue = deque()
    
    # Initialize a set to track coordinates that have been visited or are part of the fill
    # This prevents infinite loops and redundant checks.
    visited = set()

    # Find initial starting points (blue pixels) and add them to the queue and visited set.
    # These are the sources from which the fill expands.
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is blue (1)
            if output_grid[r, c] == 1:
                # Add blue pixels as starting points for the BFS if not already added
                # (relevant if multiple blue pixels are connected initially)
                if (r, c) not in visited:
                    queue.append((r, c))
                    visited.add((r, c))

    # Perform the BFS flood fill
    while queue:
        # Get the next coordinate from the front of the queue
        r, c = queue.popleft()

        # Define the four cardinal directions for neighbors
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Explore neighbors (up, down, left, right)
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc

            # Check if the neighbor coordinate is within the grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor pixel is white (0) AND has not been visited yet
                # White pixels are the target for filling.
                # Non-white pixels act as implicit boundaries and are not processed further.
                if output_grid[nr, nc] == 0 and (nr, nc) not in visited:
                    # Change the neighbor's color to blue (1)
                    output_grid[nr, nc] = 1
                    # Mark the neighbor as visited
                    visited.add((nr, nc))
                    # Add the newly filled neighbor to the queue to explore from it later
                    queue.append((nr, nc))

    # Convert the final numpy grid back to a list of lists format
    return output_grid.tolist()