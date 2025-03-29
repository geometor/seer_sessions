import numpy as np
from collections import deque

"""
Identify contiguous regions of white pixels (0) that are completely enclosed by azure pixels (8) or the grid boundaries. 
Change all white pixels within these enclosed regions to green (3). Other pixels remain unchanged.

The process involves:
1. Copy the input grid to create the output grid.
2. Find all white pixels (0) that are connected to the grid boundary (either directly on the boundary or connected via a path of white pixels).
3. Use a Breadth-First Search (BFS) starting from all boundary white pixels to mark all reachable white pixels.
4. Iterate through the grid. Any white pixel that was *not* marked as reachable from the boundary is considered enclosed.
5. Change the color of these enclosed white pixels to green (3) in the output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling enclosed white regions with green.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid to numpy array if it's not already
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid_np.copy()
    
    # Initialize a visited grid to keep track of white pixels reachable from the boundary
    visited = np.zeros((height, width), dtype=bool)
    
    # Queue for BFS
    q = deque()

    # Add all white pixels (0) on the border to the queue and mark as visited
    for r in range(height):
        for c in range(width):
            if (r == 0 or r == height - 1 or c == 0 or c == width - 1) and input_grid_np[r, c] == 0:
                if not visited[r, c]:
                    q.append((r, c))
                    visited[r, c] = True

    # Define neighbors (up, down, left, right)
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    # Perform BFS to find all white pixels connected to the boundary
    while q:
        r, c = q.popleft()
        
        # Explore neighbors
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            
            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is white and not visited
                if input_grid_np[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # Iterate through the grid and change unvisited white pixels to green (3)
    for r in range(height):
        for c in range(width):
            # If a pixel is white (0) and was not visited by the BFS (meaning it's enclosed)
            if input_grid_np[r, c] == 0 and not visited[r, c]:
                output_grid[r, c] = 3  # Change color to green
                
    return output_grid.tolist() # Return as list of lists for compatibility