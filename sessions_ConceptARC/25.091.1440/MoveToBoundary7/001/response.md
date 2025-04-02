```python
import numpy as np
from collections import deque

"""
Identifies two distinct non-background objects in the input grid. 
Determines which object is 'moving' and which is 'static' based on their relative 
positions (calculated using centroids). The object positioned further out along 
the primary axis of separation (horizontal or vertical) is considered the 
moving object. The moving object is then translated pixel by pixel along that axis 
towards the static object. The movement stops just before the moving object would 
collide with (become edge-adjacent to) the static object or move out of the 
grid boundaries. The static object remains in its original position. The final 
grid reflects the new position of the moving object and the original position 
of the static object. Assumes exactly two non-background objects exist.
"""

# Helper Class for representing objects
class ArcObject:
    """Represents a contiguous object in the grid."""
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords # set of (r, c) tuples
        self.centroid = self._calculate_centroid()

    def _calculate_centroid(self):
        """Calculates the geometric center of the object."""
        if not self.coords:
            return (0.0, 0.0)
        sum_r = sum(r for r, c in self.coords)
        sum_c = sum(c for r, c in self.coords)
        count = len(self.coords)
        # Using float division for potentially non-integer centroid
        return (sum_r / count, sum_c / count)

def find_objects(grid, background_color=0):
    """
    Finds all distinct connected components (objects) of non-background colors
    in the grid using Breadth-First Search (BFS).

    Args:
        grid (np.array): The input grid.
        background_color (int): The value representing the background.

    Returns:
        list[ArcObject]: A list of ArcObject instances found in the grid.
    """
    objects = []
    height, width = grid.shape
    visited = set() # Keep track of visited cells to avoid redundant searches

    for r in range(height):
        for c in range(width):
            # If the cell is not background and hasn't been visited yet
            if grid[r, c] != background_color and (r, c) not in visited:
                color = grid[r, c]
                coords = set() # Coordinates belonging to this object
                q = deque([(r, c)]) # Queue for BFS
                visited.add((r, c))
                coords.add((r, c))

                # Start BFS from this cell
                while q:
                    row, col = q.popleft()
                    # Explore 4 cardinal neighbors (North, South, East, West)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor is part of the object (same color) and not visited
                            if (nr, nc) not in visited and grid[nr, nc] == color:
                                visited.add((nr, nc))
                                coords.add((nr, nc))
                                q.append((nr, nc))
                
                # If coordinates were found, create an ArcObject
                if coords: 
                    objects.append(ArcObject(color, coords))
    return objects

def transform(input_grid_list):
    """
    Transforms the input grid based on the object movement rule.

    Args:
        input_grid_list (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    background_color = 0 # Standard ARC background

    # --- 1. Find Objects ---
    objects = find_objects(input_grid, background_color)

    # --- Basic Assumption Check ---
    # The observed rule applies specifically to two objects.
    if len(objects) != 2:
        # If the assumption isn't met, return the input unchanged as the rule doesn't apply.
        # print(f"Warning: Expected 2 objects, found {len(objects)}. Returning input.")
        return input_grid_list 
        
    obj1, obj2 = objects[0], objects[1]

    # --- 2. Determine Moving/Static Objects and Direction ---
    # Calculate centroids to determine relative positions
    c1_r, c1_c = obj1.centroid
    c2_r, c2_c = obj2.centroid

    # Calculate difference in row and column coordinates
    delta_r = abs(c1_r - c2_r)
    delta_c = abs(c1_c - c2_c)

    moving_obj, static_obj = None, None
    direction = (0, 0) # Represents (dr, dc) for movement step

    # Determine primary axis of separation and assign roles/direction
    if delta_c > delta_r: # Primarily horizontal separation
        if c1_c < c2_c: # obj1 is left of obj2
            moving_obj = obj1
            static_obj = obj2
            direction = (0, 1) # Move right
        else: # obj1 is right of obj2 (c1_c >= c2_c)
            # Need to swap roles if obj1 is right
            moving_obj = obj2 
            static_obj = obj1
            direction = (0, -1) # Move left (obj2 moves left towards obj1)
            # Correction: Original logic assumed obj1 always moves if left/top.
            # Corrected logic: The object 'further out' moves towards the other.
            # If obj1 right of obj2, obj1 moves left towards obj2.
            moving_obj = obj1
            static_obj = obj2
            direction = (0, -1) # Move left
            
    else: # Primarily vertical separation (or equal distance)
        if c1_r < c2_r: # obj1 is above obj2
            moving_obj = obj1
            static_obj = obj2
            direction = (1, 0) # Move down
        else: # obj1 is below obj2 (c1_r >= c2_r)
            # If obj1 below obj2, obj1 moves up towards obj2.
            moving_obj = obj1
            static_obj = obj2
            direction = (-1, 0) # Move up


    # --- 3. Simulate Movement ---
    output_grid = np.copy(input_grid)
    # Use a mutable set for the moving object's coordinates
    current_coords = set(moving_obj.coords) 
    # Use an immutable set for the static object's coordinates (faster lookups)
    static_coords_set = frozenset(static_obj.coords) 

    while True:
        # Calculate the potential next position for the entire object
        next_coords = set()
        possible_move = True
        for r, c in current_coords:
            nr, nc = r + direction[0], c + direction[1]
            
            # Check if the next position of this pixel is within grid bounds
            if not (0 <= nr < height and 0 <= nc < width):
                possible_move = False # Entire object cannot make this move
                break 
            next_coords.add((nr, nc))
        
        # If any part of the object would move out of bounds, stop
        if not possible_move:
            break 

        # Check if the potential next position is adjacent to the static object
        adjacent = False
        for nr, nc in next_coords:
            # Check N, S, E, W neighbors of the potential next pixel position
            for dr_adj, dc_adj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor_r, neighbor_c = nr + dr_adj, nc + dc_adj
                # Check if this neighbor belongs to the static object
                if (neighbor_r, neighbor_c) in static_coords_set:
                    adjacent = True
                    break # Found adjacency, no need to check further neighbors
            if adjacent:
                break # Found adjacency, no need to check other pixels in next_coords
        
        # If the next move would result in adjacency, stop *before* making the move
        if adjacent:
            break 

        # --- If move is valid (in bounds and not adjacent) ---
        # Erase the object from its old position on the output grid
        for r, c in current_coords:
            output_grid[r, c] = background_color
        
        # Draw the object in its new position on the output grid
        for nr, nc in next_coords:
            # Check if the target cell is background (prevent overwriting static obj if colors are same)
            # This check might be redundant if initial separation is guaranteed, but safe to include.
             if output_grid[nr,nc] == background_color:
                 output_grid[nr, nc] = moving_obj.color
            # else: # This case shouldn't happen if objects start separate and static obj isn't background
            #    pass # potentially overlapping non-background? ignore for now.
            
        # Update the current coordinates for the next iteration
        current_coords = next_coords

    # --- 4. Return final grid state ---
    return output_grid.tolist()
```