
## train_1

**input:**
```
4 4 4 4 4
7 0 0 0 4
7 0 8 8 4
7 0 0 0 4
4 4 4 4 4
```


**output:**
```
4 4 4 4 4
7 0 0 0 4
7 8 8 0 4
7 0 0 0 4
4 4 4 4 4
```


## train_2

**input:**
```
5 7 7 7 5
5 0 0 0 5
5 9 9 0 5
5 9 9 0 5
5 5 5 5 5
```


**output:**
```
5 7 7 7 5
5 9 9 0 5
5 9 9 0 5
5 0 0 0 5
5 5 5 5 5
```


## train_3

**input:**
```
1 1 1 1 1
1 3 3 3 1
1 0 0 0 1
1 0 0 0 1
1 7 7 7 1
```


**output:**
```
1 1 1 1 1
1 0 0 0 1
1 0 0 0 1
1 3 3 3 1
1 7 7 7 1
```


## train_4

**input:**
```
3 3 3 3 3
3 6 0 0 7
3 0 6 0 7
3 0 0 0 7
3 3 3 3 3
```


**output:**
```
3 3 3 3 3
3 0 6 0 7
3 0 0 6 7
3 0 0 0 7
3 3 3 3 3
```


## train_5

**input:**
```
6 6 6 6 6
6 1 1 0 6
6 1 0 0 6
6 0 0 0 6
6 7 7 7 6
```


**output:**
```
6 6 6 6 6
6 0 0 0 6
6 1 1 0 6
6 1 0 0 6
6 7 7 7 6
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are always 2D grids of single-digit integers.
2.  **Background:** The digit `0` consistently represents empty space or background.
3.  **Border:** There's typically an outer border frame composed of a single digit (e.g., `4` in train_1, `5` in train_2). This border seems static. Sometimes, other non-zero digits also act as static boundaries or internal walls (like the `7`s often positioned along one edge).
4.  **Movable Objects:** Within the grid, there are contiguous blocks of identical non-zero digits (that are not the primary border digit and not `0`). These blocks appear to be the objects that move. Examples: `8`s in train_1, `9`s in train_2, `3`s in train_3, `6`s in train_4, `1`s in train_5. There can be multiple disconnected blocks of the same digit (train_4).
5.  **Target/Obstacle Objects:** The digit `7` appears in every example, forming static blocks. The movable objects seem to move *towards* these `7` blocks and stop upon reaching adjacency.
6.  **Movement:** The core transformation involves moving the "movable object(s)" within the grid. The space they vacate is filled with `0`s.
7.  **Directionality:** The direction of movement varies across examples: Left (train_1), Up (train_2), Down (train_3 & 5), Right (train_4). This direction seems determined by the relative position of the movable object(s) with respect to the target `7` block(s). The movement occurs in the primary cardinal direction towards the target.
8.  **Stopping Condition:** The movement isn't just one step (except sometimes by coincidence). It appears the movable object(s) slide iteratively, one step at a time, in the determined direction until any part of any movable object becomes adjacent (sharing an edge) to a target `7` cell or potentially another static border element. All related movable blocks stop simultaneously when the condition is met for any one part.

**YAML Facts:**


```yaml
# Task Components and Relationships

# --- Grid Definition ---
grid:
  type: 2D array
  content: single-digit integers (0-9)
  role: defines the space where transformation occurs

# --- Identified Objects ---
background:
  digit: 0
  role: represents empty space
  behavior: static, fills vacated cells

border:
  role: static frame or boundary
  identification: usually the outermost layer of identical digits, but can include other static non-zero elements (like some 7s).
  behavior: remains unchanged during transformation

movable_object:
  role: the object(s) that undergo translation
  identification: one or more contiguous blocks of identical digits that are not 0, not the primary border digit, and not the target digit (7).
  properties:
    - digit_value: varies per example (e.g., 8, 9, 3, 6, 1)
    - shape: defined by contiguous cells
    - count: can be one or more separate blocks of the same digit
  behavior: moves within the grid

target_object:
  role: defines the destination boundary or attractor for movement
  identification: contiguous block(s) of the digit 7 (based on examples)
  behavior: static, acts as a stopping point for movable_object(s)

# --- Transformation Details ---
transformation:
  type: translation
  actor: movable_object(s)
  action: move iteratively (step-by-step)
  direction:
    determination: Determined by the relative position of the movable_object(s) with respect to the target_object(s). The movement is along the cardinal axis (Up, Down, Left, Right) that represents the primary direction from movable to target.
  stopping_condition: The iterative movement stops immediately when any cell occupied by any movable_object becomes adjacent (sharing an edge, not diagonal) to any cell occupied by the target_object (digit 7) or another static border element. All movable objects cease movement together.
  effect:
    - movable_object(s) occupy new positions.
    - original positions of movable_object(s) are filled with the background digit (0).
    - border, target_object, and background remain otherwise unchanged.
```


**Natural Language Program:**

1.  Identify the background digit (0), the static border elements (typically the outermost frame digit and potentially others like the digit 7), and the movable digit(s) (non-zero, non-border, non-7).
2.  Locate all contiguous blocks of the movable digit(s) ("movable objects").
3.  Locate all contiguous blocks of the target digit (7) ("target objects").
4.  Determine the single cardinal direction (Up, Down, Left, Right) that points generally from the center(s) of the movable object(s) towards the center(s) of the target object(s).
5.  Initialize a representation of the grid state (e.g., copy the input grid).
6.  Start an iterative process:
    a.  Check if any cell occupied by a movable object is directly adjacent (sharing an edge) to any cell occupied by a target object (7) or a static border element.
    b.  If adjacency is found (stopping condition met), terminate the iteration.
    c.  If no adjacency is found, simulate one step of movement:
        i.  Calculate the next position for all cells currently occupied by movable objects by shifting them one unit in the determined direction.
        ii. Update the grid representation: change the original positions of the movable objects to the background digit (0) and place the movable objects' digits in their calculated new positions.
    d.  Repeat the iteration with the updated grid state.
7.  The final grid state after the iteration stops is the transformation output.
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
```python
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
```
