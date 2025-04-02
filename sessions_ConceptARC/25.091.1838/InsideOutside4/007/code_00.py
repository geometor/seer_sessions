import numpy as np
from collections import deque

"""
Conditionally changes a single unique magenta pixel (color 6) to white (color 0)
based on the colors of the two closest enclosing objects found by exploring outwards 
through adjacent background pixels using Breadth-First Search (BFS).

Transformation Steps:
1. Locate the unique magenta pixel (P). Exit if not found or not unique.
2. Find the first non-background, non-magenta color (C_inner) encountered by BFS starting 
   from a background neighbor of P, exploring only background. Exit if none found.
3. Find the first non-background color (C_outer) encountered by BFS starting from a 
   background neighbor of any C_inner pixel, exploring only background. C_outer must not be C_inner or magenta. Exit if none found.
4. Check if (C_inner=4 (yellow), C_outer=2 (red)) or (C_inner=1 (blue), C_outer=3 (green)).
5. If the condition holds, change pixel P to white (0) in a copy of the grid. Otherwise, make no change.
6. Return the resulting grid as a list of lists.
"""

def find_pixels(grid, color):
    """Finds all coordinates (row, col) of pixels with a specific color."""
    # Ensure grid is numpy array for efficient searching
    if not isinstance(grid, np.ndarray):
        grid_np = np.array(grid, dtype=int)
    else:
        grid_np = grid
    # Use np.argwhere to find coordinates
    return list(map(tuple, np.argwhere(grid_np == color)))

def find_adjacent_pixel(grid, start_coords, target_color):
    """
    Finds the coordinates of the first pixel with target_color adjacent 
    (4-connectivity) to any of the start_coords. Returns None if not found.
    Assumes grid is a numpy array.
    """
    rows, cols = grid.shape
    initial_coords_set = set(start_coords)
    
    for r, c in start_coords:
         # Check 4 neighbors
         for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_pos = (nr, nc)
                # Check if neighbor has the target color and is not part of the starting set
                if grid[nr, nc] == target_color and neighbor_pos not in initial_coords_set:
                    return neighbor_pos # Found one
    return None # Not found

def find_first_enclosing_color(grid, start_pos, excluded_colors):
    """
    Performs BFS starting from start_pos (must be background) traversing only background (0).
    Returns the color (as standard Python int) of the first non-background neighbor 
    encountered whose color is NOT in excluded_colors.
    Returns None if the BFS completes without finding such a neighbor or if start_pos is invalid.
    Assumes grid is a numpy array.
    """
    rows, cols = grid.shape
    
    # Validate start_pos: must be within bounds and background color (0)
    if start_pos is None or not (0 <= start_pos[0] < rows and 0 <= start_pos[1] < cols and grid[start_pos] == 0):
         return None # Invalid start

    q = deque([start_pos])
    visited_background = {start_pos}
    
    # Ensure excluded colors are standard Python ints
    excluded_colors_int = {int(ex) for ex in excluded_colors}

    while q:
        r, c = q.popleft()

        # Check neighbors (4-connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue # Skip out-of-bounds

            neighbor_pos = (nr, nc)
            neighbor_color = grid[nr, nc]

            # If neighbor is background (0) and not visited, add to queue
            if neighbor_color == 0:
                if neighbor_pos not in visited_background:
                    visited_background.add(neighbor_pos)
                    q.append(neighbor_pos)
            # If neighbor is non-background
            else:
                # Convert color to standard int for checks and return
                neighbor_color_int = int(neighbor_color) 
                # Check if its color is one we are looking for (not excluded)
                if neighbor_color_int not in excluded_colors_int:
                    return neighbor_color_int # Found the first valid enclosing color

    # If queue empties and we haven't returned, no valid enclosing color was found
    return None


def transform(input_grid_list):
    """
    Applies the conditional color change based on the nested object color logic.
    
    Args:
        input_grid_list: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)
    # Create a copy to modify, ensuring the original is unchanged if conditions aren't met
    output_grid = np.copy(input_grid) 

    # --- Step 1: Locate Target ---
    # Find all magenta pixels (color 6)
    magenta_pixels = find_pixels(output_grid, 6)
    # Check if exactly one magenta pixel exists
    if len(magenta_pixels) != 1:
        # Return the original grid if not exactly one magenta pixel
        return input_grid_list 
    target_pos = magenta_pixels[0]

    # --- Step 2: Find Inner Color (C_inner) ---
    # Find a background pixel (color 0) adjacent to the target magenta pixel
    start_pos_inner = find_adjacent_pixel(output_grid, [target_pos], 0)
    if start_pos_inner is None:
        # If no adjacent background pixel, cannot perform search, return original
        return input_grid_list
        
    # Search outwards from the adjacent background pixel using BFS
    # Find the first non-background, non-magenta color encountered.
    # Exclude background (0) and magenta (6) from being considered the inner color.
    C_inner = find_first_enclosing_color(output_grid, start_pos_inner, {0, 6})
    if C_inner is None:
        # If BFS doesn't find a suitable inner enclosing color, return original
        return input_grid_list

    # --- Step 3: Find Outer Color (C_outer) ---
    # Find all pixels belonging to the inner object (color C_inner)
    c_inner_pixels = find_pixels(output_grid, C_inner)
    if not c_inner_pixels:
         # Safety check: if no pixels found for C_inner (shouldn't happen), return original
         return input_grid_list
         
    # Find a background pixel adjacent to any of the inner object's pixels
    start_pos_outer = find_adjacent_pixel(output_grid, c_inner_pixels, 0)
    if start_pos_outer is None:
        # If the C_inner object has no adjacent background pixels, it cannot be enclosed by another
        # object via background space, so return original.
        return input_grid_list

    # Search outwards from this new background starting point using BFS.
    # Exclude background (0), magenta (6), and the inner color (C_inner) itself.
    C_outer = find_first_enclosing_color(output_grid, start_pos_outer, {0, 6, C_inner})
    if C_outer is None:
        # If BFS doesn't find a suitable outer enclosing color, return original
        return input_grid_list

    # --- Step 4: Evaluate Condition ---
    condition_met = False
    # Check for the specific required pairs of inner and outer colors
    # Condition 1: Yellow (4) inside Red (2)
    if C_inner == 4 and C_outer == 2:
        condition_met = True
    # Condition 2: Blue (1) inside Green (3)
    elif C_inner == 1 and C_outer == 3:
        condition_met = True

    # --- Step 5: Apply Transformation or Return Original ---
    if condition_met:
        # If the condition is met, modify the output grid copy
        r_target, c_target = target_pos
        # Change the target magenta pixel to white (0)
        output_grid[r_target, c_target] = 0
        # Return the modified grid as a list of lists
        return output_grid.tolist() 
    else:
        # If condition is not met, return the original unchanged input grid
        return input_grid_list