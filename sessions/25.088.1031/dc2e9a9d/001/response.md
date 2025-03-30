```python
import numpy as np
from collections import deque

# Define colors based on the problem description (mapping integers to names for clarity)
# COLOR_MAP = {0: 'white', 1: 'blue', 2: 'red', 3: 'green', 4: 'yellow', 5: 'gray', 6: 'magenta', 7: 'orange', 8: 'azure', 9: 'maroon'}
WHITE = 0
BLUE = 1
GREEN = 3
AZURE = 8

def find_objects(grid, color):
    """
    Finds all distinct connected objects of a given color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[list[tuple[int, int]]]: A list of objects, where each object
                                      is a list of its coordinate tuples (row, col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start BFS to find a new object
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_coords.append((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if obj_coords:
                    objects.append(obj_coords)
                    
    return objects

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box of an object.

    Args:
        obj_coords (list[tuple[int, int]]): List of coordinates for the object.

    Returns:
        tuple[int, int, int, int]: (min_row, min_col, max_row, max_col)
    """
    if not obj_coords:
        return None # Or raise an error
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    return min(rows), min(cols), max(rows), max(cols)

def is_bottom_heavy(obj_coords, bbox):
    """Checks if the object touches the bottom edge but not the top edge of its bounding box."""
    min_r, _, max_r, _ = bbox
    touches_bottom = any(r == max_r for r, c in obj_coords)
    touches_top = any(r == min_r for r, c in obj_coords)
    return touches_bottom and not touches_top

def has_hole(grid, obj_coords, bbox):
    """Checks if the object encloses any background (white) pixels."""
    min_r, min_c, max_r, max_c = bbox
    rows, cols = grid.shape
    
    # Quick check: if bbox is too small to have an interior, no hole
    if max_r - min_r < 2 or max_c - min_c < 2:
        return False

    obj_set = set(obj_coords)
    visited = set()
    q = deque()

    # Start BFS from all background pixels on the bounding box border
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if r == min_r or r == max_r or c == min_c or c == max_c:
                 # Consider only background pixels within the actual grid bounds
                if 0 <= r < rows and 0 <= c < cols and grid[r, c] == WHITE:
                    if (r,c) not in visited:
                        q.append((r, c))
                        visited.add((r, c))
                # Also consider pixels just outside the bounding box as starting points for the "outside" region
                # Check direct neighbors of bbox border pixels
                for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == WHITE:
                         if (nr, nc) not in visited:
                             q.append((nr, nc))
                             visited.add((nr, nc))


    # Also start BFS from the grid edges if they are close to the bbox
    # This ensures we capture the full 'outside' region connectivity
    for r in range(rows):
        if grid[r, 0] == WHITE and (r, 0) not in visited: q.append((r, 0)); visited.add((r,0))
        if grid[r, cols-1] == WHITE and (r, cols-1) not in visited: q.append((r, cols-1)); visited.add((r, cols-1))
    for c in range(cols):
        if grid[0, c] == WHITE and (0, c) not in visited: q.append((0, c)); visited.add((0,c))
        if grid[rows-1, c] == WHITE and (rows-1, c) not in visited: q.append((rows-1, c)); visited.add((rows-1, c))


    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check neighbor validity (within grid, is background, not object, not visited)
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == WHITE and \
               (nr, nc) not in obj_set and \
               (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc))

    # Check for any background pixel inside the bounding box that wasn't visited
    # These are pixels disconnected from the outside -> hole
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            if grid[r, c] == WHITE and (r, c) not in visited and (r,c) not in obj_set:
                return True
                
    return False


def has_stem(obj_coords, bbox):
    """Checks if the object touches the bottom edge of its bounding box with 1 or 2 pixels."""
    _, _, max_r, _ = bbox
    bottom_pixels = [ (r,c) for r,c in obj_coords if r == max_r ]
    count = len(bottom_pixels)
    return count == 1 or count == 2


def transform(input_grid):
    """
    Identifies green objects in the input grid, analyzes their shape properties 
    (bottom-heavy, has hole, has stem), and creates a copy of each object. 
    The copy's color (blue or azure) and position (below or right of the original) 
    are determined by these properties.

    1. Initialize the output grid as a copy of the input grid.
    2. Find all distinct green objects.
    3. For each green object:
        a. Calculate its bounding box.
        b. Check if it's bottom-heavy (touches bottom bbox edge but not top).
        c. Check if it has an internal hole (enclosed white pixels).
        d. Check if it has a stem (1 or 2 pixels touching bottom bbox edge).
        e. Determine copy position: Below if bottom-heavy, Right otherwise (with 1px gap).
        f. Determine copy color:
            - Right -> Blue
            - Below: Blue if (has_hole and has_stem), Azure otherwise.
        g. Draw the copy onto the output grid.
    4. Return the modified output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Find all green objects
    green_objects = find_objects(input_grid, GREEN)

    # Process each object
    for obj_coords in green_objects:
        # Calculate properties
        bbox = get_bounding_box(obj_coords)
        min_r, min_c, max_r, max_c = bbox
        
        bottom_heavy = is_bottom_heavy(obj_coords, bbox)
        # Note: Use input_grid for has_hole check as output_grid might be modified
        hole = has_hole(input_grid, obj_coords, bbox) 
        stem = has_stem(obj_coords, bbox)

        # Determine copy placement and color
        copy_color = -1 # Initialize with invalid color
        offset_r, offset_c = 0, 0 # Offset from original top-left to copy top-left

        if bottom_heavy:
            # Place Below
            offset_r = (max_r - min_r) + 2 # Start row is max_r + 2, relative to min_r
            offset_c = 0                  # Start col is min_c, relative to min_c
            if hole and stem:
                copy_color = BLUE
            else:
                copy_color = AZURE
        else:
            # Place Right
            offset_r = 0                  # Start row is min_r, relative to min_r
            offset_c = (max_c - min_c) + 2 # Start col is max_c + 2, relative to min_c
            copy_color = BLUE
            
        # Create the copy if color is valid
        if copy_color != -1:
            for r, c in obj_coords:
                # Calculate relative position within the object's bounding box
                rel_r = r - min_r
                rel_c = c - min_c
                
                # Calculate target position in the output grid
                target_r = min_r + offset_r + rel_r
                target_c = min_c + offset_c + rel_c
                
                # Draw the pixel if within grid bounds
                if 0 <= target_r < rows and 0 <= target_c < cols:
                    # Important: Check if target location is currently background (white)
                    # This prevents overwriting parts of other original objects if copies overlap originals slightly
                    # Based on examples, copies don't seem to overwrite originals, but might overwrite background
                    # Let's assume copies can overwrite background but not existing colored pixels from originals.
                    # Example 1 output shows the '8' copy starting near the original 'T'.
                    # Example 3 output shows '1' copy near original 'G'.
                    # Example 2 output shows '1' near 'C' and '8' near 'G'.
                    # It seems safe to draw the copy regardless of what's there, as long as it's within bounds.
                    # The problem doesn't specify behavior for overlapping copies - assume last one drawn wins.
                    output_grid[target_r, target_c] = copy_color

    return output_grid
```