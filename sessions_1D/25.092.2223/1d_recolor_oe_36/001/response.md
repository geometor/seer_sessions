```python
"""
1. Initialize the output grid as a copy of the input grid.
2. Find all distinct groups (objects) of connected yellow (4) pixels in the input grid. 
   Pixels are considered connected if they share an edge (horizontally or vertically adjacent).
3. For each distinct yellow object found:
   a. Count the total number of pixels that make up the object (its size).
   b. Determine if the object's size is an odd or even number.
   c. If the size is odd, change the color of all pixels belonging to this object in the output grid to azure (8).
   d. If the size is even, change the color of all pixels belonging to this object in the output grid to green (3).
4. Leave all other pixels (originally white (0)) unchanged in the output grid.
5. The final output grid reflects these color changes.
"""

import numpy as np
from collections import deque

def find_connected_object(grid, start_row, start_col, target_color, visited):
    """
    Finds all connected pixels of a target color starting from a given point using BFS.
    Marks visited pixels.
    """
    rows, cols = grid.shape
    q = deque([(start_row, start_col)])
    object_pixels = []
    
    # Check if starting pixel is valid and not visited
    if not (0 <= start_row < rows and 0 <= start_col < cols) or \
       visited[start_row, start_col] or \
       grid[start_row, start_col] != target_color:
        return [] # Should not happen if called correctly, but good for safety

    visited[start_row, start_col] = True
    object_pixels.append((start_row, start_col))

    while q:
        r, c = q.popleft()
        
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds, color, and visited status
            if 0 <= nr < rows and 0 <= nc < cols and \
               not visited[nr, nc] and \
               grid[nr, nc] == target_color:
                
                visited[nr, nc] = True
                object_pixels.append((nr, nc))
                q.append((nr, nc))
                
    return object_pixels


def transform(input_grid):
    """
    Transforms the input grid based on the size parity of connected yellow objects.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = input_grid_np.copy()
    
    # Keep track of visited pixels to avoid reprocessing parts of the same object
    visited = np.zeros_like(input_grid_np, dtype=bool)
    
    target_color = 4 # yellow
    even_color = 3 # green
    odd_color = 8 # azure
    
    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # If we find a yellow pixel that hasn't been visited yet, it's the start of a new object
            if input_grid_np[r, c] == target_color and not visited[r, c]:
                
                # Find all pixels belonging to this connected object
                object_pixels = find_connected_object(input_grid_np, r, c, target_color, visited)
                
                # Calculate the size of the object
                object_size = len(object_pixels)
                
                # Determine the new color based on size parity
                new_color = odd_color if object_size % 2 != 0 else even_color
                
                # Update the output grid with the new color for all pixels in this object
                for obj_r, obj_c in object_pixels:
                    output_grid[obj_r, obj_c] = new_color
                    
    # Return the modified grid as a list of lists
    return output_grid.tolist()
```