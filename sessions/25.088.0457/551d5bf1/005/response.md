```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1. Copy the input grid to create the output grid.
2. Identify Exterior White Pixels: Perform a flood fill (BFS) starting from all white (0) pixels on the grid borders. Mark all reachable white pixels as 'exterior'.
3. Initial Fill: Iterate through the grid. Change any white (0) pixel that was *not* marked as 'exterior' to azure (8). Keep track of the coordinates of these 'initially filled' azure pixels.
4. Identify Leak Points and Directions: Iterate through the initially filled azure pixels. For each azure pixel, check its four orthogonal neighbors. If a neighbor is white (0) *and* was marked as 'exterior' in Step 2, then this neighbor is a 'leak point'. Record the coordinates of the leak point and the direction *away* from the initial azure pixel (e.g., if the white neighbor is above the azure pixel, the leak direction is 'Up'). Store these leak points along with their respective propagation directions. Store these as tuples: `(r, c, dr, dc)`.
5. Propagate Leaks:
   - Initialize a set `filled_by_leak` to store coordinates of pixels colored azure during this step. Add coordinates of initially filled azure pixels from Step 3 to this set initially to prevent leaks from overwriting the initial fill areas.
   - Iterate through each identified leak point and its direction `(start_r, start_c, dr, dc)`:
     - Start at the leak point coordinates `r, c = start_r, start_c`.
     - Repeatedly step in the determined direction:
       - Check the current cell `(r, c)`:
         - Is `(r, c)` outside the grid boundaries? Stop.
         - Is `output_grid[r, c]` not white (0)? Stop.
         - Is `(r, c)` already in `filled_by_leak`? Stop.
       - If none of the stopping conditions are met:
         - Change `output_grid[r, c]` to azure (8).
         - Add `(r, c)` to the `filled_by_leak` set.
         - Update coordinates for the next step: `r, c = r + dr, c + dc`.
       - If any stopping condition is met, break the inner loop and move to the next leak point.
6. Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies a fill and leak transformation based on refined rules. Fills enclosed
    white areas and then propagates leaks from these areas outwards into exterior
    white areas until hitting boundaries or non-white pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    output_grid = input_array.copy() # Step 1: Copy input
    rows, cols = input_array.shape
    
    white = 0
    blue = 1  # Assuming blue (1) is the primary obstacle color
    azure = 8

    # Helper to check if coordinates are within grid bounds
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    # Step 2: Identify Exterior White Pixels using flood fill from borders
    is_exterior = np.zeros_like(input_array, dtype=bool)
    q_exterior = deque()

    # Add all border white cells to the queue
    for r in range(rows):
        for c in [0, cols - 1]:
            if is_valid(r, c) and output_grid[r, c] == white and not is_exterior[r, c]:
                is_exterior[r, c] = True
                q_exterior.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
             if is_valid(r, c) and output_grid[r, c] == white and not is_exterior[r, c]:
                is_exterior[r, c] = True
                q_exterior.append((r, c))

    # Perform flood fill for exterior white cells
    while q_exterior:
        r, c = q_exterior.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and output_grid[nr, nc] == white and not is_exterior[nr, nc]:
                is_exterior[nr, nc] = True
                q_exterior.append((nr, nc))

    # Step 3: Fill enclosed white areas (those not exterior) with azure
    initial_fill_coords = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == white and not is_exterior[r, c]:
                output_grid[r, c] = azure
                initial_fill_coords.append((r, c))

    # Initialize set to track all azure-filled cells (initial + leaks)
    filled_by_leak = set(initial_fill_coords)

    # Step 4: Identify Leak Points and Directions
    leak_starts = [] # List to store (r, c, dr, dc) tuples

    for r_az, c_az in initial_fill_coords:
        # Check neighbors of initially filled azure pixels
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_az + dr, c_az + dc # Coordinates of the neighbor

            # Check if neighbor is a valid, exterior white pixel (potential leak point)
            if is_valid(nr, nc) and output_grid[nr, nc] == white and is_exterior[nr, nc]:
                # The direction of propagation is (dr, dc) - away from the azure cell
                leak_starts.append((nr, nc, dr, dc))

    # Step 5: Propagate Leaks
    # Use a set to avoid adding duplicate starting points for propagation if multiple
    # initial azure cells border the same exterior white cell.
    processed_leak_starts = set()
    
    for start_r, start_c, dr, dc in leak_starts:
        
        # Ensure we process each unique leak *starting point* only once per direction
        # Note: A single point might leak in multiple directions if bordered by multiple azure cells initially.
        # The current structure handles this as separate entries in leak_starts.
        # We only need to ensure we don't re-process the *exact same* (r, c, dr, dc) tuple if it arises.
        # Let's refine this - we should only process a starting CELL once per direction.
        # A simple check before propagation loop suffices.
        
        # Current position for propagation
        r, c = start_r, start_c

        while True:
            # Check stopping conditions for the *current* cell (r, c)
            if not is_valid(r, c):
                break # Out of bounds
            if output_grid[r, c] != white:
                 # Check if it's already azure (from initial fill or another leak)
                 # We only want to stop if it's an obstacle (like blue) or already azure
                 # If it's azure and *not* in filled_by_leak, something is wrong.
                 # If it's azure and *in* filled_by_leak, stop.
                 # If it's blue (or other non-white), stop.
                 if output_grid[r,c] == azure and (r,c) in filled_by_leak:
                      break 
                 elif output_grid[r,c] != white: # Hit blue or other obstacle
                      break

            # Check if this cell has already been filled by *this* propagation step or another
            if (r, c) in filled_by_leak:
                 # This check seems redundant given the color check above, 
                 # but keep it for safety. If it's white, it shouldn't be in filled_by_leak yet.
                 # If it's azure, the check above handles it. Let's remove this specific check.
                 # The crucial check is that output_grid[r,c] must be white to proceed.
                 pass # Continue to color it below if white


            # If conditions met, fill the current cell and move to the next
            output_grid[r, c] = azure
            filled_by_leak.add((r, c))

            # Update coordinates for the next step
            r, c = r + dr, c + dc


    # Step 6: Return the final grid
    return output_grid.tolist()
```