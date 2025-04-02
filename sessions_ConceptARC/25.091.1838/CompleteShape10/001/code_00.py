import numpy as np
from collections import deque

"""
Fill internal holes within the largest non-background object with the object's color.

1. Identify the background color (most frequent color, typically white/0).
2. Find all contiguous objects of non-background colors.
3. Identify the largest object among them based on pixel count.
4. Determine the color of this largest object (the 'fill color').
5. Identify all background pixels that are 'internal' to this largest object. 
   A background pixel is internal if it cannot reach the grid boundary by moving only through other background pixels.
6. Create the output grid by copying the input grid.
7. Fill the identified internal background pixels in the output grid with the 'fill color'.
"""

def _find_objects(grid, background_color):
    """Finds all contiguous objects of non-background colors."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                obj_color = grid[r, c]
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_pixels.append((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == obj_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if current_object_pixels:
                    objects.append({
                        'color': obj_color,
                        'pixels': set(current_object_pixels), # Use set for faster lookup
                        'size': len(current_object_pixels)
                    })
                    
    return objects

def transform(input_grid):
    """
    Fills internal holes within the largest non-background object with the object's color.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid = np.copy(input_np)

    # 1. Identify background color (assume 0 based on examples, could calculate most frequent)
    background_color = 0
    # More robustly:
    # colors, counts = np.unique(input_np, return_counts=True)
    # background_color = colors[np.argmax(counts)]


    # 2. Find all non-background objects
    objects = _find_objects(input_np, background_color)

    # Handle case where there are no non-background objects
    if not objects:
        return output_grid.tolist() 

    # 3. Identify the largest object
    largest_object = max(objects, key=lambda obj: obj['size'])
    fill_color = largest_object['color']
    largest_object_pixels = largest_object['pixels']

    # 4. Identify internal background pixels using BFS from the border
    # Mark all background pixels reachable from the border as 'external'
    external_background = np.zeros_like(input_np, dtype=bool)
    q = deque()

    # Add all border background pixels to the queue
    for r in range(rows):
        for c in [0, cols - 1]: # First and last column
            if input_np[r, c] == background_color and not external_background[r, c]:
                external_background[r, c] = True
                q.append((r, c))
    for c in range(cols):
         for r in [0, rows - 1]: # First and last row
            if input_np[r, c] == background_color and not external_background[r, c]:
                external_background[r, c] = True
                q.append((r, c))

    # Perform BFS to find all reachable background pixels
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               not external_background[nr, nc] and \
               input_np[nr, nc] == background_color:
                external_background[nr, nc] = True
                q.append((nr, nc))

    # 5. Fill internal holes
    # Iterate through the grid. If a pixel is background color and NOT marked as external,
    # it's an internal hole relative to *something*. We only care about holes
    # fully enclosed by the *largest* object, but the definition of 'internal' 
    # (cannot reach border via background) effectively captures this for this problem type.
    # A background pixel not reachable from the border must be enclosed. Given the problem
    # structure (one main object with holes), these enclosed pixels must be within that main object.
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] == background_color and not external_background[r, c]:
                # This pixel is an internal background pixel. Fill it with the largest object's color.
                output_grid[r, c] = fill_color

    return output_grid.tolist()