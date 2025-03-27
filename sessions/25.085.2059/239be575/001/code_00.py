"""
Identify all distinct contiguous groups of red (2) pixels (Red Objects) and azure (8) pixels (Azure Objects).
Check if any single Azure Object is adjacent (including diagonals) to at least one pixel from *every* distinct Red Object.
If such an Azure Object exists, output 8. Otherwise, output 0.
If there are no Red Objects, output 0.
"""

import numpy as np
from collections import deque

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to find objects for.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of a single object.
    """
    height, width = grid.shape
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and (r, c) not in visited:
                # Start BFS for a new object
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 8 neighbors (Moore neighborhood)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds and if it's the target color and not visited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                obj_coords.add((nr, nc))
                                q.append((nr, nc))
                objects.append(obj_coords)
    return objects

def get_neighbors(coord, grid_shape):
    """
    Gets all 8 neighboring coordinates for a given coordinate, within grid bounds.

    Args:
        coord (tuple): The (row, col) coordinate.
        grid_shape (tuple): The (height, width) of the grid.

    Returns:
        set: A set of valid neighbor (row, col) tuples.
    """
    r, c = coord
    height, width = grid_shape
    neighbors = set()
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.add((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid based on the adjacency rule between azure and red objects.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        int: 8 if a single azure object touches all red objects, 0 otherwise.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Find all Red Objects (color 2)
    red_objects = find_objects(grid, 2)

    # 2. Handle the case where there are no Red Objects
    if not red_objects:
        return 0 # Output is 0 if no red objects

    # 3. Find all Azure Objects (color 8)
    azure_objects = find_objects(grid, 8)

    # Create a mapping from each red pixel coordinate to the index of the Red Object it belongs to.
    # This helps quickly identify which red object a neighbor belongs to.
    red_pixel_to_object_index = {}
    for i, red_obj_coords in enumerate(red_objects):
        for coord in red_obj_coords:
            red_pixel_to_object_index[coord] = i

    # 4. Iterate through each Azure Object
    for azure_obj_coords in azure_objects:
        touched_red_indices = set() # Keep track of which Red Objects this Azure Object touches

        # 5. For the current Azure Object, check its adjacency to Red Objects
        # Iterate through each pixel of the current Azure object
        for azure_coord in azure_obj_coords:
            # Find all neighbors of the current azure pixel
            neighbors = get_neighbors(azure_coord, (height, width))
            # Check if any neighbor belongs to a Red Object
            for neighbor_coord in neighbors:
                if neighbor_coord in red_pixel_to_object_index:
                    # If a neighbor is red, find which Red Object it belongs to
                    red_obj_index = red_pixel_to_object_index[neighbor_coord]
                    # Record that this Red Object index has been touched by the current Azure Object
                    touched_red_indices.add(red_obj_index)

        # 6. Check if this Azure Object touched *all* Red Objects
        if len(touched_red_indices) == len(red_objects):
            # If the number of touched Red Object indices equals the total number of Red Objects,
            # this Azure Object is our connector.
            return 8 # Output 8

    # 7. If no Azure Object touched all Red Objects after checking all of them
    return 0 # Output 0