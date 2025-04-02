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