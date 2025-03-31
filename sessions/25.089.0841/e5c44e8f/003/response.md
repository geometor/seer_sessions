```python
"""
Perform a flood fill operation starting from green (3) pixels. 
The fill color is green (3).
The fill only affects white (0) pixels found in the original input grid.
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
        input_grid (list of lists): The input grid.
        
    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation and copying
    input_np = np.array(input_grid, dtype=int)
    output_grid = input_np.copy()
    height, width = input_np.shape

    # Initialize a queue for Breadth-First Search (BFS) flood fill
    queue = deque()
    
    # Keep track of visited cells to avoid cycles and redundant work. 
    # Crucially, visited means "either a start point or a point we have filled".
    visited = set()

    # Find initial green pixels (starting points)
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 3:
                start_point = (r, c)
                # Add starting green points to the queue and visited set
                if start_point not in visited:
                    queue.append(start_point)
                    visited.add(start_point)

    # Define 4-directional neighbors (Right, Left, Down, Up)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

    # Perform Breadth-First Search (BFS) based flood fill
    while queue:
        # Get the current cell from the front of the queue
        r, c = queue.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # 1. Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                
                # 2. Check if the neighbor has not been visited (i.e., not a starting green or already filled)
                if (nr, nc) not in visited:
                    
                    # 3. Check if the neighbor in the *original* grid is white (0), which is the only color fillable
                    if input_np[nr, nc] == 0:
                        # If all conditions met: fill, mark visited, and enqueue
                        output_grid[nr, nc] = 3  # Change the color in the output grid
                        visited.add((nr, nc))    # Mark as visited
                        queue.append((nr, nc))   # Add to queue for further exploration
                    
                    # Note: We implicitly handle red barriers (2) by not filling them (input_np[nr,nc] != 0) 
                    # and not adding them to the queue or visited set if they are encountered as neighbors.

    # Convert the result back to a list of lists as required
    return output_grid.tolist()
```