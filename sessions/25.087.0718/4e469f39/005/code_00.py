import numpy as np
from collections import deque

"""
Transforms the input grid based on gray (5) objects.
1. Identifies contiguous gray (5) objects using 4-way adjacency.
2. For each gray object:
    a. Determines its bounding box (min/max row and column).
    b. If the object is not touching the top border (min_row > 0), draws a 
       horizontal red (2) line in the output grid one row above the object's 
       bounding box, spanning the width of the bounding box (min_col to max_col).
    c. Identifies specific white (0) pixels within the bounding box to fill with red (2). 
       A white pixel (r, c) within the bounding box is filled if it is 4-way 
       adjacent to at least one gray pixel belonging to that specific gray object.
3. Gray pixels and other pixels remain unchanged.
"""

def find_objects(grid, color_code):
    """
    Finds all contiguous objects of a specific color in the grid using 4-way adjacency.

    Args:
        grid (np.array): The input grid.
        color_code (int): The color code of the objects to find.

    Returns:
        list: A list of sets, where each set contains tuples of (row, col)
              coordinates for one object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color_code and not visited[r, c]:
                current_object = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object.add((row, col))
                    
                    # Check 4 neighbors (standard ARC connectivity for objects)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color_code and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_object:
                    objects.append(current_object)
                    
    return objects

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box for a set of coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if coords is empty.
    """
    if not obj_coords:
        return None
    
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    
    min_r = min(rows)
    max_r = max(rows)
    min_c = min(cols)
    max_c = max(cols)
    
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Identify all distinct contiguous objects composed of gray (5) pixels.
    gray_objects = find_objects(input_grid, 5)

    # Process each identified gray object.
    for obj_coords in gray_objects:
        # Determine the coordinates of its bounding box.
        bbox = get_bounding_box(obj_coords)
        if bbox is None:
            continue # Should not happen with valid objects, but safe check.
            
        min_r, max_r, min_c, max_c = bbox
        
        # Check if the object touches the top edge of the grid.
        # If not, draw a red line above it.
        if min_r > 0:
            # Ensure the column range is valid before assignment
            if min_c <= max_c:
                 output_grid[min_r - 1, min_c : max_c + 1] = 2 # Red color
            
        # Examine every pixel coordinate (r, c) within the bounding box.
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                # Check if the pixel is white (0) in the *input* grid.
                if input_grid[r, c] == 0:
                    # Check if it shares an edge (4-way adjacent) with a gray pixel
                    # belonging to the *current* gray object.
                    is_adjacent_to_object_pixel = False
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        # Check bounds and if the neighbor is part of the current object
                        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in obj_coords:
                            is_adjacent_to_object_pixel = True
                            break # Found one adjacent gray pixel, no need to check more
                            
                    # If adjacent, change the pixel color to red (2) in the output grid.
                    if is_adjacent_to_object_pixel:
                        output_grid[r, c] = 2

    # Return the modified output grid.
    return output_grid