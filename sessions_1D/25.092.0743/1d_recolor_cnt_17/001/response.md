```python
"""
Identifies all distinct contiguous objects composed of yellow (4) pixels in the input grid.
Counts the number of pixels (size) for each yellow object.
Recolors the pixels of each yellow object in the output grid based on its size:
- Size 1 objects become red (2).
- Size 2 objects become azure (8).
- Size 3 objects become gray (5).
Background pixels (white, 0) and yellow objects of other sizes remain unchanged.
Connectivity is defined by horizontal and vertical adjacency.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Transforms the input grid by recoloring yellow objects based on their size.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()  # Initialize output grid as a copy of the input
    rows, cols = grid.shape
    
    # Keep track of visited cells to avoid processing the same object multiple times
    visited = np.zeros_like(grid, dtype=bool)
    
    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is yellow (4) and hasn't been visited yet
            if grid[r, c] == 4 and not visited[r, c]:
                # Found the start of a potential yellow object
                current_object_pixels = []
                q = deque([(r, c)]) # Use a queue for Breadth-First Search (BFS)
                visited[r, c] = True # Mark the starting cell as visited
                
                # Perform BFS to find all connected yellow pixels (the object)
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_pixels.append((curr_r, curr_c))
                    
                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check if the neighbor is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor is yellow and not visited
                            if grid[nr, nc] == 4 and not visited[nr, nc]:
                                visited[nr, nc] = True # Mark neighbor as visited
                                q.append((nr, nc)) # Add neighbor to the queue
                                
                # Object found, determine its size
                object_size = len(current_object_pixels)
                
                # Determine the target color based on the object size
                target_color = -1 # Default value indicating no color change based on size rules
                if object_size == 1:
                    target_color = 2 # Red
                elif object_size == 2:
                    target_color = 8 # Azure
                elif object_size == 3:
                    target_color = 5 # Gray
                    
                # Recolor the object in the output grid if a target color was determined
                if target_color != -1:
                    for obj_r, obj_c in current_object_pixels:
                        output_grid[obj_r, obj_c] = target_color
                        
    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()

```