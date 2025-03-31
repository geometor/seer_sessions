import numpy as np
from collections import deque

"""
Identify all separate, contiguous objects composed of azure (8) pixels in the input grid.
Determine the order of these objects by finding the top-most, left-most pixel of each object and sorting them first by row index, then by column index.
Create the output grid, initially identical to the input grid.
Iterate through the identified azure objects based on the determined order.
For the second object in the sequence, change all its azure (8) pixels to red (2) in the output grid.
For all other objects (the first, third, fourth, etc.), change all their azure (8) pixels to blue (1) in the output grid.
Leave all white (0) background pixels unchanged.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of (row, col) coordinates.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) to find the contiguous object
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_coords.append((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check grid boundaries
                        if 0 <= nr < rows and 0 <= nc < cols:
                             # Check if neighbor is the same color and not visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                # Add the found object's coordinates to the list of objects
                objects.append(current_object_coords)
                
    return objects

def get_top_left_coord(obj_coords):
    """
    Finds the top-most, left-most coordinate of an object.

    Args:
        obj_coords (list): A list of (row, col) coordinates for an object.

    Returns:
        tuple: The (row, col) coordinate of the top-left pixel.
    """
    # Sort coordinates primarily by row, secondarily by column.
    # The first coordinate after sorting is the top-left one.
    return sorted(obj_coords)[0]

def transform(input_grid):
    """
    Transforms the input grid by finding azure objects, ordering them,
    and recoloring the second object red and all others blue.

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
    
    # Find all distinct azure objects
    azure_objects = find_objects(output_grid, azure_color)

    # If there are no azure objects, return the grid as is
    if not azure_objects:
        return output_grid

    # Sort the objects based on their top-most, left-most pixel
    # The key function finds the top-left coordinate for each object
    azure_objects.sort(key=get_top_left_coord)

    # Recolor the objects based on their sorted order
    for i, obj_coords in enumerate(azure_objects):
        # Determine the target color based on the object's order index
        if i == 1:  # The second object (index 1)
            target_color = red_color
        else:       # All other objects (index 0, 2, 3, ...)
            target_color = blue_color

        # Change the color of all pixels belonging to the current object
        for r, c in obj_coords:
            output_grid[r, c] = target_color

    return output_grid