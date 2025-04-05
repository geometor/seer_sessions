import numpy as np
from typing import List, Tuple, Dict, Set, Optional

"""
Transformation Rule:
1. Identify distinct objects: Background (0), Target (7), Movable Object (heuristic: non-0/7, not simple border, least frequent if ambiguous), and Static Obstacles (other non-0).
2. Determine the single cardinal movement direction (dr, dc) from the Movable Object's centroid towards the Target Object's centroid.
3. Iteratively move the Movable Object one step in the determined direction until a stop condition is met.
4. Stop conditions (checked *before* executing a move):
    a) Any part of the Movable Object is currently adjacent (sharing an edge) to any part of the Target Object (7).
    b) The *next* potential move would cause any part of the Movable Object to go out of grid bounds.
    c) The *next* potential move would cause any part of the Movable Object to collide with (land on) a Static Obstacle cell.
5. If no stop condition is met, execute the move: erase the Movable Object from its current position (fill with 0) and draw it in the new position. Update the object's coordinates and repeat the loop.
6. If no Target Object (7) exists or the direction is ambiguous (e.g., centroids overlap), no movement occurs.
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

    # Identify Target (7)
    target_coords = find_digit_coords(grid, 7)
    
    # Identify potential movable digits (non-0, non-7)
    potential_movable_digits = [d for d in unique_digits if d != 0 and d != 7]
    if not potential_movable_digits:
        # No potential movable objects found (only 0s and 7s, or just 0s)
        # All non-zero, non-7 are static obstacles in this case
        static_obstacle_coords = [tuple(c) for c in np.argwhere(grid != 0) if grid[c[0], c[1]] != 7]
        return None, [], target_coords, static_obstacle_coords

    counts = {d: np.sum(grid == d) for d in potential_movable_digits}

    # Simple border check heuristic: check if the outermost layer is composed of a single potential digit
    border_digit = -1 # Use -1 to indicate no simple border found or border is 0/7
    potential_border_digit = grid[0,0]
    if potential_border_digit in potential_movable_digits:
        is_simple_border = True
        # Check corners
        if not (grid[0, -1] == potential_border_digit and \
                grid[-1, 0] == potential_border_digit and \
                grid[-1, -1] == potential_border_digit):
            is_simple_border = False
        # Check edges (ensure all non-zero edge cells match potential_border_digit)
        if is_simple_border:
            for r in range(rows):
                if grid[r, 0] != 0 and grid[r, 0] != potential_border_digit: is_simple_border = False; break
                if grid[r, cols-1] != 0 and grid[r, cols-1] != potential_border_digit: is_simple_border = False; break
            if is_simple_border:
                for c in range(cols):
                    if grid[0, c] != 0 and grid[0, c] != potential_border_digit: is_simple_border = False; break
                    if grid[rows-1, c] != 0 and grid[rows-1, c] != potential_border_digit: is_simple_border = False; break
        
        if is_simple_border:
            border_digit = potential_border_digit


    # Filter out the identified border digit from potential movable digits
    if border_digit != -1:
        potential_movable_digits = [d for d in potential_movable_digits if d != border_digit]

    # Determine the movable digit
    movable_digit = None
    if not potential_movable_digits:
        # Only border and target/background exist
        movable_digit = None
    elif len(potential_movable_digits) == 1:
        movable_digit = potential_movable_digits[0]
    else:
        # Ambiguous: Use frequency heuristic (least frequent non-border/non-target/non-zero)
        counts_filtered = {d: counts[d] for d in potential_movable_digits}
        sorted_counts = sorted(counts_filtered.items(), key=lambda item: item[1])
        if sorted_counts:
            movable_digit = sorted_counts[0][0] # Choose least frequent
        # If still ambiguous (e.g., equal counts), this picks the one with the lower digit value first due to sorting tie-breaking

    # Get coordinates for the identified objects
    movable_coords = []
    if movable_digit is not None:
        movable_coords = find_digit_coords(grid, movable_digit)

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


def calculate_center(coords: List[Tuple[int, int]]) -> Optional[Tuple[float, float]]:
    """Calculates the geometric center (average row, col) of coordinates."""
    if not coords:
        return None
    avg_row = sum(r for r, c in coords) / len(coords)
    avg_col = sum(c for r, c in coords) / len(coords)
    return (avg_row, avg_col)

def determine_direction(movable_center: Optional[Tuple[float, float]], target_center: Optional[Tuple[float, float]]) -> Tuple[int, int]:
    """Determines the primary cardinal direction (dr, dc) from movable to target."""
    if movable_center is None or target_center is None:
        return (0, 0) # No movement if either object doesn't exist

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

def check_adjacency(coords: List[Tuple[int, int]], target_set: Set[Tuple[int, int]]) -> bool:
    """Checks if any coord in the list is adjacent to any coord in the target_set."""
    for r, c in coords:
        for dr_adj, dc_adj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            adj_r, adj_c = r + dr_adj, c + dc_adj
            if (adj_r, adj_c) in target_set:
                return True # Found adjacency
    return False # No adjacency found

def check_path_validity(
    potential_coords: List[Tuple[int, int]], 
    obstacle_set: Set[Tuple[int, int]], 
    grid_shape: Tuple[int, int]
) -> bool:
    """Checks if the potential move is valid (within bounds and no collision with obstacles)."""
    rows, cols = grid_shape
    for r, c in potential_coords:
        # Check grid bounds
        if not (0 <= r < rows and 0 <= c < cols):
            return False  # Invalid: Out of bounds
        # Check collision with static obstacles
        if (r, c) in obstacle_set:
            return False # Invalid: Collision with obstacle
    return True # Path is valid


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Moves a block of digits towards the '7' block until adjacent or blocked.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # --- 1. Identify Components ---
    movable_digit, current_movable_coords, target_coords, static_obstacle_coords = identify_objects(grid)

    # If no movable object identified, return the original grid
    if movable_digit is None or not current_movable_coords:
        return output_grid.tolist()

    # Convert lists to sets for efficient lookup
    target_set = set(target_coords)
    static_obstacle_set = set(static_obstacle_coords)

    # --- 2. Determine Movement Direction ---
    movable_center = calculate_center(current_movable_coords)
    target_center = calculate_center(target_coords)
    dr, dc = determine_direction(movable_center, target_center)

    # If no direction (e.g., no target, or centers coincide), return original grid
    if dr == 0 and dc == 0:
        return output_grid.tolist()

    # --- 3. Iterative Movement ---
    while True:
        # --- 3a. Check Stop Condition: Adjacency to Target ---
        # Check if the *current* position is adjacent to the target
        if check_adjacency(current_movable_coords, target_set):
            break # Stop: Already adjacent

        # --- 3b. Calculate Potential Next Position ---
        potential_next_coords = [(r + dr, c + dc) for r, c in current_movable_coords]

        # --- 3c. Check Stop Condition: Path Validity for Next Step ---
        # Check if the *next* move would be invalid (out of bounds or collision)
        if not check_path_validity(potential_next_coords, static_obstacle_set, (rows, cols)):
            break # Stop: Next move is blocked

        # --- 3d. Execute Move (if no stop conditions met) ---
        # Clear old positions in the output grid
        for r, c in current_movable_coords:
            output_grid[r, c] = 0
        # Place movable object in new positions in the output grid
        for nr, nc in potential_next_coords:
            # Double check bounds just in case check_path_validity had a flaw
            if 0 <= nr < rows and 0 <= nc < cols:
                 output_grid[nr, nc] = movable_digit
            
        # Update coordinates for the next iteration
        current_movable_coords = potential_next_coords
        
        # Basic safety break to prevent potential infinite loops in unexpected scenarios, limit steps.
        # A better approach might involve state tracking if needed.
        # For now, relying on stop conditions.

    # --- 4. Finalize ---
    return output_grid.tolist()