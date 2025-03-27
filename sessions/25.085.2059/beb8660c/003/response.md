```python
import numpy as np
from collections import deque

"""
Simulates gravity on non-white (0), non-azure (8) objects in a grid.
Objects are defined as contiguous blocks (adjacent, not diagonal) of the same 
color, excluding white and azure. These mobile objects fall downwards as 
whole units through white space (color 0). An object stops falling when any 
part of it is directly above a non-white pixel (either another mobile object, 
a static azure pixel, or the grid's bottom boundary). The simulation runs 
iteratively, allowing objects to fall one step at a time in each pass, until 
a full pass completes with no objects moving, indicating a stable state. Azure 
pixels (color 8) are static and act as obstacles/ground.
"""

def _find_objects(grid, background_color, static_colors):
    """
    Identifies all distinct mobile objects in the grid.

    Args:
        grid: The numpy array representing the grid state.
        background_color: The integer value representing empty space.
        static_colors: A set of integer values representing static colors.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its 'color' (int) and 'pixels' (a set of (row, col) tuples).
    """
    height, width = grid.shape
    visited = set()
    objects = []
    # Define which colors are considered mobile
    mobile_colors = set(range(10)) - {background_color} - static_colors

    # Iterate through each cell to find starting points of new objects
    for r in range(height):
        for c in range(width):
            # If the cell has a mobile color and hasn't been visited yet
            if grid[r, c] in mobile_colors and (r, c) not in visited:
                color = grid[r, c]
                obj_pixels = set()
                # Use BFS (Breadth-First Search) to find all connected pixels of the same color
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check 4 adjacent neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check if neighbor is within bounds, has the same color, and hasn't been visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                # Add the found object to the list if it contains any pixels
                if obj_pixels:
                    objects.append({'color': color, 'pixels': obj_pixels})
    return objects


def transform(input_grid):
    """
    Applies object-based gravity simulation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid after simulation.
    """
    # Convert input to NumPy array for efficient manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    # Create a copy to modify, representing the evolving grid state
    output_grid = input_np.copy() 
    
    background_color = 0
    static_colors = {8} # Azure (8) is static

    # --- Identify initial mobile objects ---
    # These objects will be tracked and moved throughout the simulation.
    mobile_objects = _find_objects(output_grid, background_color, static_colors)

    # --- Simulation Loop ---
    # Continue iterating until no objects move in a full pass.
    while True:
        moved_in_pass = False # Flag to track movement within a single pass
        
        # Sort objects by their lowest point (max row index) in descending order.
        # This ensures that objects lower down are processed first in each pass.
        mobile_objects.sort(key=lambda obj: max(r for r, c in obj['pixels']), reverse=True)

        # Iterate through each mobile object and attempt to move it down
        for i in range(len(mobile_objects)):
            obj = mobile_objects[i]
            
            # --- Check if the object can move down one step ---
            can_move = True
            # Calculate the set of coordinates the object would occupy if moved down
            potential_new_pixels = set((r + 1, c) for r, c in obj['pixels'])
            
            # Check for boundary collisions and obstacles below
            for nr, nc in potential_new_pixels:
                # 1. Check if any part hits the bottom boundary
                if nr >= height:
                    can_move = False
                    break
                # 2. Check if the potential new cell (nr, nc) is occupied by something static
                #    or another object *that is not the object currently being moved*.
                #    The `(nr, nc) not in obj['pixels']` condition is crucial. It ensures
                #    that an object can move into a space that it currently occupies (e.g., the bottom
                #    part moving into the space previously occupied by the top part).
                #    We check the *current* state of output_grid, which reflects moves made
                #    by lower objects earlier in this same pass.
                if (nr, nc) not in obj['pixels'] and output_grid[nr, nc] != background_color:
                    can_move = False
                    break
            
            # --- If movement is possible, update the grid and object state ---
            if can_move:
                moved_in_pass = True # Mark that movement occurred in this pass
                obj_color = obj['color']
                
                # 1. Erase the object from its old position in the output grid
                #    It's important to copy the old pixels before updating the object's state.
                old_pixels = obj['pixels'].copy() 
                for r, c in old_pixels:
                    output_grid[r, c] = background_color
                
                # 2. Update the object's internal state (its pixel coordinates)
                obj['pixels'] = potential_new_pixels 

                # 3. Draw the object in its new position in the output grid
                for nr, nc in obj['pixels']:
                    output_grid[nr, nc] = obj_color
                
                # The grid (output_grid) is now updated, reflecting this object's move.
                # Subsequent objects checked in this pass will see this new state.

        # --- Check for Simulation End ---
        # If no object moved during this entire pass, the grid has stabilized.
        if not moved_in_pass:
            break # Exit the while loop

    # Convert the final NumPy array back to a standard list of lists format
    return output_grid.tolist()
```