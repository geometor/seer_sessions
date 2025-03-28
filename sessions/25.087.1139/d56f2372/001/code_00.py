import numpy as np
from collections import deque

"""
Identifies the object in the input grid that contains internal holes 
(white pixels completely surrounded by the object's pixels) and extracts 
this object into the output grid, cropped to its minimal bounding box.
Assumes exactly one such object exists.
"""

# Helper function to find connected components (objects) based on color
def find_objects(grid):
    """
    Finds all contiguous objects of non-white colors in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'coords' (set of (row, col) tuples).
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            # If pixel is non-white (not 0) and not visited yet, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    coords.add((row, col))
                    
                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds, color match, and visited status
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found object
                objects.append({'color': color, 'coords': coords})
                
    return objects

# Helper function to calculate the bounding box of a set of coordinates
def get_bounding_box(coords):
    """
    Calculates the minimum and maximum row and column indices for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if coords is empty.
    """
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return min_r, min_c, max_r, max_c

# Helper function to check if an object contains internal holes
def has_holes(grid, obj_coords):
    """
    Checks if an object encloses any white pixels (value 0).
    It works by flood-filling the background (white pixels) starting from the grid borders.
    Any white pixel not reached by this fill is considered enclosed.
    It then checks if any of these enclosed white pixels are adjacent to the object.

    Args:
        grid (np.array): The input grid.
        obj_coords (set): The coordinates {(row, col), ...} of the object being checked.

    Returns:
        bool: True if the object encloses at least one white pixel, False otherwise.
    """
    height, width = grid.shape
    
    # 1. Perform flood fill (BFS) from background (white pixels on the border)
    # visited_background tracks white pixels reachable from the outside.
    visited_background = np.zeros_like(grid, dtype=bool)
    q = deque()
    
    # Initialize queue with all white border pixels
    for r in range(height):
        if grid[r, 0] == 0 and not visited_background[r, 0]:
            visited_background[r, 0] = True
            q.append((r, 0))
        if grid[r, width - 1] == 0 and not visited_background[r, width - 1]:
             visited_background[r, width - 1] = True
             q.append((r, width - 1))
    for c in range(1, width - 1): # Avoid checking corners twice
        if grid[0, c] == 0 and not visited_background[0, c]:
            visited_background[0, c] = True
            q.append((0, c))
        if grid[height - 1, c] == 0 and not visited_background[height - 1, c]:
             visited_background[height - 1, c] = True
             q.append((height - 1, c))

    # BFS traversal for background white pixels
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if it's white, and if not already visited
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and not visited_background[nr, nc]:
                visited_background[nr, nc] = True
                q.append((nr, nc))

    # 2. Find enclosed white pixels (white pixels not visited by the background fill)
    enclosed_white_coords = set()
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 0 and not visited_background[r, c]:
                enclosed_white_coords.add((r,c))

    if not enclosed_white_coords:
        return False # No enclosed white pixels anywhere in the grid

    # 3. Check if any of these enclosed white pixels are adjacent to *this* object
    for r_enclosed, c_enclosed in enclosed_white_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_enclosed + dr, c_enclosed + dc
            # Check if the neighbor coordinate belongs to the object
            if (nr, nc) in obj_coords: 
                 # Found an enclosed white pixel adjacent to this object
                 return True 

    # If no enclosed white pixel was found adjacent to this object's coordinates
    return False


def transform(input_grid_list):
    """
    Identifies the object in the input grid that contains internal holes 
    (white pixels completely surrounded by the object's pixels) and extracts 
    this object into the output grid, cropped to its minimal bounding box.
    Assumes exactly one such object exists based on training examples.

    Args:
        input_grid_list (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the extracted object within its bounding box, 
              or an empty list if no suitable object is found (unexpected case).
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)
    
    # Step 1: Find all distinct colored objects in the grid
    objects = find_objects(input_grid)
    
    # Step 2: Identify the object that has internal holes
    target_object = None
    for obj in objects:
        # Check if the object encloses any white pixels using the helper function
        if has_holes(input_grid, obj['coords']):
            target_object = obj
            # Assumption: Only one object will satisfy the condition per the examples
            break 
            
    # Step 3: Handle the case where no target object is found (error or unexpected input)
    if target_object is None:
        print("Warning: No object with holes found. Returning empty grid.")
        return [] 

    # Step 4: Determine the bounding box of the identified target object
    bounding_box = get_bounding_box(target_object['coords'])
    if bounding_box is None: # Should not happen if target_object is not None
         print("Warning: Found object but failed to get bounding box. Returning empty grid.")
         return []
    min_r, min_c, max_r, max_c = bounding_box
    
    # Step 5: Extract the subgrid corresponding to the bounding box from the input grid
    # NumPy slicing is [start_row:end_row+1, start_col:end_col+1]
    output_grid_np = input_grid[min_r:max_r+1, min_c:max_c+1]
    
    # Step 6: Convert the resulting NumPy array back to a list of lists for the output
    output_grid = output_grid_np.tolist()
    
    return output_grid
