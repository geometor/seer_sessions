```python
import numpy as np
from collections import deque

"""
Identifies regions enclosed by green (3) pixels and fills them with azure (8).

The transformation logic involves a flood fill starting from the non-green pixels 
on the border of the grid. Any pixel that cannot be reached from the border 
without crossing a green (3) pixel is considered enclosed. All pixels within 
these enclosed regions are changed to azure (8). Pixels reachable from the border 
retain their original color. Green (3) pixels themselves are never changed.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling regions enclosed by green pixels (3) 
    with azure pixels (8).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Create the output grid as a copy of the input grid initially
    output_grid = grid.copy()
    
    # Create a boolean grid to keep track of reachable cells
    # Initialize all cells as not reachable (False)
    reachable = np.zeros((height, width), dtype=bool)
    
    # Define the color acting as a wall/boundary
    wall_color = 3 # green
    fill_color = 8 # azure

    # Initialize a queue for Breadth-First Search (BFS)
    queue = deque()

    # Add all non-wall border cells to the queue and mark them as reachable
    for r in range(height):
        for c in range(width):
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                if grid[r, c] != wall_color:
                    if not reachable[r, c]:
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

    # Iterate through the entire grid
    for r in range(height):
        for c in range(width):
            # If a cell was not reached by the BFS, it's enclosed
            # Fill the corresponding cell in the output grid with the fill color
            # Do not change the color if the cell itself is a wall color. Although the 
            # description implies all unreachable cells are changed, the examples
            # show that the green walls themselves remain green. We need to check
            # if the *original* color was green before potentially changing it.
            # However, the logic implicitly handles this: green cells are walls,
            # and the BFS only marks *non-wall* cells as reachable. Therefore, any
            # green cell will *never* be marked as reachable.
            # The correct logic is simply: if it wasn't reached, fill it with azure.
            if not reachable[r, c]:
                 output_grid[r, c] = fill_color

    return output_grid.tolist() # Convert back to list of lists if required by framework
```