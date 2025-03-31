import numpy as np
from collections import deque

"""
Identifies all separate, contiguous objects composed of azure (8) pixels in the input grid. 
Calculates the size (pixel count) of each object. Finds the object(s) with the minimum size.
If there's a tie for minimum size, selects the one whose top-most, left-most pixel appears earliest in scan order (row-major).
Colors the selected smallest object red (2) and all other azure objects blue (1). Leaves the background white (0).
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid using BFS.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of (row, col) coordinates.
              Returns an empty list if no objects of the specified color are found.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find an unvisited pixel of the target color
            if grid[r, c] == color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_coords.append((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check grid boundaries and if neighbor is same color and unvisited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                                
                # Store the coordinates of the found object
                if current_object_coords:
                    objects.append(current_object_coords)
                
    return objects

def get_object_properties(obj_coords):
    """
    Calculates properties of an object: size and top-left coordinate.

    Args:
        obj_coords (list): A list of (row, col) coordinates for an object.

    Returns:
        dict: A dictionary containing 'coords', 'size', and 'top_left'.
              Returns None if obj_coords is empty.
    """
    if not obj_coords:
        return None
        
    # Size is the number of coordinates
    size = len(obj_coords)
    
    # Sort coordinates primarily by row, secondarily by column to find top-left
    top_left = sorted(obj_coords)[0]
    
    return {'coords': obj_coords, 'size': size, 'top_left': top_left}

def transform(input_grid):
    """
    Transforms the input grid by finding azure objects, identifying the smallest
    (first by scan order in case of tie), coloring it red, and others blue.

    Args:
        input_grid (np.array): The input grid with azure (8) objects on a white (0) background.

    Returns:
        np.array: The transformed grid with objects colored blue (1) or red (2).
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Define colors
    azure_color = 8
    blue_color = 1
    red_color = 2
    
    # 1. Identify all azure objects
    azure_object_coords_list = find_objects(output_grid, azure_color)

    # If there are no azure objects, return the grid as is
    if not azure_object_coords_list:
        return output_grid

    # 2. Calculate properties (size, top-left) for each object
    object_properties = [get_object_properties(coords) for coords in azure_object_coords_list]
    
    # 3. Find the minimum size among all objects
    min_size = min(prop['size'] for prop in object_properties)
    
    # 4. Create a list of objects that have this minimum size
    min_size_objects = [prop for prop in object_properties if prop['size'] == min_size]
    
    # 5. Sort the minimum-sized objects by their top-left coordinate (scan order)
    min_size_objects.sort(key=lambda x: x['top_left'])
    
    # 6. Select the first object from this sorted list as the target to color red
    target_object_to_color_red_coords = set(min_size_objects[0]['coords']) # Use set for faster lookup

    # 7. Iterate through all originally identified objects and apply recoloring
    for obj_prop in object_properties:
        current_coords = obj_prop['coords']
        # Check if the *first coordinate* of the current object matches the first coordinate
        # of the target object. Since coordinates within an object are unique, comparing
        # the first coordinate (or any coordinate) is sufficient to identify the object.
        # A more robust check compares the entire set of coordinates, but using the top-left
        # is simpler if we trust find_objects returns distinct objects.
        # Let's use the full coordinate set comparison for robustness.
        
        is_target_object = set(current_coords) == target_object_to_color_red_coords
        
        # Determine the color based on whether it's the target object
        target_color = red_color if is_target_object else blue_color
            
        # Change the color of all pixels belonging to the current object
        for r, c in current_coords:
            output_grid[r, c] = target_color
            
    # 8. Return the modified grid
    return output_grid