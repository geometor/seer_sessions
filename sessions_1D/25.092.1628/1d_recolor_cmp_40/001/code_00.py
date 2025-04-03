"""
Identify all distinct connected groups (objects) of maroon (9) pixels in the input grid, considering pixels connected horizontally or vertically as part of the same object. Calculate the size (number of pixels) for each identified maroon object. Determine the maximum size among these objects. Locate the maroon object that corresponds to this maximum size. Create a copy of the input grid. Change the color of all pixels belonging to the identified largest maroon object from maroon (9) to yellow (4) in the copied grid. The resulting grid is the output.
"""

import numpy as np
from collections import deque

def find_objects(grid, target_color):
    """
    Finds all connected objects of a specific color in a grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start BFS for a new object
                current_object = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object.append((row, col))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by finding the largest maroon (9) object 
    and changing its color to yellow (4).

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(grid_np)

    # Define target and replacement colors
    target_color = 9  # maroon
    replacement_color = 4  # yellow

    # Find all objects of the target color (maroon)
    maroon_objects = find_objects(grid_np, target_color)

    # If no maroon objects are found, return the original grid
    if not maroon_objects:
        return output_grid.tolist()

    # Find the largest object
    largest_object = []
    max_size = -1
    for obj in maroon_objects:
        if len(obj) > max_size:
            max_size = len(obj)
            largest_object = obj
        # Note: If multiple objects have the same max size, the first one found is chosen.
        # The problem description implies a unique largest object or doesn't specify tie-breaking.

    # Change the color of the pixels belonging to the largest object
    for r, c in largest_object:
        output_grid[r, c] = replacement_color

    # Convert back to list of lists before returning
    return output_grid.tolist()