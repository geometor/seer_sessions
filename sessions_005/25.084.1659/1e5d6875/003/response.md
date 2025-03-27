```python
import numpy as np
from collections import deque

"""
Transforms an input grid based on the proximity of contiguous orange (7) objects to red (2) and gray (5) pixels.

1. Initialize the output grid as a copy of the input grid.
2. Find all contiguous objects composed of orange (7) pixels in the input grid.
3. For each distinct orange object found:
    a. Check all pixels adjacent (including diagonals) to any pixel belonging to the current orange object.
    b. Determine if any of these adjacent pixels (that are not part of the object itself) are red (2). Let this be `object_near_red`.
    c. Determine if any of these adjacent pixels (that are not part of the object itself) are gray (5). Let this be `object_near_gray`.
    d. If `object_near_red` is true, change the color of *all* pixels constituting this orange object in the output grid to green (3).
    e. Else if `object_near_gray` is true (and `object_near_red` is false), change the color of *all* pixels constituting this orange object in the output grid to yellow (4).
    f. Otherwise (the orange object is not adjacent to any red or gray pixels), the pixels of the object remain orange (7) in the output grid.
4. Pixels that were not part of any orange object remain unchanged.
5. Return the final output grid.
"""

def _find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of coordinates 
              [(r1, c1), (r2, c2), ...] representing the pixels of the object.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) to find the connected object
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft() # Use popleft for BFS
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

def _check_object_neighbors(grid, object_coords):
    """
    Checks the neighbors surrounding an entire object for red (2) and gray (5) pixels.

    Args:
        grid (np.array): The input grid.
        object_coords (list): A list of (row, col) tuples representing the object's pixels.

    Returns:
        tuple: (is_near_red, is_near_gray) - booleans indicating presence of neighbors.
               Priority is given to red. If red is found, is_near_gray is returned as False.
    """
    height, width = grid.shape
    is_near_red = False
    is_near_gray = False
    
    # Use a set for efficient checking if a neighbor is part of the object itself
    object_coords_set = set(object_coords) 
    
    # Check for red neighbors first due to priority rule
    for r, c in object_coords:
        # Check 8 neighbors of this pixel
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
                            is_near_red = True
                            # Found red, no need to check further for red or gray
                            return True, False 
                            
    # If no red neighbors were found, check for gray neighbors
    for r, c in object_coords:
        # Check 8 neighbors of this pixel
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
                        if neighbor_color == 5: # gray
                            is_near_gray = True
                            # Found gray, no need to check further for gray
                            return False, True 
                            
    # If neither red nor gray neighbors were found
    return False, False


def transform(input_grid):
    """
    Applies the color transformation based on object neighbor proximity.

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

    # Iterate through each found orange object
    for obj_coords in orange_objects:
        # Check the neighbors of the current object
        is_near_red, is_near_gray = _check_object_neighbors(input_np, obj_coords)

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