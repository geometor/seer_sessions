import numpy as np
from collections import deque

"""
Identifies distinct blue (1) objects in the input grid using 4-way adjacency.
Determines if a blue object encloses an area of white (0) pixels. An enclosure means
there are white pixels adjacent to the object that cannot reach the grid boundary
by moving only through other white pixels (4-way adjacency).
If a blue object encloses a white area (contains a 'hole'), all its pixels are 
recolored to green (3) in the output grid.
Blue objects that do not enclose any white area remain blue (1).
All other pixels (including the background) remain unchanged.
"""

def find_objects(grid, color):
    """
    Finds all distinct connected objects of a given color in the grid using BFS.
    Connectivity is based on 4-way adjacency (up, down, left, right).

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of a single connected object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    for r in range(rows):
        for c in range(cols):
            # If the pixel is the target color and hasn't been visited yet, start BFS
            if grid[r, c] == color and (r, c) not in visited:
                current_object = set()
                q = deque([(r, c)])
                visited.add((r, c))
                current_object.add((r, c))

                while q:
                    row, col = q.popleft()
                    
                    # Check 4 neighbors
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc

                        # Check bounds, color, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            current_object.add((nr, nc))
                            q.append((nr, nc))
                
                # Add the found object to the list
                objects.append(current_object)
    return objects

def find_external_white_pixels(grid):
    """
    Finds all white pixels connected to the grid boundary using BFS.

    Args:
        grid (np.array): The input grid.
        
    Returns:
        set: A set of (row, col) tuples representing external white pixels.
    """
    rows, cols = grid.shape
    white = 0
    external_white = set()
    visited = set()
    q = deque()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Add all boundary white pixels to the queue and sets
    for r in range(rows):
        for c in [0, cols - 1]: # Left and Right boundaries
            if grid[r, c] == white and (r, c) not in visited:
                visited.add((r, c))
                external_white.add((r, c))
                q.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]: # Top and Bottom boundaries
             if grid[r, c] == white and (r, c) not in visited:
                visited.add((r, c))
                external_white.add((r, c))
                q.append((r, c))

    # Perform BFS from boundary white pixels
    while q:
        r, c = q.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check bounds, color, and visited status
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == white and (nr, nc) not in visited:
                visited.add((nr, nc))
                external_white.add((nr, nc))
                q.append((nr, nc))

    return external_white


def check_for_internal_hole(grid, object_coords, external_white):
    """
    Checks if any pixel of the object is adjacent to an internal white pixel.

    Args:
        grid (np.array): The input grid.
        object_coords (set): Coordinates of the object's pixels.
        external_white (set): Coordinates of white pixels connected to the boundary.

    Returns:
        bool: True if the object is adjacent to an internal white pixel, False otherwise.
    """
    rows, cols = grid.shape
    white = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Check neighbors of all pixels belonging to the object
    for r, c in object_coords:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is white AND NOT external
                if grid[nr, nc] == white and (nr, nc) not in external_white:
                    return True # Found an adjacent internal white pixel

    return False # No adjacent internal white pixels found


def transform(input_grid):
    """
    Transforms the input grid by recoloring blue objects that enclose white areas to green.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Define colors
    blue = 1
    green = 3
    white = 0

    # Find all distinct blue objects
    blue_objects = find_objects(input_grid, blue)

    # Find all white pixels connected to the boundary
    external_white_pixels = find_external_white_pixels(input_grid)

    # Iterate through each identified blue object
    for obj_coords in blue_objects:
        # Check if the current object encloses an internal white area (hole)
        if check_for_internal_hole(input_grid, obj_coords, external_white_pixels):
            # If it encloses a hole, recolor all pixels of this object to green
            for r, c in obj_coords:
                output_grid[r, c] = green
        # If it doesn't enclose a hole, it remains blue (already copied)

    return output_grid