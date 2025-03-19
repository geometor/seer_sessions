"""
Transforms the input grid by rotating a connected red (2) object 90 degrees clockwise. Green (3) pixels remain in their original positions.
"""

import numpy as np

def find_connected_objects(grid, color):
    """
    Finds connected components of a given color in a grid.

    Args:
        grid: A numpy array representing the grid.
        color: The color to find connected components for.

    Returns:
        A list of lists, where each inner list contains the coordinates of
        a connected component.
    """
    visited = set()
    objects = []

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def rotate_object_90(object_coords):
    """Rotates a set of coordinates 90 degrees clockwise around its centroid."""
    if not object_coords:
        return []

    # Convert to numpy array for easier calculations
    coords = np.array(object_coords)

    # Calculate the centroid
    centroid = coords.mean(axis=0)

    # Rotate each point around the centroid
    rotated_coords = []
    for r, c in coords:
        # Translate to origin, rotate, then translate back
        translated_r = r - centroid[0]
        translated_c = c - centroid[1]
        rotated_r = translated_c + centroid[0]
        rotated_c = -translated_r + centroid[1]
        rotated_coords.append((rotated_r, rotated_c))

    return rotated_coords

def transform(input_grid):
    # Initialize output grid with the same dimensions, filled with white (0).
    output_grid = np.zeros_like(input_grid)

    # Find connected objects for green and red pixels.
    green_objects = find_connected_objects(input_grid, 3)
    red_objects = find_connected_objects(input_grid, 2)

    # Place green pixels in the output grid (invariant).
    for obj in green_objects:
        for r, c in obj:
            output_grid[int(r), int(c)] = 3

    # Rotate red object (only one red object is expected).
    for red_object in red_objects:  # Should ideally be just one
       rotated_red_object = rotate_object_90(red_object)
       for r, c in rotated_red_object:
            r = int(round(r))  #important - round to the nearest integer
            c = int(round(c))
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                output_grid[r,c] = 2


    return output_grid