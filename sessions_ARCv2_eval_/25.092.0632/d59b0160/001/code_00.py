import numpy as np
from collections import deque

"""
Identifies a specific anchor object (a 1x4 horizontal line of green (3) pixels, typically at row 3, cols 0-3). 
Finds all other distinct objects (contiguous non-background pixels) in the input grid. 
Determines which objects are adjacent (sharing a side or corner) to the anchor object.
Creates an output grid by copying the input grid. 
Removes objects (replaces their pixels with the background color orange (7)) if they are *not* adjacent to the anchor object. 
Preserves the anchor object and all objects adjacent to it.
"""

def find_objects(grid, background_color):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to ignore when finding objects.

    Returns:
        list: A list where each element is a tuple containing:
              - color (int): The color of the object.
              - coords (set): A set of (row, col) tuples representing the object's pixels.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and (r, c) not in visited:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               (nr, nc) not in visited and \
                               grid[nr, nc] == color:
                                visited.add((nr, nc))
                                obj_coords.add((nr, nc))
                                q.append((nr, nc))
                objects.append({'color': color, 'coords': obj_coords})
    return objects

def get_neighbor_coords(coords, max_row, max_col):
    """
    Gets all unique neighboring coordinates (including diagonals) for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples.
        max_row (int): Maximum row index.
        max_col (int): Maximum column index.

    Returns:
        set: A set of unique (row, col) tuples representing neighbors.
    """
    neighbors = set()
    for r, c in coords:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < max_row and 0 <= nc < max_col:
                    neighbors.add((nr, nc))
    # Remove the original coordinates themselves if they ended up in neighbors
    neighbors = neighbors - coords
    return neighbors


def transform(input_grid):
    """
    Transforms the input grid based on object adjacency to a specific anchor object.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: The transformed 2D output grid.
    """
    # Constants
    background_color = 7
    anchor_color = 3
    rows, cols = input_grid.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find all objects in the grid
    all_objects = find_objects(input_grid, background_color)

    # Identify the anchor object(s) - assuming there might be multiple parts or instances
    anchor_objects = [obj for obj in all_objects if obj['color'] == anchor_color]
    
    # Combine all coordinates of the anchor object parts into one set
    anchor_coords = set()
    for obj in anchor_objects:
        anchor_coords.update(obj['coords'])
        
    # If no anchor object found, return the original grid (or handle as error)
    if not anchor_coords:
        # Based on examples, anchor is always present. If not, returning input might be safest.
        return output_grid 

    # Find the adjacency zone around the anchor object
    # This includes all pixels directly neighboring any pixel of the anchor object
    anchor_adjacency_zone = get_neighbor_coords(anchor_coords, rows, cols)
    # Also include the anchor coordinates themselves in the 'keep' zone
    keep_zone = anchor_coords.union(anchor_adjacency_zone)


    # Identify objects to keep and remove
    objects_to_remove = []
    for obj in all_objects:
        # Skip the anchor object itself
        if obj['color'] == anchor_color:
            continue

        # Check if any part of the object touches the adjacency zone OR is part of the anchor
        is_adjacent = False
        for coord in obj['coords']:
            if coord in keep_zone: 
                is_adjacent = True
                break
        
        if not is_adjacent:
            objects_to_remove.append(obj)

    # Modify the output grid by removing non-adjacent objects
    for obj in objects_to_remove:
        for r, c in obj['coords']:
            output_grid[r, c] = background_color

    return output_grid