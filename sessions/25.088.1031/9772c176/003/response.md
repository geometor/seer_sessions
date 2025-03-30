```python
import numpy as np
from collections import deque

"""
Identifies white background pixels (0) that are enclosed by azure shapes (8), 
meaning they cannot be reached from the grid border via 4-directional movement 
without crossing an azure pixel. These enclosed white pixels are then colored 
yellow (4) in the output grid. The original azure shapes and the reachable 
white background pixels remain unchanged.
"""

def flood_fill_reachable(grid, barrier_color):
    """
    Performs a flood fill from the border to find all cells reachable
    without crossing the barrier color.

    Args:
        grid (np.array): The input grid.
        barrier_color (int): The color that acts as a barrier.

    Returns:
        np.array: A boolean mask where True indicates a cell is reachable
                  from the border without crossing the barrier.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Initialize queue with non-barrier border cells
    for r in range(height):
        if grid[r, 0] != barrier_color and not visited[r, 0]:
            visited[r, 0] = True
            q.append((r, 0))
        if grid[r, width - 1] != barrier_color and not visited[r, width - 1]:
            visited[r, width - 1] = True
            q.append((r, width - 1))
    for c in range(1, width - 1): # Avoid corners twice
        if grid[0, c] != barrier_color and not visited[0, c]:
            visited[0, c] = True
            q.append((0, c))
        if grid[height - 1, c] != barrier_color and not visited[height - 1, c]:
            visited[height - 1, c] = True
            q.append((height - 1, c))

    # Perform flood fill
    while q:
        r, c = q.popleft()
        
        # Check 4-directional neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds, barrier color, and visited status
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] != barrier_color and not visited[nr, nc]:
                visited[nr, nc] = True
                q.append((nr, nc))
                
    return visited

def transform(input_grid):
    """
    Fills enclosed white areas with yellow.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    
    # Define colors
    BACKGROUND_COLOR = 0 # white
    BARRIER_COLOR = 8    # azure
    FILL_COLOR = 4       # yellow

    # 1. Identify all pixels reachable from the border without crossing the barrier
    reachable_mask = flood_fill_reachable(input_np, BARRIER_COLOR)

    # 2. Iterate through the grid
    for r in range(height):
        for c in range(width):
            # 3. If a pixel is background color AND not reachable, fill it
            if input_np[r, c] == BACKGROUND_COLOR and not reachable_mask[r, c]:
                output_grid[r, c] = FILL_COLOR
                
    # 4. Return the modified grid as a list of lists
    return output_grid.tolist()
```