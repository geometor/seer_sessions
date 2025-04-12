```python
import collections
import numpy as np

"""
Identifies all distinct, connected objects within the input grid that have one of the 
candidate colors: red (2), orange (7), or gray (5). For each candidate object, 
determines the row index of its top-most pixel (min_r). Selects the single candidate 
object that possesses the largest min_r value (i.e., the one starting lowest 
vertically). Records the color (target_color) and the top-left coordinates 
(bbox_top_row, bbox_left_col) of the minimum bounding box for this target object. 
Creates a new 3x3 grid initialized to white (0). Iterates through each cell 
(r_out, c_out) of the 3x3 output grid. Calculates the corresponding coordinates 
(r_in, c_in) in the input grid. If (r_in, c_in) is within the input grid bounds AND 
the color at input_grid[r_in][c_in] matches the target_color, sets the output cell 
output_grid[r_out][c_out] to target_color. Otherwise, the cell remains white (0). 
Returns the final 3x3 output grid.
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

    # Step 1: Identify all distinct candidate objects (colors 2, 7, or 5).
    for r in range(height):
        for c in range(width):
            # Check if pixel is non-background and hasn't been visited
            if grid[r, c] != 0 and (r, c) not in visited_global:
                color = grid[r, c]
                # Find all connected pixels for this object using BFS
                pixels = find_connected_pixels(grid, r, c, color, visited_global)
                
                # Step 2: For each candidate object, determine the top-most row index (min_r).
                if color in target_colors:
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

    # Step 3: Select the target object: the one with the maximum minimum row index.
    target_object = max(candidate_objects, key=lambda obj: obj['min_r'])
    
    # Step 4: Record target color and top-left coordinates of its bounding box.
    final_target_color = target_object['color']
    bbox_top_row = target_object['min_r']
    bbox_left_col = target_object['min_c']

    # Step 5: Create a new 3x3 grid, initializing all cells to white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Step 6-10: Iterate through the 3x3 output grid cells.
    for r_out in range(3): # Iterate through output rows (0 to 2)
        for c_out in range(3): # Iterate through output columns (0 to 2)
            # Step 7: Calculate corresponding input grid coordinates.
            r_in = bbox_top_row + r_out
            c_in = bbox_left_col + c_out

            # Step 8 & 9: Check if input coords are valid and pixel has the target color.
            if 0 <= r_in < height and 0 <= c_in < width and \
               grid[r_in, c_in] == final_target_color:
                # Step 10: If yes, copy the target color to the output grid.
                output_grid[r_out, c_out] = final_target_color
            # Else (conditions false): Leave the output cell as white (0).

    # Step 11: Return the final 3x3 output grid as a list of lists.
    return output_grid.tolist()
```