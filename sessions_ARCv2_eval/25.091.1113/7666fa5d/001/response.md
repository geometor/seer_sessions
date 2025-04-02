```python
"""
This program transforms an input grid by filling enclosed regions.
1. It identifies the background color (azure 8).
2. It performs a flood fill starting from all background-colored pixels on the grid's border. This marks all background pixels connected to the outside.
3. It iterates through the grid. Any background pixel that was *not* reached by the flood fill (i.e., is enclosed by non-background pixels) is changed to red (2).
4. Non-background pixels and background pixels connected to the border remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Fills enclosed regions of the background color with red (2).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid)
    output_grid = grid.copy()
    rows, cols = grid.shape
    
    # Define background and fill colors
    background_color = 8
    fill_color = 2
    
    # Create a boolean grid to mark visited background pixels connected to the outside
    visited = np.zeros_like(grid, dtype=bool)
    
    # Queue for Flood Fill (BFS)
    q = deque()

    # Add all background pixels on the border to the queue and mark as visited
    for r in range(rows):
        if grid[r, 0] == background_color and not visited[r, 0]:
            q.append((r, 0))
            visited[r, 0] = True
        if grid[r, cols - 1] == background_color and not visited[r, cols - 1]:
            q.append((r, cols - 1))
            visited[r, cols - 1] = True
            
    for c in range(cols):
        if grid[0, c] == background_color and not visited[0, c]:
            q.append((0, c))
            visited[0, c] = True
        if grid[rows - 1, c] == background_color and not visited[rows - 1, c]:
            q.append((rows - 1, c))
            visited[rows - 1, c] = True

    # Perform flood fill (BFS) from the border background pixels
    while q:
        r, c = q.popleft()
        
        # Check 4-way neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is background color and not yet visited
                if grid[nr, nc] == background_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # Iterate through the entire grid
    for r in range(rows):
        for c in range(cols):
            # If a pixel is background color but was not visited by the flood fill,
            # it means it's enclosed. Fill it with the fill_color.
            if grid[r, c] == background_color and not visited[r, c]:
                output_grid[r, c] = fill_color

    # Return the modified grid (convert back to list of lists if necessary for ARC standard)
    # return output_grid.tolist() 
    # Keep as numpy array for internal consistency within the SEER process for now
    return output_grid

```