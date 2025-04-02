import numpy as np
from collections import deque

"""
Identify all distinct objects (contiguous areas of the same non-white color) in the input grid.
Determine which objects are 'internal', meaning they are not reachable from the outer boundary of the grid by traversing only white (0) pixels.
Create an output grid of the same dimensions as the input, initialized to white (0).
Copy only the 'internal' objects to the output grid, preserving their original colors and positions.
"""

def find_objects(grid):
    """
    Finds all connected components of non-white pixels in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'pixels' (a set of (row, col) tuples) and 'color'.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check 4 neighbors (horizontal/vertical)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({'pixels': obj_pixels, 'color': color})
                
    return objects

def flood_fill_outside(grid):
    """
    Performs a flood fill starting from white pixels on the border
    to find all white pixels reachable from the outside.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        set: A set of (row, col) tuples representing reachable white pixels.
    """
    height, width = grid.shape
    reachable_white = set()
    q = deque()

    # Add border white pixels to the queue and set
    for r in range(height):
        if grid[r, 0] == 0:
            if (r, 0) not in reachable_white:
                reachable_white.add((r, 0))
                q.append((r, 0))
        if grid[r, width - 1] == 0:
             if (r, width - 1) not in reachable_white:
                reachable_white.add((r, width - 1))
                q.append((r, width - 1))
                
    for c in range(width):
        if grid[0, c] == 0:
            if (0, c) not in reachable_white:
                reachable_white.add((0, c))
                q.append((0, c))
        if grid[height - 1, c] == 0:
            if (height - 1, c) not in reachable_white:
                reachable_white.add((height - 1, c))
                q.append((height - 1, c))

    # Perform BFS for reachable white pixels
    while q:
        r, c = q.popleft()
        
        # Check 8 neighbors (including diagonals) - important for finding adjacency later
        # Actually, only 4 neighbours needed for flood fill itself
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and (nr, nc) not in reachable_white:
                reachable_white.add((nr, nc))
                q.append((nr, nc))
                
    return reachable_white


def transform(input_grid):
    """
    Transforms the input grid by keeping only objects that are fully enclosed
    (not reachable from the outside via white pixels).

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    
    # Initialize output_grid with white (0)
    output_grid = np.zeros_like(input_grid)

    # Find all distinct non-white objects
    objects = find_objects(input_grid)
    
    # Find all white pixels reachable from the outside border
    reachable_white = flood_fill_outside(input_grid)
    
    # Identify internal objects and draw them on the output grid
    for obj in objects:
        is_internal = True
        # Check if any pixel of the object is adjacent (8 directions) to a reachable white pixel
        for r, c in obj['pixels']:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    # Check if neighbor is within bounds and is a reachable white pixel
                    if 0 <= nr < height and 0 <= nc < width:
                         if (nr, nc) in reachable_white:
                            is_internal = False
                            break # No need to check other neighbours for this pixel
                if not is_internal:
                    break # No need to check other pixels for this object
            if not is_internal:
                break # Exit outer loop as well

        # If the object is internal, copy its pixels to the output grid
        if is_internal:
            for r, c in obj['pixels']:
                output_grid[r, c] = obj['color']

    return output_grid.tolist()