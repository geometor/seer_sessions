"""
Fill the region enclosed by a gray (5) boundary with azure (8). 
Identify the 'outside' region by performing a flood fill starting from white (0) pixels on the grid border. 
Any white pixels not reached by this flood fill are considered 'inside' the boundary and are changed to azure. 
Gray boundary pixels remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Transforms the input grid by filling the area enclosed by gray pixels with azure.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape
    
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Define colors
    WHITE = 0
    GRAY = 5
    AZURE = 8
    
    # Keep track of visited white pixels reachable from the border
    visited = np.zeros_like(input_grid, dtype=bool)
    
    # Initialize queue for Breadth-First Search (BFS) flood fill
    queue = deque()

    # Add all white border pixels to the queue and mark as visited
    for r in range(height):
        if input_grid[r, 0] == WHITE and not visited[r, 0]:
            queue.append((r, 0))
            visited[r, 0] = True
        if input_grid[r, width - 1] == WHITE and not visited[r, width - 1]:
            queue.append((r, width - 1))
            visited[r, width - 1] = True
            
    for c in range(width):
        if input_grid[0, c] == WHITE and not visited[0, c]:
            queue.append((0, c))
            visited[0, c] = True
        if input_grid[height - 1, c] == WHITE and not visited[height - 1, c]:
            queue.append((height - 1, c))
            visited[height - 1, c] = True

    # Perform BFS flood fill from border white pixels
    while queue:
        r, c = queue.popleft()
        
        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is white and not visited
                if input_grid[nr, nc] == WHITE and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    # Iterate through the grid and change unvisited white pixels to azure
    for r in range(height):
        for c in range(width):
            # If a pixel is white and was not reached by the border flood fill, it's inside
            if input_grid[r, c] == WHITE and not visited[r, c]:
                output_grid[r, c] = AZURE
                
    return output_grid