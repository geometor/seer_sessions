```python
import numpy as np
from collections import deque

"""
Identifies regions enclosed by green (3) pixels and fills them with azure (8), 
preserving the original green pixels.

The transformation logic involves a flood fill (BFS) starting from non-green 
pixels on the border of the grid. This identifies all pixels reachable from 
the outside without crossing a green pixel. Any pixel that is not reachable 
AND was not originally green (3) is considered part of an enclosed non-green 
region and is changed to azure (8). Pixels that were originally green (3) remain 
unchanged. Reachable pixels also retain their original color.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling non-green regions enclosed by 
    green pixels (3) with azure pixels (8).

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for efficient manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Create the output grid as a copy of the input grid initially
    output_grid = grid.copy()
    
    # Create a boolean grid to keep track of reachable cells
    # Initialize all cells as not reachable (False)
    reachable = np.zeros((height, width), dtype=bool)
    
    # Define the color acting as a wall/boundary and the fill color
    wall_color = 3 # green
    fill_color = 8 # azure

    # Initialize a queue for Breadth-First Search (BFS)
    queue = deque()

    # Seed the BFS: Add all non-wall border cells to the queue and mark them as reachable
    for r in range(height):
        for c in range(width):
            # Check if the cell is on the border
            is_border = r == 0 or r == height - 1 or c == 0 or c == width - 1
            if is_border:
                # Check if the border cell is not a wall and hasn't been marked reachable yet
                if grid[r, c] != wall_color and not reachable[r, c]:
                    reachable[r, c] = True
                    queue.append((r, c))

    # Perform BFS to find all cells reachable from the border without crossing walls
    while queue:
        r, c = queue.popleft()

        # Check four neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is not a wall and has not been reached yet
                if grid[nr, nc] != wall_color and not reachable[nr, nc]:
                    reachable[nr, nc] = True
                    queue.append((nr, nc))

    # Iterate through the entire grid to fill unreachable non-wall cells
    for r in range(height):
        for c in range(width):
            # Check if the cell was NOT reached by the BFS
            if not reachable[r, c]:
                # Check if the original cell color was NOT the wall color
                if grid[r, c] != wall_color:
                    # If both conditions are true, fill the cell in the output grid
                    output_grid[r, c] = fill_color

    # Convert the result back to a list of lists before returning
    return output_grid.tolist()
```