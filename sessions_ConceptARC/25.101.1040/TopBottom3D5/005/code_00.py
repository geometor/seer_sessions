import collections
import numpy as np

"""
Identifies all distinct connected objects in the input grid that have one of the 
candidate colors: red (2), orange (7), or gray (5). Among these candidates, 
selects the one whose bounding box starts at the lowest row index (maximum minimum row). 
Determines the top-left 3x3 area relative to the selected target object's bounding box. 
Creates a 3x3 output grid. For each cell in the output grid, if the corresponding 
cell in the input grid (relative to the target bounding box's top-left) exists 
and belongs to the target object (has the target color), copy the target color. 
Otherwise, the output cell is white (0).
"""

def find_connected_pixels(grid, start_r, start_c, target_color, visited_global):
    """
    Finds all connected pixels of a target color using BFS, respecting globally visited pixels.
    Uses 4-way connectivity.
    Returns the set of pixel coordinates (row, col) belonging to the object.
    """
    height, width = grid.shape
    q = collections.deque([(start_r, start_c)])
    visited_local = set([(start_r, start_c)]) # Track visited within this specific BFS call
    pixels = set([(start_r, start_c)])
    visited_global.add((start_r, start_c)) # Mark globally visited

    while q:
        r, c = q.popleft()

        # Explore neighbors (4-way connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds, color match, and if visited locally in this BFS run
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == target_color and (nr, nc) not in visited_local:

                # We only start BFS from unvisited pixels, so checking visited_global here
                # is redundant but harmless. The primary check is visited_local.
                visited_local.add((nr, nc))
                pixels.add((nr, nc))
                visited_global.add((nr, nc)) # Mark globally visited
                q.append((nr, nc))
                
    return pixels

def get_bounding_box(pixels):
    """
    Calculates the bounding box (min_r, min_c, max_r, max_c) for a set of pixel coordinates.
    Returns (-1, -1, -1, -1) if the set is empty.
    """
    if not pixels:
        return -1, -1, -1, -1 # Indicate no bounding box
    
    # Find min/max row and column from the pixel coordinates
    min_r = min(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_r = max(r for r, c in pixels)
    max_c = max(c for r, c in pixels)
    
    return min_r, min_c, max_r, max_c

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Convert input list of lists to numpy array for easier indexing
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    target_colors = {2, 7, 5} # Candidate colors: red, orange, gray
    
    candidate_objects = []
    visited_global = set() # Keep track of pixels already assigned to an object across the grid

    # Step 1: Scan the input grid to find all distinct candidate objects.
    for r in range(height):
        for c in range(width):
            # Check if pixel is non-background and hasn't been visited
            if grid[r, c] != 0 and (r, c) not in visited_global:
                color = grid[r, c]
                # Find all connected pixels for this object using BFS
                pixels = find_connected_pixels(grid, r, c, color, visited_global)
                
                # Step 2: Check if the object's color is one of the target colors.
                if color in target_colors:
                    # Step 3: Determine the bounding box and record the top-most row (min_r).
                    min_r, min_c, _, _ = get_bounding_box(pixels)
                    # Store relevant info if a valid bounding box was found
                    if min_r != -1: 
                        candidate_objects.append({
                            "color": color,
                            "min_r": min_r,
                            "min_c": min_c,
                        })

    # Handle case where no candidate objects are found
    if not candidate_objects:
        # Return a default 3x3 white grid
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]] 

    # Step 4: Select the target object: the one with the maximum minimum row index (lowest starting point).
    target_object = max(candidate_objects, key=lambda obj: obj['min_r'])
    
    final_target_color = target_object['color']
    bbox_top_row = target_object['min_r']
    bbox_left_col = target_object['min_c']

    # Step 5: Create the 3x3 output grid, initialized to white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Step 6-9: Populate the output grid based on the target object's top-left 3x3 area.
    for r_out in range(3): # Iterate through output rows (0 to 2)
        for c_out in range(3): # Iterate through output columns (0 to 2)
            # Calculate corresponding coordinates in the input grid
            r_in = bbox_top_row + r_out
            c_in = bbox_left_col + c_out

            # Check if the input coordinates are valid (within bounds) 
            # AND if the pixel at that coordinate has the target color.
            if 0 <= r_in < height and 0 <= c_in < width and \
               grid[r_in, c_in] == final_target_color:
                # If yes, copy the target color to the output grid.
                output_grid[r_out, c_out] = final_target_color
            # Else: leave the output cell as 0 (white), as initialized.

    # Step 10: Convert the NumPy output grid back to a list of lists and return.
    return output_grid.tolist()