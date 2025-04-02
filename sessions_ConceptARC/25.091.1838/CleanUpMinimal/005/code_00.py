"""
Identify all separate, contiguous groups of pixels in the input grid that are not the background color (white, 0). Record the color, size (pixel count), and coordinates of each group (object). Find the object(s) with the largest size. Determine the color of this largest object(s) - call this the "target color". Create a new output grid of the same dimensions as the input, initially filled completely with the background color (white, 0). Go through each object identified. If the object's color is the same as the "target color", copy all pixels belonging to this object to the corresponding positions in the output grid, keeping their "target color". If the object's color is *different* from the "target color", check if *any* pixel in this object is directly adjacent (up, down, left, or right) to *any* pixel that belongs to *any* object having the "target color". If such adjacency is found for the non-target-color object, then color *all* pixels corresponding to this object's original positions with the "target color" in the output grid. If no such adjacency is found for the non-target-color object, leave its corresponding pixels as the background color (white, 0) in the output grid. The final output grid is the result of applying these rules to all identified objects.
"""

import numpy as np
from collections import deque

def find_objects(grid, background_color=0):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The color considered as background.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains keys 'coords' (a set of (row, col) tuples),
              'color' (int), and 'size' (int).
              Returns an empty list if no non-background objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is non-background and not yet visited
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                # Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Check cardinal neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within bounds, has the same color, and hasn't been visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Store the found object with its coordinates, color, and size
                objects.append({'coords': obj_coords, 'color': int(color), 'size': len(obj_coords)})

    return objects

def check_adjacency(obj_coords, target_coords, grid_shape):
    """
    Checks if any pixel in obj_coords is cardinally adjacent to any pixel in target_coords.

    Args:
        obj_coords (set): Set of coordinates for the object to check.
        target_coords (set): Set of coordinates for the target color objects.
        grid_shape (tuple): Shape (rows, cols) of the grid.

    Returns:
        bool: True if any pixel in obj_coords is adjacent to target_coords, False otherwise.
    """
    rows, cols = grid_shape
    for r, c in obj_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in target_coords:
                return True
    return False

def transform(input_grid):
    """
    Transforms the input grid based on the refined rule involving the largest object's color
    and adjacency for other colored objects.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    background_color = 0

    # Initialize the output grid with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Find all non-background objects in the input grid
    objects = find_objects(input_grid_np, background_color)

    # If no non-background objects are found, return the initialized background grid
    if not objects:
        return output_grid.tolist()

    # Find the maximum size among all objects
    max_size = 0
    for obj in objects:
        if obj['size'] > max_size:
            max_size = obj['size']

    # Determine the target color (color of any object with max_size)
    target_color = -1 # Should be overwritten
    for obj in objects:
        if obj['size'] == max_size:
            target_color = obj['color']
            break

    # Collect all coordinates of objects with the target color
    target_color_coords = set()
    for obj in objects:
        if obj['color'] == target_color:
            target_color_coords.update(obj['coords'])

    # Iterate through all objects to populate the output grid
    for obj in objects:
        # If the object's color is the target color, copy it directly
        if obj['color'] == target_color:
            for r, c in obj['coords']:
                output_grid[r, c] = target_color
        # If the object's color is not the target color, check for adjacency
        else:
            # Check if this object is adjacent to any target color pixel
            is_adjacent = check_adjacency(obj['coords'], target_color_coords, input_grid_np.shape)
            # If adjacent, color this object's pixels with the target color
            if is_adjacent:
                for r, c in obj['coords']:
                    output_grid[r, c] = target_color
            # If not adjacent, leave as background (already initialized)

    # Convert the final numpy grid back to a list of lists
    return output_grid.tolist()