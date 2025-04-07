import numpy as np
from collections import deque

"""
Identify a horizontal separator line (blue=1).
Define the area above the separator as the 'key area' and below as the 'work area'.
Find all contiguous non-background, non-separator colored objects in the key area. Record their shapes (relative pixel coordinates) and colors.
Find all contiguous gray (5) objects in the work area.
For each gray object, determine its shape.
If a gray object's shape matches the shape of a key object, replace the gray pixels in the output grid with the color of the matching key object.
Leave the key area, separator line, and background pixels in the work area unchanged.
"""

def find_objects(grid, target_colors, bounds=None):
    """
    Finds all contiguous objects of specified colors within given bounds.

    Args:
        grid (np.ndarray): The input grid.
        target_colors (list or set): The color(s) of the objects to find.
        bounds (tuple, optional): (min_row, max_row, min_col, max_col) defining the search area. 
                                  Defaults to the whole grid if None.

    Returns:
        list: A list of objects. Each object is a tuple: (color, set_of_coordinates).
              Coordinates are (row, col) tuples.
    """
    if bounds:
        min_row, max_row, min_col, max_col = bounds
    else:
        min_row, max_row = 0, grid.shape[0]
        min_col, max_col = 0, grid.shape[1]

    visited = np.zeros((max_row - min_row, max_col - min_col), dtype=bool)
    objects = []
    
    rows, cols = grid.shape
    
    for r in range(min_row, max_row):
        for c in range(min_col, max_col):
            # Adjust coordinates relative to the bounds for visited check
            visited_r, visited_c = r - min_row, c - min_col
            
            if not visited[visited_r, visited_c] and grid[r, c] in target_colors:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[visited_r, visited_c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check if neighbor is within grid and bounds
                        if min_row <= nr < max_row and min_col <= nc < max_col:
                           # Adjust coordinates relative to the bounds for visited check
                            visited_nr, visited_nc = nr - min_row, nc - min_col
                            # Check if neighbor is the same color and not visited
                            if grid[nr, nc] == color and not visited[visited_nr, visited_nc]:
                                visited[visited_nr, visited_nc] = True
                                q.append((nr, nc))
                                
                if obj_coords:
                    objects.append((color, obj_coords))
                    
    return objects

def get_object_shape(obj_coords):
    """
    Calculates the normalized shape of an object.

    Args:
        obj_coords (set): A set of (row, col) coordinates representing the object.

    Returns:
        tuple: A tuple of sorted relative coordinates ((r1, c1), (r2, c2), ...),
               representing the shape normalized to the top-left corner.
               Returns None if obj_coords is empty.
    """
    if not obj_coords:
        return None
        
    min_r = min(r for r, c in obj_coords)
    min_c = min(c for r, c in obj_coords)
    
    # Calculate relative coordinates and sort them for consistent representation
    relative_coords = sorted([(r - min_r, c - min_c) for r, c in obj_coords])
    
    return tuple(relative_coords)

def transform(input_grid):
    """
    Transforms the input grid by replacing gray shapes in the lower part 
    with colors based on matching shapes found in the upper part.
    """
    input_grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # 1. Find the separator line (assuming blue=1 and full width)
    separator_row = -1
    for r in range(rows):
        if np.all(input_grid[r, :] == 1):
            separator_row = r
            break
            
    if separator_row == -1:
        # No separator found, maybe return input or handle error
        print("Warning: Separator line not found.")
        return output_grid # Or raise an error depending on requirements

    # 2. Define key and work areas
    key_area_bounds = (0, separator_row, 0, cols) 
    work_area_bounds = (separator_row + 1, rows, 0, cols)

    # 3. Find key patterns (shapes and colors) in the key area
    # Exclude background (0) and separator color (1)
    key_colors = set(range(10)) - {0, 1} 
    key_objects = find_objects(input_grid, key_colors, key_area_bounds)
    
    key_patterns = {}
    for color, coords in key_objects:
        shape = get_object_shape(coords)
        if shape:
            # Store shape -> color mapping. Handle potential duplicate shapes if needed.
            # For now, last one wins if shapes are identical but colors differ (unlikely in ARC)
             key_patterns[shape] = color

    # 4. Find gray (5) objects in the work area
    gray_objects = find_objects(input_grid, {5}, work_area_bounds)

    # 5. Process gray objects: match shapes and replace colors
    for _, gray_coords in gray_objects:
        gray_shape = get_object_shape(gray_coords)
        
        if gray_shape and gray_shape in key_patterns:
            replacement_color = key_patterns[gray_shape]
            # Update the output grid
            for r, c in gray_coords:
                 # Check bounds just in case, though coords should be valid
                if 0 <= r < rows and 0 <= c < cols:
                    output_grid[r, c] = replacement_color

    return output_grid.tolist() # Return as list of lists