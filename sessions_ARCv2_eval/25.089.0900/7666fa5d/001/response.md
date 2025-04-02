```python
import numpy as np
from collections import deque

"""
Identify the background color (azure, 8) and boundary colors (any non-azure color).
Find all background pixels reachable from the grid's border without crossing a boundary pixel using a flood fill algorithm.
Create the output grid by copying the input grid.
Change the color of any background pixel *not* reached by the flood fill to red (2). 
Keep the boundary pixels and the reachable background pixels unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid by flood-filling the exterior background area and
    then changing the color of the interior (unfilled) background pixels.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape
    
    # Define colors
    background_color = 8
    fill_color = 2

    # Keep track of visited background cells reachable from the exterior
    visited = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # Add all background cells on the border to the queue to start the flood fill
    for r in range(height):
        if grid[r, 0] == background_color and not visited[r, 0]:
            queue.append((r, 0))
            visited[r, 0] = True
        if grid[r, width - 1] == background_color and not visited[r, width - 1]:
            queue.append((r, width - 1))
            visited[r, width - 1] = True
            
    for c in range(width):
        if grid[0, c] == background_color and not visited[0, c]:
            queue.append((0, c))
            visited[0, c] = True
        if grid[height - 1, c] == background_color and not visited[height - 1, c]:
            queue.append((height - 1, c))
            visited[height - 1, c] = True

    # Perform the flood fill (Breadth-First Search)
    while queue:
        r, c = queue.popleft()

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is a background cell and hasn't been visited
                if grid[nr, nc] == background_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    # Iterate through the grid and fill the interior background cells
    for r in range(height):
        for c in range(width):
            # If a cell is background color but was not visited by the flood fill,
            # it means it's enclosed by boundary pixels. Fill it with red.
            if grid[r, c] == background_color and not visited[r, c]:
                output_grid[r, c] = fill_color
                
    # Convert back to list of lists for the required output format
    return output_grid.tolist()

```