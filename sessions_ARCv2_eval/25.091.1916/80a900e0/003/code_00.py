import numpy as np

"""
Simulates the movement of colored pixels on a grid based on specific rules.

The grid contains a background checkerboard pattern (blue=1, white=0) and foreground pixels of different colors.
Green (3) pixels are static obstacles.
Red (2), Yellow (4), and Azure (8) pixels are mobile.
The simulation proceeds in discrete steps until no pixels can move.

Rules per step:
1.  Identify all mobile pixels in the current grid state.
2.  For each mobile pixel, determine its potential next position(s) based on its color:
    - Red (2): Tries to move one step down. If the cell below is blocked (out of bounds, not background, or already claimed in this step), it tries to move one step down-left.
    - Yellow (4): Tries to move one step down. If the cell below is blocked, it tries to move one step down-right.
    - Azure (8): Tries to move *both* one step down-left and one step down-right simultaneously. Each potential move is evaluated independently.
3.  A move is valid only if the target cell is within grid bounds, contains a background color (0 or 1) in the *current* grid state, and has not already been claimed by another pixel moving in the *same* step.
4.  Conflicts for the same target cell are resolved by prioritizing the pixel encountered first during a top-down, left-right scan of the grid.
5.  All valid moves are determined based on the grid state at the beginning of the step.
6.  After identifying all valid moves for the step:
    - Create the next grid state.
    - Place the moved pixels in their new target cells.
    - For each pixel that successfully moved, clear its original cell by restoring the background color (0 or 1) from the initial input grid. An Azure pixel's original cell is cleared if at least one of its potential moves (down-left or down-right) was successful.
7.  Repeat steps 1-6 until a step occurs where no pixels move.
8.  Return the final grid state.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the iterative pixel movement simulation to the input grid.

    Args:
        input_grid: A list of lists representing the initial grid state.

    Returns:
        A list of lists representing the final grid state after simulation.
    """
    input_np = np.array(input_grid, dtype=int)
    current_grid = input_np.copy()
    height, width = input_np.shape
    background_colors = {0, 1} # white, blue
    mobile_colors = {2, 4, 8} # red, yellow, azure

    while True:
        moved_in_step = False
        # next_grid starts as a copy, modifications happen based on calculated moves
        next_grid = current_grid.copy()
        # Keep track of targets claimed in this step to handle conflicts
        occupied_targets_this_step = set()
        # Keep track of sources that successfully initiated a move
        sources_to_clear_this_step = set()
        # Store the actual moves to perform after scanning the whole grid
        moves_to_make = [] # Stores tuples of (target_r, target_c, color)

        # --- Scan the grid to determine all valid moves for this step ---
        for r in range(height):
            for c in range(width):
                current_color = current_grid[r, c]

                if current_color not in mobile_colors:
                    continue

                # --- Helper function to check if a move to (nr, nc) is valid ---
                def can_move_to(nr, nc):
                    # Check bounds
                    if not (0 <= nr < height and 0 <= nc < width):
                        return False
                    # Check if target is currently background
                    if current_grid[nr, nc] not in background_colors:
                        return False
                    # Check if target is already claimed in this step
                    if (nr, nc) in occupied_targets_this_step:
                        return False
                    return True

                # --- Determine potential moves based on color ---
                if current_color == 2: # Red
                    moved_pixel = False
                    # Try down
                    target_r, target_c = r + 1, c
                    if can_move_to(target_r, target_c):
                        occupied_targets_this_step.add((target_r, target_c))
                        moves_to_make.append((target_r, target_c, 2))
                        sources_to_clear_this_step.add((r, c))
                        moved_in_step = True
                        moved_pixel = True
                    # Else try down-left
                    elif not moved_pixel:
                        target_r, target_c = r + 1, c - 1
                        if can_move_to(target_r, target_c):
                            occupied_targets_this_step.add((target_r, target_c))
                            moves_to_make.append((target_r, target_c, 2))
                            sources_to_clear_this_step.add((r, c))
                            moved_in_step = True
                            moved_pixel = True


                elif current_color == 4: # Yellow
                    moved_pixel = False
                    # Try down
                    target_r, target_c = r + 1, c
                    if can_move_to(target_r, target_c):
                        occupied_targets_this_step.add((target_r, target_c))
                        moves_to_make.append((target_r, target_c, 4))
                        sources_to_clear_this_step.add((r, c))
                        moved_in_step = True
                        moved_pixel = True
                    # Else try down-right
                    elif not moved_pixel:
                        target_r, target_c = r + 1, c + 1
                        if can_move_to(target_r, target_c):
                            occupied_targets_this_step.add((target_r, target_c))
                            moves_to_make.append((target_r, target_c, 4))
                            sources_to_clear_this_step.add((r, c))
                            moved_in_step = True
                            moved_pixel = True

                elif current_color == 8: # Azure
                    moved_azure_component = False
                    # Try down-left (independent)
                    target_r_left, target_c_left = r + 1, c - 1
                    if can_move_to(target_r_left, target_c_left):
                        occupied_targets_this_step.add((target_r_left, target_c_left))
                        moves_to_make.append((target_r_left, target_c_left, 8))
                        moved_in_step = True
                        moved_azure_component = True

                    # Try down-right (independent)
                    target_r_right, target_c_right = r + 1, c + 1
                    if can_move_to(target_r_right, target_c_right):
                        occupied_targets_this_step.add((target_r_right, target_c_right))
                        moves_to_make.append((target_r_right, target_c_right, 8))
                        moved_in_step = True
                        moved_azure_component = True

                    # If at least one component moved, mark the source for clearing
                    if moved_azure_component:
                        sources_to_clear_this_step.add((r, c))


        # --- If no pixels moved in this step, simulation is done ---
        if not moved_in_step:
            break

        # --- Apply the changes for the next step ---
        # 1. Clear the source cells of moved pixels (restore original background)
        for r, c in sources_to_clear_this_step:
             # Only clear if it wasn't occupied by another move in the same step
             if (r,c) not in occupied_targets_this_step:
                next_grid[r, c] = input_np[r, c] # Restore original background

        # 2. Place the pixels in their new target locations
        for r, c, color in moves_to_make:
            next_grid[r, c] = color

        # Update the grid for the next iteration
        current_grid = next_grid

    # Return the final state as a list of lists
    return current_grid.tolist()