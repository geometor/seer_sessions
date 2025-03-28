import numpy as np
from collections import deque

"""
Simulates a gravity-like effect where non-red, non-white objects, treated as 
whole units, 'fall' towards a static red barrier until they hit the red barrier, 
another object, or the grid boundary. The direction of 'gravity' (Down, Left, 
or Right) is determined by the relative average position of the red barrier(s) 
compared to the movable objects. Objects move one step at a time iteratively 
until no object can move further, maintaining their shape and integrity.
"""

def find_objects(grid, colors_to_find):
    """
    Finds all contiguous objects of specified colors in the grid.
    Uses 8-way connectivity (including diagonals).

    Args:
        grid (np.array): The input grid.
        colors_to_find (set): A set of color values to find objects for.

    Returns:
        list: A list of objects. Each object is a dictionary:
              {'color': int, 'pixels': list of (r, c) tuples}.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color in colors_to_find and not visited[r, c]:
                # Start BFS to find all connected pixels of the same color
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            
                            # Check bounds, color match, and visited status
                            if 0 <= nr < height and 0 <= nc < width and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                if obj_pixels:
                    objects.append({'color': color, 'pixels': obj_pixels})
                    
    return objects

def determine_direction(grid, movable_objects, barrier_pixels):
    """
    Determines the direction of movement based on the relative positions of
    red (2) pixels and movable objects.

    Args:
        grid (np.array): The grid.
        movable_objects (list): List of movable object dicts.
        barrier_pixels (list): List of (r, c) tuples for red pixels.

    Returns:
        tuple: (delta_row, delta_col) representing the direction vector.
               (1, 0) for down, (0, -1) for left, (0, 1) for right.
               Returns (0, 0) if direction cannot be determined or no movement needed.
    """
    height, width = grid.shape

    if not barrier_pixels or not movable_objects:
        return (0, 0) # No barrier or nothing to move

    # Calculate average positions
    barrier_r_coords = [p[0] for p in barrier_pixels]
    barrier_c_coords = [p[1] for p in barrier_pixels]
    barrier_r_avg = np.mean(barrier_r_coords)
    barrier_c_avg = np.mean(barrier_c_coords)

    all_object_pixels = [p for obj in movable_objects for p in obj['pixels']]
    if not all_object_pixels:
         return (0,0)
         
    object_r_coords = [p[0] for p in all_object_pixels]
    object_c_coords = [p[1] for p in all_object_pixels]
    object_r_avg = np.mean(object_r_coords)
    object_c_avg = np.mean(object_c_coords)

    # Determine direction based on average positions
    # Prioritize vertical difference slightly
    delta_r_diff = barrier_r_avg - object_r_avg
    delta_c_diff = barrier_c_avg - object_c_avg

    # Use a threshold to avoid ambiguity when averages are very close
    threshold = 0.1 

    # Check Down first
    if delta_r_diff > threshold and delta_r_diff > abs(delta_c_diff):
        return (1, 0) # Down
        
    # Check Left
    if delta_c_diff < -threshold and abs(delta_c_diff) >= delta_r_diff :
         return (0, -1) # Left

    # Check Right
    if delta_c_diff > threshold and delta_c_diff >= delta_r_diff:
         return (0, 1) # Right

    # Fallback: Check Down if red is mostly below, even if horizontal diff is larger
    if delta_r_diff > threshold:
         return (1,0)

    # --- Refined Fallback / edge cases ---
    # Check proximity to boundaries if averages are close or ambiguous
    max_barrier_r = max(barrier_r_coords) if barrier_r_coords else -1
    min_barrier_r = min(barrier_r_coords) if barrier_r_coords else height
    max_barrier_c = max(barrier_c_coords) if barrier_c_coords else -1
    min_barrier_c = min(barrier_c_coords) if barrier_c_coords else width

    if max_barrier_r == height - 1 and min_barrier_r > 0 : return (1, 0) # Red touches bottom, not top -> Down
    if min_barrier_c == 0 and max_barrier_c < width -1 : return (0, -1) # Red touches left, not right -> Left
    if max_barrier_c == width - 1 and min_barrier_c > 0: return (0, 1) # Red touches right, not left -> Right
    
    # Default: If still unclear, favor Down if possible, otherwise no movement
    if delta_r_diff > 0: # If red is generally below at all
        return (1, 0)
        
    return (0, 0) # Default to no movement if unclear

def transform(input_grid):
    """
    Applies a gravity-like transformation to the input grid. Non-red, non-white
    objects, treated as single units, move towards the static red pixels 
    (color 2) until blocked by the grid boundary, the red barrier, or another 
    settled object. Objects maintain their integrity.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Define movable colors (all except white 0 and red 2)
    movable_colors = set(range(10)) - {0, 2}

    # --- Initialization ---
    # 1. Identify barrier pixels
    barrier_pixels = list(zip(*np.where(grid == 2)))

    # 2. Identify all movable objects
    # We re-find objects in each iteration's grid state
    
    # 3. Determine the single global direction of gravity
    initial_objects = find_objects(grid, movable_colors)
    delta_r, delta_c = determine_direction(grid, initial_objects, barrier_pixels)

    # If no direction determined, return the original grid
    if delta_r == 0 and delta_c == 0:
        return grid.tolist()

    # Set to keep track of objects that have settled
    settled_object_indices = set() 
    # Assign unique IDs to objects for tracking (indices in the list work)
    
    # --- Simulation Loop ---
    while True:
        moved_this_iteration = False
        
        # Find current objects in the grid - needed if objects merge etc.
        # For this problem, shapes are static, so just tracking indices is likely ok,
        # but re-finding is safer for complex interactions. Let's use initial objects for simplicity.
        current_objects = find_objects(grid, movable_colors)
        if not current_objects: # No objects left to move
             break
             
        # Create mapping from pixel location to object index for quick lookup
        pixel_to_object_idx = {}
        for idx, obj in enumerate(current_objects):
             for r, c in obj['pixels']:
                  pixel_to_object_idx[(r, c)] = idx


        objects_to_move_this_step = [] # Store tuples: (obj_idx, current_pixels, next_pixels)

        # Determine iteration order based on gravity direction
        # Sort by key: for Down -> max row desc, Left -> min col asc, Right -> max col desc
        def sort_key(obj_idx_pair):
            idx, obj = obj_idx_pair
            if delta_r == 1: # Down
                return max(p[0] for p in obj['pixels'])
            elif delta_c == -1: # Left
                return min(p[1] for p in obj['pixels'])
            elif delta_c == 1: # Right
                return max(p[1] for p in obj['pixels'])
            return 0 # Should not happen

        sorted_object_indices = sorted(enumerate(current_objects), 
                                     key=sort_key, 
                                     reverse=(delta_r == 1 or delta_c == 1)) # Reverse for Down and Right

        # Check each object for potential movement
        for obj_idx, obj in sorted_object_indices:
            # Skip if already settled
            if obj_idx in settled_object_indices:
                continue

            can_move = True
            next_pixel_positions = []
            current_pixels = obj['pixels']
            obj_color = obj['color']

            # Calculate potential next positions for all pixels in the object
            for r, c in current_pixels:
                next_r, next_c = r + delta_r, c + delta_c
                next_pixel_positions.append((next_r, next_c))

                # Check if the next position is valid
                # 1. Out of bounds?
                if not (0 <= next_r < height and 0 <= next_c < width):
                    can_move = False
                    break
                # 2. Hits a red barrier?
                if grid[next_r, next_c] == 2:
                    can_move = False
                    break
                # 3. Hits another non-white pixel *not* part of the current object?
                if grid[next_r, next_c] != 0 and (next_r, next_c) not in current_pixels:
                     # Check if the blocking pixel belongs to an already settled object
                     blocking_obj_idx = pixel_to_object_idx.get((next_r, next_c), -1)
                     if blocking_obj_idx != -1 and blocking_obj_idx in settled_object_indices:
                          can_move = False
                          break
                     # If it hits another *moving* object in this step, allow it for now
                     # Conflict resolution happens implicitly by processing order or later checks
                     # Simplest: if target is non-0 and not self -> block.
                     can_move = False
                     break

            # If all pixels can move to valid empty spots
            if can_move:
                objects_to_move_this_step.append((obj_idx, obj_color, current_pixels, next_pixel_positions))
                moved_this_iteration = True
            else:
                # Mark this object as settled for future iterations
                settled_object_indices.add(obj_idx)

        # If no objects moved in this iteration, the simulation is stable
        if not moved_this_iteration:
            break

        # --- Apply Moves ---
        # Create a temporary grid or update carefully
        # 1. Erase old positions of moving objects
        for _, _, current_pixels, _ in objects_to_move_this_step:
            for r, c in current_pixels:
                grid[r, c] = 0
        
        # 2. Draw new positions of moving objects
        for obj_idx, color, _, next_pixels in objects_to_move_this_step:
            for r, c in next_pixels:
                # Check for conflicts again just before drawing (though sorting should handle most)
                if grid[r,c] == 0: 
                     grid[r, c] = color
                else:
                     # This case indicates a potential issue in logic or simultaneous moves
                     # For now, let the first object claim the spot based on sort order
                     # Or potentially revert this object's move and mark as settled?
                     # Let's assume sort order prevents direct conflict for now.
                     # Mark the object as settled if conflict occurs? Best approach depends on desired interaction.
                     # Fallback: If conflict, mark current obj as settled and don't draw it
                     # This needs careful handling if reverting is desired.
                     # Let's stick to overwriting based on sort order for simplicity here.
                     grid[r, c] = color # Overwrite based on processing order
                     
            # Update the object's pixel list in the main structure if needed for next iter (if not re-finding)
            # current_objects[obj_idx]['pixels'] = next_pixels # Requires obj_idx to be stable index

    # Convert the final numpy array back to a list of lists
    output_grid = grid.tolist()
    return output_grid