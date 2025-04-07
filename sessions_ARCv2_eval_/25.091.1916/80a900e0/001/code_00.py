import numpy as np

"""
Transforms an input grid based on color-specific propagation rules over a checkerboard background.

1.  Initialize the output grid as a copy of the input grid.
2.  Identify background pixels (blue=1, white=0) from the original input grid.
3.  Repeatedly iterate through the grid until no pixels can propagate further in a full pass:
    a.  Create a temporary grid for the next state based on the current state.
    b.  For each pixel in the current grid:
        i.  If the pixel is Red (2):
            - Try to propagate Red to the cell directly below (r+1, c).
            - If the target cell is within bounds, was originally background, and is currently background in the next state grid, change it to Red in the next state grid.
            - If propagation straight down fails, try propagating Red to the cell down-left (r+1, c-1) under the same conditions.
        ii. If the pixel is Yellow (4):
            - Try to propagate Yellow to the cell directly below (r+1, c).
            - If the target cell is within bounds, was originally background, and is currently background in the next state grid, change it to Yellow in the next state grid.
            - If propagation straight down fails, try propagating Yellow to the cell down-right (r+1, c+1) under the same conditions.
        iii. If the pixel is Azure (8):
            - Try to propagate Azure to the cell down-left (r+1, c-1). If the target cell is within bounds, was originally background, and is currently background in the next state grid, change it to Azure in the next state grid.
            - Try to propagate Azure to the cell down-right (r+1, c+1). If the target cell is within bounds, was originally background, and is currently background in the next state grid, change it to Azure in the next state grid. (These are independent attempts).
    c.  Update the main grid with the next state.
    d.  If no changes were made in this pass, terminate the iteration.
4.  Return the final grid state. Green (3) pixels are static and act as blockers but are never overwritten.
"""

def transform(input_grid):
    """
    Applies the color propagation rules to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = input_np.copy()
    height, width = input_np.shape
    background_colors = {0, 1} # white, blue

    while True:
        changed = False
        # Create a grid for the next state based on the current state.
        # This prevents changes within one iteration from immediately causing further changes in the same iteration.
        next_output_grid = output_grid.copy()

        # Iterate row by row, from top to bottom
        for r in range(height - 1): # No need to check the last row as propagation is downwards
            for c in range(width):
                current_color = output_grid[r, c]

                # --- Helper function to check propagation validity ---
                def is_valid_target(nr, nc):
                    # Check bounds
                    if not (0 <= nr < height and 0 <= nc < width):
                        return False
                    # Check if the target was originally background
                    if input_np[nr, nc] not in background_colors:
                        return False
                     # Check if the target in the *next* state is currently background (not yet filled in this iteration)
                    if next_output_grid[nr, nc] not in background_colors:
                         return False
                    return True

                # --- Propagation Logic ---
                if current_color == 2: # Red
                    # Try down
                    target_r, target_c = r + 1, c
                    propagated_down = False
                    if is_valid_target(target_r, target_c):
                        if next_output_grid[target_r, target_c] != 2: # Avoid redundant changes
                           next_output_grid[target_r, target_c] = 2
                           changed = True
                           propagated_down = True
                    # If down failed, try down-left
                    if not propagated_down:
                        target_r, target_c = r + 1, c - 1
                        if is_valid_target(target_r, target_c):
                           if next_output_grid[target_r, target_c] != 2:
                                next_output_grid[target_r, target_c] = 2
                                changed = True

                elif current_color == 4: # Yellow
                    # Try down
                    target_r, target_c = r + 1, c
                    propagated_down = False
                    if is_valid_target(target_r, target_c):
                       if next_output_grid[target_r, target_c] != 4:
                           next_output_grid[target_r, target_c] = 4
                           changed = True
                           propagated_down = True
                    # If down failed, try down-right
                    if not propagated_down:
                        target_r, target_c = r + 1, c + 1
                        if is_valid_target(target_r, target_c):
                            if next_output_grid[target_r, target_c] != 4:
                                next_output_grid[target_r, target_c] = 4
                                changed = True

                elif current_color == 8: # Azure
                    # Try down-left (independent)
                    target_r_left, target_c_left = r + 1, c - 1
                    if is_valid_target(target_r_left, target_c_left):
                        if next_output_grid[target_r_left, target_c_left] != 8:
                            next_output_grid[target_r_left, target_c_left] = 8
                            changed = True
                    # Try down-right (independent)
                    target_r_right, target_c_right = r + 1, c + 1
                    if is_valid_target(target_r_right, target_c_right):
                        if next_output_grid[target_r_right, target_c_right] != 8:
                            next_output_grid[target_r_right, target_c_right] = 8
                            changed = True

        # Update the main grid for the next iteration
        output_grid = next_output_grid

        # If no changes occurred in this full pass, the simulation is stable
        if not changed:
            break

    # Return the final state as a list of lists
    return output_grid.tolist()