```python
import numpy as np
from collections import deque

"""
Identifies distinct connected components (objects) of red (2) pixels in the input grid using orthogonal adjacency. 
Assigns a unique identifier to each red pixel based on the object it belongs to.
Iterates through every white (0) pixel in the input grid.
For each white pixel, checks if it lies on a straight, unobstructed (only white pixels) horizontal path between two red pixels belonging to *different* objects. If so, colors the white pixel blue (1).
If the horizontal check fails, performs a similar check vertically. If it lies on a straight, unobstructed vertical path between two red pixels belonging to *different* objects, colors the white pixel blue (1).
Original red pixels and other white pixels remain unchanged.
"""

def find_objects(grid, target_color):
    """
    Finds connected components of a specific color in a grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        np.array: A grid of the same dimensions where each pixel belonging
                  to an object is labeled with a unique positive integer ID.
                  Other pixels are labeled 0.
    """
    rows, cols = grid.shape
    object_id_grid = np.zeros_like(grid, dtype=int)
    current_object_id = 1
    visited = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and (r, c) not in visited:
                # Start BFS for a new object
                q = deque([(r, c)])
                visited.add((r, c))
                object_id_grid[r, c] = current_object_id
                
                while q:
                    row, col = q.popleft()
                    
                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check boundaries and if the neighbor is the target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            object_id_grid[nr, nc] = current_object_id
                            q.append((nr, nc))
                            
                current_object_id += 1
                
    return object_id_grid

def transform(input_grid):
    """
    Transforms the input grid by adding blue bridges between distinct red objects.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)
    
    # 1. Identify distinct red objects
    red_object_ids = find_objects(input_grid, 2) # 2 is red

    # 2. Iterate through white pixels to check for potential bridges
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0: # Check only white pixels (0)
                
                # 3a. Check horizontally
                left_red_pixel = None
                right_red_pixel = None

                # Scan left
                for nc in range(c - 1, -2, -1): # Go down to -1 to handle boundary check easily
                    if nc < 0: # Reached boundary
                        break
                    if input_grid[r, nc] != 0: # Found non-white
                        if input_grid[r, nc] == 2: # It's red
                            left_red_pixel = (r, nc)
                        break # Stop scanning left (either found red or obstruction)
                
                # Scan right
                for nc in range(c + 1, cols + 1): # Go up to cols to handle boundary check easily
                    if nc >= cols: # Reached boundary
                        break
                    if input_grid[r, nc] != 0: # Found non-white
                        if input_grid[r, nc] == 2: # It's red
                            right_red_pixel = (r, nc)
                        break # Stop scanning right

                # Check if valid horizontal bridge
                if (left_red_pixel is not None and 
                    right_red_pixel is not None and
                    red_object_ids[left_red_pixel] != red_object_ids[right_red_pixel]):
                    output_grid[r, c] = 1 # Color blue
                    continue # Move to next white pixel, no need for vertical check

                # 3b. Check vertically (only if horizontal failed)
                up_red_pixel = None
                down_red_pixel = None

                # Scan up
                for nr in range(r - 1, -2, -1): # Go down to -1 
                    if nr < 0:
                        break
                    if input_grid[nr, c] != 0:
                        if input_grid[nr, c] == 2:
                            up_red_pixel = (nr, c)
                        break
                        
                # Scan down
                for nr in range(r + 1, rows + 1): # Go up to rows
                    if nr >= rows:
                        break
                    if input_grid[nr, c] != 0:
                        if input_grid[nr, c] == 2:
                            down_red_pixel = (nr, c)
                        break

                # Check if valid vertical bridge
                if (up_red_pixel is not None and 
                    down_red_pixel is not None and
                    red_object_ids[up_red_pixel] != red_object_ids[down_red_pixel]):
                    output_grid[r, c] = 1 # Color blue

    return output_grid
```