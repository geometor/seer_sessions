
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
```python
import numpy as np
from collections import deque

"""
Transforms the input grid based on the following rule:
1. Identifies two distinct non-background objects in the input grid. Assumes exactly two objects exist.
2. Determines the primary axis of separation (horizontal or vertical) between the two objects based on the distance between their bounding boxes or centroids.
3. Identifies one object as the "moving" object and the other as "static". The object that is "further out" along the separation axis (e.g., left object if separated horizontally, top object if separated vertically) is designated as the moving object.
4. The moving object is translated pixel by pixel along the separation axis towards the static object.
5. The movement stops when the moving object becomes edge-adjacent (shares a side, not just a corner) to the static object.
6. The final output grid shows the static object in its original position and the moving object in its final, adjacent position. If the objects have the same color, they may appear merged in the output.
"""

# Helper Class for representing objects
class ArcObject:
    """Represents a contiguous object in the grid."""
    def __init__(self, color, coords):
        if not coords:
             raise ValueError("Cannot create ArcObject with empty coordinates.")
        self.color = color
        self.coords = frozenset(coords) # Use frozenset for hashability if needed elsewhere
        # Calculate bounding box immediately
        self.min_r = min(r for r, c in coords)
        self.max_r = max(r for r, c in coords)
        self.min_c = min(c for r, c in coords)
        self.max_c = max(c for r, c in coords)
        self.centroid = self._calculate_centroid()

    def _calculate_centroid(self):
        """Calculates the geometric center of the object."""
        sum_r = sum(r for r, c in self.coords)
        sum_c = sum(c for r, c in self.coords)
        count = len(self.coords)
        return (sum_r / count, sum_c / count)

    def get_shifted_coords(self, dr, dc):
        """ Returns the set of coordinates if the object were shifted. """
        return frozenset((r + dr, c + dc) for r, c in self.coords)

def find_objects(grid, background_color=0):
    """
    Finds all distinct connected components (objects) of non-background colors
    in the grid using Breadth-First Search (BFS).

    Args:
        grid (np.array): The input grid.
        background_color (int): The value representing the background.

    Returns:
        list[ArcObject]: A list of ArcObject instances found in the grid. Returns empty list if no objects found.
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
                
                # Create an ArcObject if coordinates were found
                if coords: 
                    objects.append(ArcObject(color, coords))
    return objects

def check_adjacency(coords1, coords2):
    """ Checks if any coordinate in coords1 is edge-adjacent to any coordinate in coords2. """
    for r1, c1 in coords1:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (r1 + dr, c1 + dc)
            if neighbor in coords2:
                return True
    return False

def transform(input_grid_list):
    """
    Transforms the input grid by moving one object towards another until they touch.

    Args:
        input_grid_list (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    background_color = 0

    # --- 1. Find Objects ---
    objects = find_objects(input_grid, background_color)

    # --- Assumption Check ---
    # This rule specifically applies when there are exactly two objects.
    if len(objects) != 2:
        # Return the input unchanged if the assumption isn't met.
        return input_grid_list

    obj_a, obj_b = objects[0], objects[1]

    # --- 2. Determine Axis, Moving/Static Objects, and Direction ---
    # Use bounding boxes for separation calculation.
    # Horizontal gap: max(0, obj_b.min_c - obj_a.max_c - 1) or max(0, obj_a.min_c - obj_b.max_c - 1)
    # Vertical gap:   max(0, obj_b.min_r - obj_a.max_r - 1) or max(0, obj_a.min_r - obj_b.max_r - 1)

    # Check horizontal separation first
    h_sep = -1
    if obj_a.max_c < obj_b.min_c: # A is strictly left of B
         h_sep = obj_b.min_c - obj_a.max_c - 1
    elif obj_b.max_c < obj_a.min_c: # B is strictly left of A
         h_sep = obj_a.min_c - obj_b.max_c - 1
         
    # Check vertical separation
    v_sep = -1
    if obj_a.max_r < obj_b.min_r: # A is strictly above B
        v_sep = obj_b.min_r - obj_a.max_r - 1
    elif obj_b.max_r < obj_a.min_r: # B is strictly above A
        v_sep = obj_a.min_r - obj_b.max_r - 1

    moving_obj, static_obj = None, None
    direction = (0, 0) # (dr, dc)

    # Determine primary axis and roles based on larger separation
    # Handle edge case where separations might be equal but non-zero - prioritize horizontal? Let's check examples.
    # Ex1: h_sep=6, v_sep=-1 -> Horizontal. Ex2: h_sep=-1, v_sep=2 -> Vertical. Larger separation dominates.
    if h_sep >= 0 and (h_sep >= v_sep or v_sep < 0) : # Horizontal separation is primary
        if obj_a.max_c < obj_b.min_c: # A is left of B
            moving_obj = obj_a
            static_obj = obj_b
            direction = (0, 1) # Move right
        else: # B is left of A (obj_b.max_c < obj_a.min_c)
            moving_obj = obj_b
            static_obj = obj_a
            direction = (0, 1) # Move right (B moves right towards A)
            # Correction: If B is left of A, B should move right. If A is left of B, A should move right.
            # Let's simplify: The leftmost object moves right.
            if obj_a.min_c < obj_b.min_c:
                moving_obj, static_obj = obj_a, obj_b
                direction = (0, 1)
            else:
                moving_obj, static_obj = obj_b, obj_a
                direction = (0, 1) # Error in reasoning. If B is further left, B moves right.
            # Third attempt at logic: If A is left of B, A moves right. If B is left of A, B moves right. NO.
            # If A is left of B, A moves right. If A is right of B, A moves left. YES. Use centroids? No, BB is fine.
            if obj_a.centroid[1] < obj_b.centroid[1]: # A is left of B
                moving_obj, static_obj = obj_a, obj_b
                direction = (0, 1) # Move A right
            else: # A is right of B
                moving_obj, static_obj = obj_a, obj_b
                direction = (0, -1) # Move A left
    elif v_sep >= 0: # Vertical separation is primary
        if obj_a.centroid[0] < obj_b.centroid[0]: # A is above B
            moving_obj = obj_a
            static_obj = obj_b
            direction = (1, 0) # Move A down
        else: # A is below B
            moving_obj = obj_a
            static_obj = obj_b
            direction = (-1, 0) # Move A up
    else:
        # Objects are already touching or overlapping? Or separation only diagonal?
        # Rule likely doesn't apply, return original grid.
        return input_grid_list

    # --- 3. Simulate Movement ---
    output_grid = np.copy(input_grid)
    current_coords = set(moving_obj.coords) # Use a mutable set for current position
    static_coords_set = static_obj.coords # Keep as frozenset for efficiency

    while True:
        # Check if already adjacent before attempting to move
        if check_adjacency(current_coords, static_coords_set):
             break # Already touching, no move needed (or previous move was the last one)

        # Calculate potential next position
        dr, dc = direction
        next_coords = set((r + dr, c + dc) for r, c in current_coords)

        # Check bounds and direct collision with static object
        possible_move = True
        for nr, nc in next_coords:
            if not (0 <= nr < height and 0 <= nc < width):
                possible_move = False; break # Out of bounds
            if (nr, nc) in static_coords_set:
                possible_move = False; break # Direct collision
        
        if not possible_move:
            break # Cannot make the next move

        # Check if this move results in adjacency
        adjacent_after_move = check_adjacency(next_coords, static_coords_set)

        # Perform the move: Erase old, Draw new
        for r, c in current_coords:
             # Only erase if not part of the static object (needed if colors are the same)
             # Safter: just erase the moving object's color at the old coords.
             if output_grid[r,c] == moving_obj.color: # Check color to be safe
                 output_grid[r, c] = background_color

        for nr, nc in next_coords:
            output_grid[nr, nc] = moving_obj.color # Draw moving object in new position

        # Update current coordinates
        current_coords = next_coords

        # If the move we just made resulted in adjacency, stop
        if adjacent_after_move:
            break

    # --- 4. Return final grid state ---
    return output_grid.tolist()
```
