import numpy as np
from collections import deque

"""
Identifies contiguous objects of orange (7) pixels in the input grid using 4-way adjacency.
Determines the size (number of pixels) of each orange object.
Replaces the orange pixels of each object in the output grid with a new color based on the object's size:
- Size 1: Replace with green (3).
- Size 2: Replace with red (2).
- Size 3: Replace with magenta (6).
All other pixels (including white background) remain unchanged.
"""

def find_objects(grid, color):
    """
    Finds all connected components (objects) of a given color in the grid using 4-way adjacency.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited, start a search
            if grid[r, c] == color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])  # Use deque for efficient BFS queue
                visited[r, c] = True

                while q:
                    row, col = q.popleft() # BFS
                    current_object_coords.append((row, col))

                    # Check neighbors (4-way adjacency: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and if the neighbor is the target color and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the found object (list of coordinates) to our list of objects
                if current_object_coords:
                    objects.append(current_object_coords)
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Define colors involved in the transformation
    orange_color = 7
    green_color = 3
    red_color = 2
    magenta_color = 6

    # Find all distinct orange objects in the input grid
    orange_objects = find_objects(input_grid, orange_color)

    # Iterate through each found orange object
    for obj_coords in orange_objects:
        # Calculate the size of the current object
        obj_size = len(obj_coords)

        # Determine the target color based on the object's size according to the refined rule
        target_color = -1 # Initialize with a value indicating no rule matched
        if obj_size == 1:
            target_color = green_color
        elif obj_size == 2:
            target_color = red_color
        elif obj_size == 3:
            target_color = magenta_color
        # Note: Objects of other sizes will remain orange as output_grid is a copy

        # If a size rule matched (size 1, 2, or 3), change the pixels in the output grid
        if target_color != -1:
            for r, c in obj_coords:
                output_grid[r, c] = target_color

    # Return the modified grid
    return output_grid