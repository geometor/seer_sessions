```python
import numpy as np

"""
Identifies a 'movable object' (a block of identical digits, not 0 and not 7, distinct from the main border digit) 
and a 'target object' (block of digit 7). Determines the primary cardinal direction from the movable object towards 
the target object. Iteratively moves the movable object one step at a time in that direction, filling its previous 
location with 0s. The movement stops when any part of the movable object becomes adjacent (up, down, left, or right) 
to any part of the target object (7) or any other static non-zero digit (like the border).
"""

def find_digit_coords(grid, digit):
    """Finds all coordinates (row, col) of a specific digit in the grid."""
    coords = np.argwhere(grid == digit)
    return [tuple(coord) for coord in coords]

def find_movable_and_static(grid):
    """
    Identifies the movable digit, its coordinates, and coordinates of all static elements (non-zero, non-movable).
    Assumes there's only one type of movable digit per grid (excluding 0 and 7).
    Assumes 7 is always static/target.
    """
    unique_digits = np.unique(grid)
    potential_movable = [d for d in unique_digits if d != 0 and d != 7]
    
    # Heuristic: Often the border is the most frequent digit excluding 0.
    # Or, the movable object might be less frequent. Let's find the digit that isn't 0 or 7
    # and isn't surrounding the grid completely (simple border check).
    
    movable_digit = -1
    rows, cols = grid.shape
    
    counts = {d: np.sum(grid == d) for d in potential_movable}

    # A simple check: if a digit forms the entire outer frame, it's likely the border.
    # Check corners and some edge midpoints.
    corner_val = grid[0, 0]
    is_simple_border = True
    if grid[0, -1] != corner_val or grid[-1, 0] != corner_val or grid[-1, -1] != corner_val or \
       grid[0, cols//2] != corner_val or grid[-1, cols//2] != corner_val or \
       grid[rows//2, 0] != corner_val or grid[rows//2, -1] != corner_val:
           is_simple_border = False

    # If there's only one potential digit, it's the movable one.
    if len(potential_movable) == 1:
        movable_digit = potential_movable[0]
    # If multiple, try to exclude the simple border if found.
    elif is_simple_border and corner_val in potential_movable:
         # Assume the non-border digit is movable. This might need refinement for complex cases.
         other_potential = [d for d in potential_movable if d != corner_val]
         if len(other_potential) == 1:
             movable_digit = other_potential[0]
         else:
             # If still ambiguous, maybe pick the least frequent non-7, non-0 digit?
             # Or the one not touching the edge? This needs better logic for edge cases.
             # For now, let's fallback or raise an error if ambiguous.
             # Trying least frequent as a guess for the examples provided.
              sorted_counts = sorted(counts.items(), key=lambda item: item[1])
              if sorted_counts:
                  movable_digit = sorted_counts[0][0] # Assume least frequent non-0/7 is movable
              else:
                    raise ValueError("Could not definitively identify movable digit.")

    else:
         # No simple border, pick least frequent?
         sorted_counts = sorted(counts.items(), key=lambda item: item[1])
         if sorted_counts:
             movable_digit = sorted_counts[0][0]
         else:
            # This case happens if grid only has 0s and 7s, or just 0s.
            movable_digit = -1 # Indicate no movable object found

    if movable_digit == -1 and len(potential_movable) > 0:
         # Default guess if logic failed: assume the first potential one found
         # This is risky and likely needs refinement based on more examples.
         # Let's stick to the least frequent as the primary guess if ambiguity remains.
         sorted_counts = sorted(counts.items(), key=lambda item: item[1])
         if sorted_counts:
             movable_digit = sorted_counts[0][0]
         else:
              movable_digit = -1 # No movable object

    if movable_digit == -1:
         movable_coords = []
         static_coords = find_digit_coords(grid, -1) # Find all non-zero coords
         all_non_zero = np.argwhere(grid != 0)
         static_coords = [tuple(coord) for coord in all_non_zero]

    else:
        movable_coords = find_digit_coords(grid, movable_digit)
        
        static_coords = []
        non_zero_coords = np.argwhere(grid != 0)
        movable_set = set(movable_coords)
        for r, c in non_zero_coords:
            if (r, c) not in movable_set:
                static_coords.append((r,c))

    return movable_digit, movable_coords, static_coords


def calculate_center(coords):
    """Calculates the geometric center (average row, col) of a list of coordinates."""
    if not coords:
        return (0, 0)
    avg_row = sum(r for r, c in coords) / len(coords)
    avg_col = sum(c for r, c in coords) / len(coords)
    return (avg_row, avg_col)

def determine_direction(movable_center, target_center):
    """Determines the primary cardinal direction (dr, dc) from movable to target."""
    dr = target_center[0] - movable_center[0]
    dc = target_center[1] - movable_center[1]

    if abs(dr) >= abs(dc):
        # Move vertically
        return (1 if dr > 0 else -1, 0) if dr != 0 else (0, 0) # Return (0,0) if centers coincide
    else:
        # Move horizontally
        return (0, 1 if dc > 0 else -1) if dc != 0 else (0, 0) # Return (0,0) if centers coincide

def check_adjacency(grid_shape, movable_coords, static_coords):
    """Checks if any movable cell is adjacent to any static cell."""
    rows, cols = grid_shape
    static_set = set(static_coords)
    for r, c in movable_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds implicitly by checking membership in static_set
            if (nr, nc) in static_set:
                return True
    return False

def transform(input_grid):
    """
    Moves a block of digits towards the '7' block until adjacent.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # 1. Identify components
    movable_digit, movable_coords, static_coords = find_movable_and_static(grid)
    target_coords = find_digit_coords(grid, 7)
    
    # Add target coordinates to static coordinates for adjacency check
    all_static_coords = list(set(static_coords + target_coords))


    # Handle cases with no movable object
    if movable_digit == -1 or not movable_coords:
        return output_grid.tolist() # Return original grid if no movable object

    # 2. Determine movement direction
    movable_center = calculate_center(movable_coords)
    target_center = calculate_center(target_coords)
    
    # If no target 7s, maybe move towards center? Or stay put? Let's assume stay put.
    if not target_coords:
         dr, dc = (0,0)
    else:
         dr, dc = determine_direction(movable_center, target_center)

    # If direction is (0,0), no movement needed
    if dr == 0 and dc == 0:
         return output_grid.tolist()

    # 3. Iterative movement
    current_movable_coords = list(movable_coords) # Work with a copy

    while True:
        # 3a. Check stopping condition (adjacency to ANY static element, including 7)
        if check_adjacency((rows, cols), current_movable_coords, all_static_coords):
            break

        # 3b. Calculate next positions
        next_movable_coords = []
        valid_move = True
        for r, c in current_movable_coords:
            nr, nc = r + dr, c + dc
            # Check bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                valid_move = False
                break
            # Check if the target cell is currently occupied by another static object (shouldn't happen if adjacency works)
            # Or if it's part of the *current* movable object (relevant for multi-cell objects moving onto their own space)
            if (nr, nc) in all_static_coords:
                 valid_move = False # Cannot move into a static cell
                 break
            # Check collision with self (important for larger shapes)
            is_part_of_current_movable = False
            for rr, cc in current_movable_coords:
                if nr == rr and nc == cc:
                    is_part_of_current_movable = True
                    break
            # Allow moving into '0' or into a space previously occupied by another part of the *same* object in this step
            if output_grid[nr, nc] != 0 and not is_part_of_current_movable:
                 # This case should ideally be covered by static check, but double check just in case.
                 # Or, this handles collision if multiple different movable objects were present.
                 # Since we assume one type, this should mainly catch static obj collision.
                 valid_move = False
                 break

            next_movable_coords.append((nr, nc))

        if not valid_move:
            # Should ideally stop due to adjacency check before hitting this,
            # but acts as a failsafe (e.g., if somehow moving into border).
            break

        # 3c. Update grid state if move is valid
        # Clear old positions
        for r, c in current_movable_coords:
            output_grid[r, c] = 0
        # Place in new positions
        for nr, nc in next_movable_coords:
            output_grid[nr, nc] = movable_digit

        # Update coordinates for the next iteration
        current_movable_coords = next_movable_coords

    return output_grid.tolist()
```