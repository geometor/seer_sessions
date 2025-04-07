```python
import numpy as np

"""
Transforms an input grid by iteratively propagating specific colors (Red=2, Yellow=4, Azure=8) downwards onto background cells (White=0, Blue=1), following specific movement rules and respecting obstacles (Green=3).

The propagation follows these rules:
1.  The process iterates until no changes occur in a full pass over the grid (stable state).
2.  Propagation only occurs into cells that meet ALL the following conditions:
    a) Within grid boundaries.
    b) Were originally background (White=0 or Blue=1) in the input grid.
    c) Are currently background (White=0 or Blue=1) in the grid state being updated for the current iteration.
3.  Green (3) pixels are static obstacles; they block propagation and are never overwritten.
4.  Red (2) pixels at (r, c) attempt to propagate straight down to (r+1, c). If this target cell is invalid (doesn't meet conditions in rule 2), they attempt to propagate down-left to (r+1, c-1).
5.  Yellow (4) pixels at (r, c) attempt to propagate straight down to (r+1, c). If this target cell is invalid, they attempt to propagate down-right to (r+1, c+1).
6.  Azure (8) pixels at (r, c) attempt to propagate *both* down-left (r+1, c-1) and down-right (r+1, c+1) independently in each step. Each potential target is checked against the validity conditions (rule 2).
7.  Changes calculated within one iteration step are based on the grid state at the *start* of that step. All valid propagations for the step are determined first, and then applied simultaneously to create the grid state for the next iteration.
"""

def transform(input_grid):
    """
    Applies the iterative color propagation rules to the input grid.

    Args:
        input_grid: A list of lists representing the initial grid state.

    Returns:
        A list of lists representing the final grid state after propagation stops.
    """
    # Convert to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # output_grid holds the state at the beginning of each iteration
    output_grid = input_np.copy()
    height, width = input_np.shape

    # Define background colors
    background_colors = {0, 1} # white, blue

    # Loop until no more changes occur in a full iteration (stable state)
    while True:
        # next_output_grid holds the changes calculated during the current iteration
        next_output_grid = output_grid.copy()
        # Flag to track if any change happened in this iteration
        changed_in_iteration = False

        # --- Helper function to check if a cell is a valid target for propagation in this iteration ---
        def is_valid_propagation_target(nr, nc):
            """Checks bounds, original background status, and current background status."""
            # 1. Check bounds
            if not (0 <= nr < height and 0 <= nc < width):
                return False
            # 2. Check if the target was originally background in the input grid
            if input_np[nr, nc] not in background_colors:
                return False
            # 3. Check if the target in the *next* state grid is currently background
            #    (meaning it hasn't been claimed by another propagation earlier in this *same* iteration scan)
            if next_output_grid[nr, nc] not in background_colors:
                return False
            return True

        # Iterate row by row, from top to bottom.
        # Pixels in row 'r' can potentially propagate into row 'r+1'.
        for r in range(height - 1): # The last row cannot propagate downwards
            for c in range(width):
                # Get the color from the grid state at the *start* of this iteration
                current_color = output_grid[r, c]

                # --- Apply Propagation Logic based on color ---
                if current_color == 2: # Red: Try down, if invalid, try down-left
                    target_r_down, target_c_down = r + 1, c
                    can_propagate_down = is_valid_propagation_target(target_r_down, target_c_down)

                    if can_propagate_down:
                        # Propagate down if valid
                        next_output_grid[target_r_down, target_c_down] = 2
                        changed_in_iteration = True
                    else:
                        # Down target was invalid, try down-left
                        target_r_dl, target_c_dl = r + 1, c - 1
                        if is_valid_propagation_target(target_r_dl, target_c_dl):
                            next_output_grid[target_r_dl, target_c_dl] = 2
                            changed_in_iteration = True

                elif current_color == 4: # Yellow: Try down, if invalid, try down-right
                    target_r_down, target_c_down = r + 1, c
                    can_propagate_down = is_valid_propagation_target(target_r_down, target_c_down)

                    if can_propagate_down:
                        # Propagate down if valid
                        next_output_grid[target_r_down, target_c_down] = 4
                        changed_in_iteration = True
                    else:
                        # Down target was invalid, try down-right
                        target_r_dr, target_c_dr = r + 1, c + 1
                        if is_valid_propagation_target(target_r_dr, target_c_dr):
                           next_output_grid[target_r_dr, target_c_dr] = 4
                           changed_in_iteration = True

                elif current_color == 8: # Azure: Try down-left AND down-right independently
                    # Try down-left
                    target_r_dl, target_c_dl = r + 1, c - 1
                    if is_valid_propagation_target(target_r_dl, target_c_dl):
                        next_output_grid[target_r_dl, target_c_dl] = 8
                        changed_in_iteration = True

                    # Try down-right
                    target_r_dr, target_c_dr = r + 1, c + 1
                    if is_valid_propagation_target(target_r_dr, target_c_dr):
                        next_output_grid[target_r_dr, target_c_dr] = 8
                        changed_in_iteration = True

        # --- End of Iteration ---
        # Check if the grid state has stabilized (no changes in this iteration)
        # Using np.array_equal is robust for comparing grid states.
        if np.array_equal(output_grid, next_output_grid):
            break # Exit the loop if no changes occurred

        # Update the grid state for the next iteration
        output_grid = next_output_grid

        # Alternative check using the flag (less robust if a cell is changed back and forth)
        # if not changed_in_iteration:
        #    break

    # Return the final stable grid state as a list of lists
    return output_grid.tolist()
```