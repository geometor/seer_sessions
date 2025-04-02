
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 3 3 3 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 3 0 0 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 3 0 0 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 3 3 3 3 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 3 3 3 3 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 3 0 0 3 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 3 0 0 3 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 3 3 3 3 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0 0 0 0 4
0 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception**

1.  **Input/Output Structure:** Both inputs and outputs are 2D grids of pixels with different colors. The background is white (0).
2.  **Objects:** Each grid contains distinct geometric shapes (objects) formed by contiguous pixels of the same non-white color.
    *   Example 1: Input has a green (3) 'C' shape and a red (2) 'L' shape. Output has the same shapes.
    *   Example 2: Input has a small yellow (4) rectangle and a large yellow (4) 'U' shape. Output has the same shapes.
3.  **Transformation:** The core transformation involves moving one object until it becomes adjacent to another object.
    *   In Example 1, the green 'C' moves horizontally to the right until it touches the side of the red 'L'. The red 'L' does not move.
    *   In Example 2, the small yellow rectangle moves vertically downwards until it touches the top edge of the large yellow 'U'. The yellow 'U' does not move.
4.  **Key Elements:**
    *   **Moving Object:** An object that changes its position.
    *   **Static Object (Obstacle):** An object that remains in its original position and acts as a barrier to the moving object.
    *   **Direction of Movement:** The moving object travels in a straight line (horizontally or vertically) towards the static object.
    *   **Stopping Condition:** The movement ceases when the moving object is directly adjacent (sharing an edge) to the static object.

**Facts**


```yaml
Examples:
  - ID: train_1
    Input:
      Grid_Size: [10, 19]
      Objects:
        - ID: Obj_A
          Color: green (3)
          Shape: 'C'
          Location: BoundingBox(rows=(2, 6), cols=(2, 5)) # Approx location
        - ID: Obj_B
          Color: red (2)
          Shape: 'L'
          Location: BoundingBox(rows=(1, 9), cols=(12, 18)) # Approx location
    Output:
      Grid_Size: [10, 19]
      Objects:
        - ID: Obj_A
          Color: green (3)
          Shape: 'C'
          Location: BoundingBox(rows=(2, 6), cols=(8, 11)) # Approx location
        - ID: Obj_B
          Color: red (2)
          Shape: 'L'
          Location: BoundingBox(rows=(1, 9), cols=(12, 18)) # Approx location
    Transformation:
      Action: Move Object_A rightwards.
      Static_Object: Object_B
      Stop_Condition: Object_A becomes horizontally adjacent to Object_B.

  - ID: train_2
    Input:
      Grid_Size: [14, 12]
      Objects:
        - ID: Obj_C
          Color: yellow (4)
          Shape: Rectangle (2x2)
          Location: BoundingBox(rows=(1, 3), cols=(4, 6)) # Approx location
        - ID: Obj_D
          Color: yellow (4)
          Shape: 'U'
          Location: BoundingBox(rows=(5, 13), cols=(1, 11)) # Approx location
    Output:
      Grid_Size: [14, 12]
      Objects:
        - ID: Obj_C
          Color: yellow (4)
          Shape: Rectangle (2x2)
          Location: BoundingBox(rows=(3, 5), cols=(4, 6)) # Approx location
        - ID: Obj_D
          Color: yellow (4)
          Shape: 'U'
          Location: BoundingBox(rows=(5, 13), cols=(1, 11)) # Approx location
    Transformation:
      Action: Move Object_C downwards.
      Static_Object: Object_D
      Stop_Condition: Object_C becomes vertically adjacent to Object_D.

General_Observations:
  - Background_Color: white (0) is consistent.
  - Object_Integrity: Shapes and colors of objects are preserved during movement.
  - Movement_Mechanism: One object moves towards another static object.
  - Movement_Axis: Movement occurs along a single axis (horizontal or vertical).
  - Adjacency_Rule: Movement stops when the moving object's boundary touches the static object's boundary along the axis of movement.
```


**Natural Language Program**

1.  Identify all distinct, contiguous non-white objects in the input grid.
2.  Determine which object moves and which object remains static by comparing the input and output grids (or by identifying a smaller object likely intended to move towards a larger one, though relying solely on input requires more inference). Assume there is one moving object and one primary static object (obstacle).
3.  Determine the primary direction of movement (up, down, left, or right) by observing the relative positions of the moving object and the static object. The moving object moves towards the static object.
4.  Simulate shifting the *entire* moving object one pixel at a time in the determined direction.
5.  After each shift, check if any pixel of the moving object is now adjacent (shares an edge, not just a corner) to any pixel of the static object along the axis of movement.
6.  If adjacency is detected, stop the movement. The current position of the moving object is its final position.
7.  Construct the output grid by placing the moving object in its final position and keeping the static object and background unchanged from the input grid.
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
