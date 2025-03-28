```python
import numpy as np
from scipy.ndimage import label

"""
Simulates gravity acting on connected objects of the same color in a grid.
Non-white objects (contiguous blocks of the same color, excluding white/0) fall 
downwards into white space (pixels with value 0) step by step. 
In each step, all objects that *can* fall one unit down without obstruction do so.
An object is obstructed if any pixel directly below any of its constituent pixels 
is either the grid boundary or a non-white pixel that is *not* part of the 
falling object itself. The process repeats until no object can move further down, 
reaching a stable state. Objects maintain their shape throughout the process.
"""

import numpy as np
from scipy.ndimage import label

def transform(input_grid):
    """
    Applies object-based gravity step-by-step to the input grid until stable.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the grid after gravity simulation.
    """
    working_grid = np.array(input_grid, dtype=int)
    height, width = working_grid.shape

    while True:
        moved_in_iteration = False
        
        # --- Identify all potential objects in the current grid state ---
        objects_data = [] # List to store info about each object found
        unique_colors = np.unique(working_grid[working_grid != 0])

        for color in unique_colors:
            mask = (working_grid == color)
            # Find connected components for the current color
            labeled_array, num_labels = label(mask) 
            
            # Store coordinates for each distinct object of this color
            for i in range(1, num_labels + 1):
                coords = np.argwhere(labeled_array == i)
                objects_data.append({'color': color, 'coords': coords})

        # --- Determine which objects can move down one step ---
        objects_to_move_this_step = [] # List of objects that will be moved
        
        # Create a temporary grid representing the current state
        # Used for checking collisions below objects accurately
        current_grid_state = working_grid.copy()

        for obj in objects_data:
            coords = obj['coords']
            color = obj['color']
            can_move_down = True # Assume it can move initially

            # Check below each pixel of the object
            for r, c in coords:
                r_below = r + 1
                
                # Check 1: Is the space below the boundary?
                if r_below >= height:
                    can_move_down = False
                    break # Obstructed by boundary

                # Check 2: Is the space below occupied by a *different* object?
                # We check against the current_grid_state. 
                # A pixel below is obstructing if it's non-white (not 0) AND 
                # it's not part of the current object itself (this handles cases 
                # where an object might have parts directly below other parts, e.g., an L-shape).
                is_part_of_self = False
                for r_obj, c_obj in coords:
                    if r_below == r_obj and c == c_obj:
                        is_part_of_self = True
                        break
                
                if current_grid_state[r_below, c] != 0 and not is_part_of_self:
                    can_move_down = False
                    break # Obstructed by another pixel

            # If after checking all pixels, it's still possible to move down
            if can_move_down:
                objects_to_move_this_step.append(obj)
                moved_in_iteration = True # Mark that movement occurred

        # --- If no objects moved in this pass, the grid is stable ---
        if not moved_in_iteration:
            break # Exit the while loop

        # --- Perform the movement: Erase all moving objects first ---
        # This prevents conflicts where one moving object would occupy the 
        # starting space of another moving object in the same step.
        for obj in objects_to_move_this_step:
             coords = obj['coords']
             for r, c in coords:
                 # Ensure we only erase pixels that currently match the object's color
                 # (Precautionary, as state shouldn't change between finding and erasing)
                 if working_grid[r, c] == obj['color']:
                      working_grid[r, c] = 0

        # --- Perform the movement: Draw all moving objects in their new positions ---
        for obj in objects_to_move_this_step:
             coords = obj['coords']
             color = obj['color']
             # Calculate new coordinates by shifting down by 1
             new_coords = coords + np.array([1, 0]) 
             for r_new, c_new in new_coords:
                 # Basic boundary check (should be safe due to can_move_down logic)
                 if 0 <= r_new < height and 0 <= c_new < width:
                     working_grid[r_new, c_new] = color
                 # else: # Optional: Log or handle unexpected out-of-bounds attempt

    # --- Convert the final NumPy array back to a list of lists ---
    output_grid = working_grid.tolist()
    
    return output_grid
```