"""
Identifies all distinct contiguous objects of Blue (1) pixels in the input grid. 
For each Blue object, it determines its bounding box and calculates its center coordinates 
(center_row = (min_row + max_row) // 2, center_col = (min_col + max_col) // 2). 
The output grid is initialized as a copy of the input. 
Then, for every pixel that was originally Azure (8) in the input:
1. If the pixel's row matches the center_row of *any* identified Blue object, it becomes Magenta (6).
2. If the pixel's column matches the center_col of *any* identified Blue object, it becomes Magenta (6).
Pixels that were originally Blue (1) remain Blue (1). All other Azure (8) pixels that do not meet 
conditions 1 or 2 remain Azure (8).
"""

import numpy as np
from collections import deque

# Define colors for clarity
BLUE = 1
AZURE = 8
MAGENTA = 6

def find_objects(grid, color):
    """
    Finds all contiguous objects of a given color in the grid using BFS.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples 
              of pixels belonging to a single object. Returns an empty list
              if no objects of the specified color are found.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check 4 cardinal neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor is the correct color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the found object's pixels to the list if it's not empty
                if obj_pixels:
                    objects.append(obj_pixels)
                    
    return objects

def get_object_properties(obj_pixels):
    """
    Calculates the bounding box and center of an object based on its pixels.

    Args:
        obj_pixels (set): A set of (row, col) tuples representing the object.

    Returns:
        tuple: (min_row, max_row, min_col, max_col, center_row, center_col)
               Returns None if the object pixel set is empty.
    """
    if not obj_pixels:
        return None

    # Extract all row and column indices
    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    
    # Determine bounding box
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    # Calculate center using integer division based on bounding box
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2
    
    return min_row, max_row, min_col, max_col, center_row, center_col


def transform(input_grid):
    """
    Applies the transformation rule: changes Azure pixels to Magenta if they lie 
    on the center row or center column of any Blue object.
    
    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Find all blue objects in the input grid
    blue_objects_pixels = find_objects(input_grid, BLUE)
    
    # Calculate properties (bounding box, center) for each blue object
    object_properties = []
    for obj_pix in blue_objects_pixels:
        props = get_object_properties(obj_pix)
        if props:
            object_properties.append(props)

    # Iterate through each pixel of the grid to determine its output color
    for r in range(rows):
        for c in range(cols):
            # Only consider changing pixels that are initially Azure
            if input_grid[r, c] == AZURE:
                should_be_magenta = False
                # Check conditions against all found blue objects
                for props in object_properties:
                    # Unpack properties - we only need the center coordinates here
                    _min_r, _max_r, _min_c, _max_c, center_r, center_c = props
                    
                    # Check if the current pixel's row matches the object's center row
                    if r == center_r:
                        should_be_magenta = True
                        break  # Found a match, no need to check other objects for this pixel
                        
                    # Check if the current pixel's column matches the object's center column
                    if c == center_c:
                        should_be_magenta = True
                        break  # Found a match, no need to check other objects for this pixel
                        
                # If any blue object's center axis matched, change the pixel to Magenta
                if should_be_magenta:
                    output_grid[r, c] = MAGENTA

    # Return the modified grid
    return output_grid