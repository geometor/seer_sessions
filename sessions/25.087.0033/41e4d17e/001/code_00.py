import numpy as np
from collections import deque

"""
Identifies all distinct contiguous objects of Blue (1) pixels in the input grid. 
For each Blue object, it determines its bounding box and center coordinates. 
The output grid is initialized as a copy of the input. 
Then, for every pixel that was originally Azure (8) in the input:
1. If the pixel's row matches the center row of any Blue object, it becomes Magenta (6).
2. If the pixel's column matches the center column of any Blue object, it becomes Magenta (6).
3. If the pixel lies strictly inside the bounding box of any Blue object, it becomes Magenta (6).
Pixels that were originally Blue (1) remain Blue (1). All other Azure (8) pixels remain Azure (8).
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a given color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples 
              of pixels belonging to a single object.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if obj_pixels:
                    objects.append(obj_pixels)
                    
    return objects

def get_object_properties(obj_pixels):
    """
    Calculates the bounding box and center of an object.

    Args:
        obj_pixels (set): A set of (row, col) tuples representing the object.

    Returns:
        tuple: (min_row, max_row, min_col, max_col, center_row, center_col)
    """
    if not obj_pixels:
        return None

    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    # Center calculation based on bounding box
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2
    
    return min_row, max_row, min_col, max_col, center_row, center_col


def transform(input_grid):
    """
    Applies the transformation rule based on Blue objects.
    
    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Define colors
    BLUE = 1
    AZURE = 8
    MAGENTA = 6

    # Find all blue objects
    blue_objects_pixels = find_objects(input_grid, BLUE)
    
    # Get properties for each blue object
    object_properties = []
    for obj_pix in blue_objects_pixels:
        props = get_object_properties(obj_pix)
        if props:
            object_properties.append(props)

    # Iterate through each pixel of the grid to determine output color
    for r in range(rows):
        for c in range(cols):
            # Only consider changing Azure pixels
            if input_grid[r, c] == AZURE:
                should_be_magenta = False
                # Check conditions against all found blue objects
                for props in object_properties:
                    min_r, max_r, min_c, max_c, center_r, center_c = props
                    
                    # Check if on center row
                    if r == center_r:
                        should_be_magenta = True
                        break 
                        
                    # Check if on center column
                    if c == center_c:
                        should_be_magenta = True
                        break
                        
                    # Check if strictly inside bounding box (interior fill)
                    if min_r < r < max_r and min_c < c < max_c:
                        should_be_magenta = True
                        break
                        
                # Change pixel to Magenta if any condition was met
                if should_be_magenta:
                    output_grid[r, c] = MAGENTA

    return output_grid