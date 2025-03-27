```python
import numpy as np
from collections import deque

"""
Transforms the input grid by changing the color of specific orange (7) objects based on adjacent colors, ignoring the single largest orange object (considered background).

1. Find all distinct contiguous objects composed of orange (7) pixels.
2. Identify the orange object with the largest number of pixels (the background).
3. For all *other* orange objects (non-background):
    a. Check if any pixel within the object is adjacent (8-way, including diagonals) to a red (2) pixel located *outside* the object. If yes, the entire object is marked to turn green (3).
    b. If not adjacent to red, check if any pixel within the object is adjacent (8-way) to a gray (5) pixel located *outside* the object. If yes, the entire object is marked to turn yellow (4).
    c. If adjacent to neither red nor gray, the object remains orange (7).
4. Apply the determined color changes to the output grid. The largest orange object and all non-orange pixels remain unchanged.
"""

def _find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid using BFS.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of coordinates 
              [(r1, c1), (r2, c2), ...] representing the pixels of the object. Returns empty list if none found.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_coords.append((row, col))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            
                            nr, nc = row + dr, col + dc
                            
                            # Check if neighbor is within bounds, is the correct color, and hasn't been visited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                # Add the found object (list of coordinates) to the list of objects
                if current_object_coords:
                    objects.append(current_object_coords)
                
    return objects

def _check_object_neighbors_refined(grid, object_coords):
    """
    Checks if any pixel within the object is adjacent to a red(2) or gray(5) pixel outside the object.
    Prioritizes red.

    Args:
        grid (np.array): The input grid.
        object_coords (list): A list of (row, col) tuples representing the object's pixels.

    Returns:
        tuple: (is_near_red, is_near_gray) - booleans indicating adjacency.
               If is_near_red is True, is_near_gray will be False due to priority.
    """
    height, width = grid.shape
    object_coords_set = set(object_coords) # For efficient lookup
    is_near_red = False
    is_near_gray = False

    for r, c in object_coords:
        # Check 8 neighbors of the current pixel (r, c)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self
                
                nr, nc = r + dr, c + dc
                
                # Check if neighbor is within grid bounds
                if 0 <= nr < height and 0 <= nc < width:
                    # Check if the neighbor is *outside* the object itself
                    if (nr, nc) not in object_coords_set: 
                        neighbor_color = grid[nr, nc]
                        if neighbor_color == 2: # red
                            # Found a red neighbor, red has priority, no need to check further.
                            return True, False 
                        elif neighbor_color == 5: # gray
                            # Found a gray neighbor, note it but continue checking
                            # in case a red neighbor is found later for this object.
                            is_near_gray = True
                            
    # If the loop completes without finding any red neighbors
    return False, is_near_gray


def transform(input_grid):
    """
    Applies the color transformation based on object adjacency, ignoring the largest orange object.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)

    # Find all orange objects
    orange_objects = _find_objects(input_np, 7) # 7 is orange

    # If no orange objects, return the copy
    if not orange_objects:
        return output_grid.tolist()

    # Find the largest orange object (by number of pixels)
    largest_object_index = -1
    max_size = -1
    if len(orange_objects) > 0:
         sizes = [len(obj) for obj in orange_objects]
         max_size = max(sizes)
         # Find the index of the first object with the maximum size
         largest_object_index = sizes.index(max_size) 
         
         # Handle potential ties: if multiple objects have the same max size,
         # the problem description implies a single "background". We assume
         # the first one found is sufficient, or that ties won't occur in test cases,
         # or that the specific tie-breaking rule doesn't matter if they all behave like background.
         # For now, we just exclude the first one found with max size.


    # Iterate through each found orange object
    for i, obj_coords in enumerate(orange_objects):
        # Skip the largest object (the background)
        if i == largest_object_index:
            continue

        # Check the neighbors of the current (non-background) object
        is_near_red, is_near_gray = _check_object_neighbors_refined(input_np, obj_coords)

        # Determine the target color based on neighbors
        target_color = 7 # Default to orange (no change)
        if is_near_red:
            target_color = 3 # Green if near red
        elif is_near_gray:
            target_color = 4 # Yellow if near gray (and not near red)

        # If the target color is different from orange, update the output grid
        if target_color != 7:
            for r, c in obj_coords:
                output_grid[r, c] = target_color

    # Return the final output grid as a list of lists
    return output_grid.tolist()
```