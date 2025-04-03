```python
"""
Recolor contiguous objects based on their size parity.

1. Identify all connected components (objects) formed by pixels of color maroon (9) 
   in the input grid, using 4-connectivity (horizontal/vertical adjacency).
2. For each identified maroon object:
   a. Count the number of pixels constituting the object (determine its size).
   b. Check if the size is even or odd.
   c. If the size is even, change the color of all pixels belonging to this object 
      in the output grid to green (3).
   d. If the size is odd, change the color of all pixels belonging to this object 
      in the output grid to magenta (6).
3. Pixels that were originally white (0) remain unchanged.
"""

import numpy as np
from collections import deque

def find_connected_component(grid, start_row, start_col, visited):
    """
    Finds a single connected component of the same color starting from a given cell
    using Breadth-First Search (BFS).
    """
    target_color = grid[start_row, start_col]
    if target_color == 0: # Don't search for background components
        return []
        
    rows, cols = grid.shape
    component_coords = []
    queue = deque([(start_row, start_col)])
    visited[start_row, start_col] = True

    while queue:
        r, c = queue.popleft()
        component_coords.append((r, c))

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds, color, and visited status
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == target_color and not visited[nr, nc]:
                visited[nr, nc] = True
                queue.append((nr, nc))
                
    return component_coords

def transform(input_grid):
    """
    Transforms the input grid by recoloring maroon (9) objects based on their size parity.
    Even-sized objects become green (3), odd-sized objects become magenta (6).
    White (0) pixels remain unchanged.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = input_array.copy()
    
    # Keep track of visited cells to avoid processing the same object multiple times
    visited = np.zeros_like(input_array, dtype=bool)
    
    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # If the cell is maroon (9) and hasn't been visited yet, find its component
            if input_array[r, c] == 9 and not visited[r, c]:
                # Find all connected pixels of this object
                component_coords = find_connected_component(input_array, r, c, visited)
                
                # Calculate the size of the object
                object_size = len(component_coords)
                
                # Determine the new color based on size parity
                if object_size % 2 == 0:
                    new_color = 3 # Green for even size
                else:
                    new_color = 6 # Magenta for odd size
                    
                # Recolor the pixels belonging to this object in the output grid
                for obj_r, obj_c in component_coords:
                    output_grid[obj_r, obj_c] = new_color
                    
    # Return the modified grid (as a numpy array or convert back to list of lists if needed)
    return output_grid.tolist() # Convert back to list of lists format if required

```