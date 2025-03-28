import numpy as np
from scipy.ndimage import label

"""
Simulates gravity acting on connected objects of the same color in a grid.
Non-white objects (contiguous blocks of the same color) fall downwards 
into white space (pixels with value 0). An object stops falling when any 
part of its bottom edge encounters a non-white pixel below it or reaches 
the grid's bottom boundary. The process iterates, allowing objects to fall 
sequentially until no object can move further, reaching a stable state. 
Objects maintain their shape throughout the process.
"""

def transform(input_grid):
    """
    Applies object-based gravity to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the grid after gravity simulation.
    """
    working_grid = np.array(input_grid, dtype=int)
    height, width = working_grid.shape

    while True:
        moved_in_iteration = False
        
        # Identify all current non-white objects based on the grid state at the start of this iteration
        current_objects = []
        # Use scipy.ndimage.label to find all connected components for each non-white color
        unique_colors = np.unique(working_grid[working_grid != 0])
        
        object_pixels_this_iteration = [] # Store list of coords for each object found

        for color in unique_colors:
            mask = (working_grid == color)
            # label assigns a unique integer to each connected component
            labeled_array, num_labels = label(mask) 
            
            # For each component found for this color
            for i in range(1, num_labels + 1):
                # Get all coordinates [(r1, c1), (r2, c2), ...] for this specific object
                coords = np.argwhere(labeled_array == i)
                object_pixels_this_iteration.append({'color': color, 'coords': coords})

        # Sort objects by their highest point (minimum row index) to process top objects first.
        # This helps ensure that objects fall in a more predictable order, though the iteration loop handles stabilization regardless.
        object_pixels_this_iteration.sort(key=lambda obj: np.min(obj['coords'][:, 0]))
        
        # Create a copy of the grid state at the beginning of this iteration
        # This is crucial for checking collisions, ensuring objects "decide" to fall based on the same snapshot
        grid_before_moves = working_grid.copy()

        # Attempt to move each identified object based on the grid_before_moves state
        for obj in object_pixels_this_iteration:
            color = obj['color']
            coords = obj['coords'] # Original coordinates of the object in grid_before_moves

            # --- Calculate the maximum distance this object can fall ---
            max_fall_dist = height # Initialize with a large value (max possible fall)
            possible_to_fall = True # Assume it can fall initially

            # Create a temporary grid representing the state *without* the current object
            # Used to check for collisions below the object's current position
            temp_grid_without_obj = grid_before_moves.copy()
            for r_obj, c_obj in coords:
                 temp_grid_without_obj[r_obj, c_obj] = 0

            # Check how far each pixel of the object *could* fall vertically before hitting something or the boundary
            for r_orig, c_orig in coords:
                dist_this_pixel = 0
                # Look downwards from the pixel's original position + 1
                for r_check in range(r_orig + 1, height):
                    # Check for collision in the grid *without* the object itself
                    if temp_grid_without_obj[r_check, c_orig] != 0:
                        # Collision detected below this specific pixel
                        break # Stop checking downwards for this pixel
                    dist_this_pixel += 1
                else: 
                    # Loop finished without break means no collision below this pixel until boundary
                    # dist_this_pixel is now the distance from r_orig+1 to the boundary
                    pass 
                
                # The maximum distance the *entire object* can fall is limited by the 
                # *minimum* distance any single one of its constituent pixels can fall.
                max_fall_dist = min(max_fall_dist, dist_this_pixel)

                # Optimization: If any pixel cannot fall at all (hits something immediately below),
                # then the entire object cannot fall.
                if max_fall_dist == 0:
                    possible_to_fall = False
                    break # No need to check other pixels for this object

            # --- Move the object if it can fall ---
            if possible_to_fall and max_fall_dist > 0:
                # Erase the object from its *current* position in the *actual working grid*
                # Do this *before* drawing the object in its new position to handle 1-step falls correctly.
                for r_erase, c_erase in coords:
                    # Double-check: only erase if the pixel in the working_grid still belongs to this object
                    # This handles cases where another object might have landed here earlier *in the same iteration*.
                     if working_grid[r_erase, c_erase] == color:
                          working_grid[r_erase, c_erase] = 0
                
                # Draw the object in its new, fallen position in the *actual working grid*
                new_coords = coords + np.array([max_fall_dist, 0])
                for r_new, c_new in new_coords:
                    # Basic boundary check (should theoretically not be needed if logic is perfect)
                    if 0 <= r_new < height and 0 <= c_new < width:
                         working_grid[r_new, c_new] = color
                    # else: Optional: Add warning for out-of-bounds draw attempt

                # Mark that at least one object moved in this iteration
                moved_in_iteration = True
                # We continue checking the rest of the objects based on the grid_before_moves state.
                # The effects of this move will be considered in the *next* iteration of the while loop.

        # After checking/moving all objects identified at the start of the iteration,
        # if no object moved at all, the grid has reached a stable state.
        if not moved_in_iteration:
            break # Exit the while loop

    # Convert the final NumPy array back to a list of lists
    output_grid = working_grid.tolist()
    
    return output_grid