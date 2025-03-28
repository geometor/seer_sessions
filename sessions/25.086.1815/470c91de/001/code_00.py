import numpy as np
from collections import deque

"""
1. Initialize the output grid with the same dimensions as the input grid, filled entirely with the background color (Orange=7).
2. Identify all contiguous shapes in the input grid that are *not* the background color (Orange=7) and *not* the marker color (Azure=8).
3. For each identified shape:
    a. Find the single Azure (8) pixel that is adjacent (shares an edge or corner) to any pixel of this shape.
    b. Determine the direction of translation (up, down, left, right, or diagonal) from the shape towards the adjacent Azure pixel. This is a one-step move.
    c. Apply this one-step translation to all pixels belonging to the current shape.
    d. Draw the translated shape onto the output grid using its original color.
4. Return the completed output grid. (Azure pixels are implicitly removed).
"""

def find_objects(grid, background_color, marker_color):
    """
    Finds all contiguous objects in the grid that are not background or marker color.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to ignore as background.
        marker_color (int): The color to ignore as marker.

    Returns:
        list: A list of tuples, where each tuple represents an object:
              (color, set_of_coordinates).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if not visited[r, c] and color != background_color and color != marker_color:
                obj_color = color
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check 4 neighbors (can extend to 8 if needed, but not required for object connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == obj_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append((obj_color, obj_pixels))
                
    return objects

def get_adjacent_marker_and_translation(grid, obj_pixels, marker_color):
    """
    Finds the unique marker adjacent to the object and calculates the translation vector.

    Args:
        grid (np.array): The input grid.
        obj_pixels (set): A set of (row, col) coordinates for the object's pixels.
        marker_color (int): The color of the marker pixel.

    Returns:
        tuple: (dr, dc) translation vector, or None if no adjacent marker found.
    """
    height, width = grid.shape
    
    for r_obj, c_obj in obj_pixels:
        # Check 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self
                
                nr, nc = r_obj + dr, c_obj + dc
                
                if 0 <= nr < height and 0 <= nc < width:
                    if grid[nr, nc] == marker_color:
                        # Found the adjacent marker. Calculate translation vector.
                        # The vector points from the object pixel towards the marker pixel.
                        # Since it's a 1-step move, the components are -1, 0, or 1.
                        # We just need the sign of the difference.
                        
                        # Find *any* pair of adjacent object/marker pixels to determine direction
                        marker_r, marker_c = nr, nc 
                        
                        # Example: marker is at (r+1, c+1) relative to object pixel (r,c)
                        # Delta_r = (r+1) - r = 1
                        # Delta_c = (c+1) - c = 1
                        # Translation vector (dr, dc) = (sign(1), sign(1)) = (1, 1) -> move down-right
                        
                        # Find *one* pair to get the direction
                        
                        # Iterate neighbors of the marker to find an object pixel
                        for mdr in [-1, 0, 1]:
                             for mdc in [-1, 0, 1]:
                                 if mdr == 0 and mdc == 0:
                                     continue
                                 obj_check_r, obj_check_c = marker_r + mdr, marker_c + mdc
                                 if (obj_check_r, obj_check_c) in obj_pixels:
                                     # Found an adjacent object pixel, calculate translation
                                     delta_r = marker_r - obj_check_r
                                     delta_c = marker_c - obj_check_c
                                     trans_dr = int(np.sign(delta_r))
                                     trans_dc = int(np.sign(delta_c))
                                     return (trans_dr, trans_dc)
                                     
    return None # Should not happen based on problem description

def transform(input_grid):
    """
    Moves each colored object (not background or marker) one step towards 
    its adjacent marker pixel (Azure=8). The marker pixel is removed, and 
    the space vacated by the object is filled with the background color (Orange=7).

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    background_color = 7
    marker_color = 8
    
    # Initialize output grid with background color
    output_grid = np.full_like(input_np, background_color)
    
    # Find all objects (color and pixel coordinates)
    objects = find_objects(input_np, background_color, marker_color)
    
    # Process each object
    for obj_color, obj_pixels in objects:
        # Find the adjacent marker and the required translation vector
        translation_vector = get_adjacent_marker_and_translation(input_np, obj_pixels, marker_color)
        
        if translation_vector:
            dr, dc = translation_vector
            
            # Apply translation to each pixel of the object
            for r, c in obj_pixels:
                new_r, new_c = r + dr, c + dc
                
                # Draw the translated pixel onto the output grid if within bounds
                if 0 <= new_r < height and 0 <= new_c < width:
                    output_grid[new_r, new_c] = obj_color
        else:
             # This case is unexpected based on the examples, but handle defensively
             # If no marker found, just copy the object as is? Or raise error?
             # For now, let's copy it without moving, although this likely indicates an issue.
             print(f"Warning: No adjacent marker found for object with color {obj_color} at {min(obj_pixels)}")
             for r, c in obj_pixels:
                 if 0 <= r < height and 0 <= c < width: # Should always be true
                    output_grid[r, c] = obj_color


    return output_grid.tolist()
