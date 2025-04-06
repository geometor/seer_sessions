import numpy as np
from typing import List, Tuple, Dict, Set, Optional

"""
Transformation Rule:
1. Identify distinct objects in the grid based on digit values:
   - Background: Digit 0.
   - Target: Digit 7 (static).
   - Movable Object: A contiguous block of identical digits (not 0 or 7). Heuristically identified as the least frequent non-0, non-7 digit, excluding potential simple border digits. Assumed unique type per grid.
   - Static Obstacles: All other non-zero digits (typically the border) that are not the target or the movable object.
2. Determine the primary cardinal direction (Up, Down, Left, Right) from the centroid of the Movable Object towards the centroid of the Target Object(s).
3. Simulate the Movable Object sliding one step at a time in the determined direction.
4. Before each step, check if the *next potential position* would result in:
   a) Any part of the Movable Object going out of grid bounds.
   b) Any part of the Movable Object colliding with a Static Obstacle cell.
   c) Any part of the Movable Object becoming adjacent (sharing an edge) to a Target (7) cell.
5. If any of conditions (a, b, c) are met for the *potential* next step, the movement stops, and the *current* position is the final position.
6. If the move is valid (none of the stop conditions met), update the grid: erase the Movable Object from its current position (fill with 0) and draw it in the new position. Update the current coordinates and repeat step 4.
7. If no Target Object (7) exists or the direction is ambiguous (e.g., centroids overlap), no movement occurs.
"""

def find_digit_coords(grid: np.ndarray, digit: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of a specific digit."""
    coords = np.argwhere(grid == digit)
    return [tuple(coord) for coord in coords]

def identify_objects(grid: np.ndarray) -> Tuple[Optional[int], List[Tuple[int, int]], List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Identifies the movable digit/coords, target coords (7), and static obstacle coords.
    Returns: (movable_digit, movable_coords, target_coords, static_obstacle_coords)
    """
    rows, cols = grid.shape
    unique_digits = np.unique(grid)

    target_coords = find_digit_coords(grid, 7)
    
    potential_movable_digits = [d for d in unique_digits if d != 0 and d != 7]
    if not potential_movable_digits:
        # No potential movable objects found (only 0s and 7s, or just 0s)
        all_non_zero_coords = [tuple(c) for c in np.argwhere(grid != 0) if grid[c[0], c[1]] != 7]
        return None, [], target_coords, all_non_zero_coords

    counts = {d: np.sum(grid == d) for d in potential_movable_digits}

    # Simple border check heuristic
    border_digit = grid[0, 0]
    is_simple_border = False
    if border_digit != 0 and border_digit != 7:
       is_simple_border = True
       # Check corners
       if grid[0, -1] != border_digit or grid[-1, 0] != border_digit or grid[-1, -1] != border_digit:
          is_simple_border = False
       # Check some edge points (crude check)
       if is_simple_border:
           for r in range(rows):
               if grid[r, 0] != border_digit and grid[r,0]!=0 : is_simple_border = False; break
               if grid[r, cols-1] != border_digit and grid[r,cols-1]!=0: is_simple_border = False; break
           if is_simple_border:
                for c in range(cols):
                   if grid[0, c] != border_digit and grid[0,c]!=0: is_simple_border = False; break
                   if grid[rows-1, c] != border_digit and grid[rows-1,c]!=0: is_simple_border = False; break

    # Filter out the border digit if it's identified
    if is_simple_border and border_digit in potential_movable_digits:
        potential_movable_digits = [d for d in potential_movable_digits if d != border_digit]
        
    movable_digit = None
    movable_coords = []
    static_obstacle_coords = []

    if not potential_movable_digits:
         # Only border and target/background exist
         movable_digit = None 
         movable_coords = []
    elif len(potential_movable_digits) == 1:
        movable_digit = potential_movable_digits[0]
        movable_coords = find_digit_coords(grid, movable_digit)
    else:
        # Ambiguous: Use frequency heuristic (least frequent non-border/non-target/non-zero)
        # Re-calculate counts for remaining potentials
        counts = {d: np.sum(grid == d) for d in potential_movable_digits}
        sorted_counts = sorted(counts.items(), key=lambda item: item[1])
        if sorted_counts:
            movable_digit = sorted_counts[0][0]
            movable_coords = find_digit_coords(grid, movable_digit)
        else: # Should not happen if potential_movable_digits is not empty
             movable_digit = None
             movable_coords = []


    # Identify all static obstacles (non-0, non-7, non-movable)
    all_non_zero_coords = np.argwhere(grid != 0)
    movable_set = set(movable_coords)
    target_set = set(target_coords)
    
    static_obstacle_coords = []
    for r, c in all_non_zero_coords:
        coord = (r, c)
        if coord not in movable_set and coord not in target_set:
            static_obstacle_coords.append(coord)
            
    return movable_digit, movable_coords, target_coords, static_obstacle_coords


def calculate_center(coords: List[Tuple[int, int]]) -> Tuple[float, float]:
    """Calculates the geometric center (average row, col) of coordinates."""
    if not coords:
        # Return center of grid? Or just origin? Let's use origin.
        return (0.0, 0.0) 
    avg_row = sum(r for r, c in coords) / len(coords)
    avg_col = sum(c for r, c in coords) / len(coords)
    return (avg_row, avg_col)

def determine_direction(movable_center: Tuple[float, float], target_center: Tuple[float, float]) -> Tuple[int, int]:
    """Determines the primary cardinal direction (dr, dc) from movable to target."""
    dr_f = target_center[0] - movable_center[0]
    dc_f = target_center[1] - movable_center[1]

    # Handle cases where centers are very close or identical
    if abs(dr_f) < 1e-6 and abs(dc_f) < 1e-6:
        return (0, 0)

    if abs(dr_f) >= abs(dc_f):
        # Move vertically
        return (1 if dr_f > 0 else -1, 0)
    else:
        # Move horizontally
        return (0, 1 if dc_f > 0 else -1)

def check_stop_condition(
    potential_coords: List[Tuple[int, int]], 
    target_set: Set[Tuple[int, int]], 
    obstacle_set: Set[Tuple[int, int]], 
    grid_shape: Tuple[int, int]
) -> bool:
    """Checks if the potential next move leads to a stop condition."""
    rows, cols = grid_shape
    for r, c in potential_coords:
        # 1. Check grid bounds
        if not (0 <= r < rows and 0 <= c < cols):
            return True  # Stop: Out of bounds
        
        # 2. Check collision with static obstacles
        if (r, c) in obstacle_set:
            return True # Stop: Collision with obstacle
            
        # 3. Check adjacency to target
        for dr_adj, dc_adj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            adj_r, adj_c = r + dr_adj, c + dc_adj
            if (adj_r, adj_c) in target_set:
                return True # Stop: Adjacent to target
                
    return False # No stop condition met

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Moves a block of digits towards the '7' block until adjacent or blocked.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # --- 1. Identify Components ---
    movable_digit, current_movable_coords, target_coords, static_obstacle_coords = identify_objects(grid)

    # Handle cases with no movable object
    if movable_digit is None or not current_movable_coords:
        return output_grid.tolist()

    # Convert lists to sets for efficient lookup
    target_set = set(target_coords)
    static_obstacle_set = set(static_obstacle_coords)

    # --- 2. Determine Movement Direction ---
    movable_center = calculate_center(current_movable_coords)
    target_center = calculate_center(target_coords)
    
    # If no target 7s, stay put.
    if not target_coords:
         dr, dc = (0,0)
    else:
         dr, dc = determine_direction(movable_center, target_center)

    # If direction is (0,0) (e.g., centers coincide or no target), no movement needed
    if dr == 0 and dc == 0:
         return output_grid.tolist()

    # --- 3. Iterative Movement ---
    while True:
        # --- 3a. Calculate Potential Next Position ---
        potential_next_coords = [(r + dr, c + dc) for r, c in current_movable_coords]

        # --- 3b. Check Stopping Conditions for Potential Position ---
        if check_stop_condition(potential_next_coords, target_set, static_obstacle_set, (rows, cols)):
            break # Stop movement, current position is final

        # --- 3c. Execute Move (if no stop condition) ---
        # Clear old positions
        for r, c in current_movable_coords:
            output_grid[r, c] = 0
        # Place in new positions
        for nr, nc in potential_next_coords:
            # Ensure we don't write out of bounds if check_stop_condition had a bug
            if 0 <= nr < rows and 0 <= nc < cols:
                 output_grid[nr, nc] = movable_digit
            else:
                 # This case indicates an issue, maybe log or raise error
                 # For now, just prevent writing out of bounds
                 pass 

        # Update coordinates for the next iteration
        current_movable_coords = potential_next_coords
        
        # Safety break: Prevent infinite loops in case of unexpected state
        # This requires tracking previous states, let's omit for now and rely on stop conditions

    # --- 4. Finalize ---
    return output_grid.tolist()