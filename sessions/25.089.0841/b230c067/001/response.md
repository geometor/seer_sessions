```python
import numpy as np
from collections import deque

"""
This program identifies all distinct contiguous objects of azure color (8) in an input grid. 
It calculates the size (pixel count) and finds the top-leftmost pixel (minimum row, then minimum column) for each object. 
It then determines the object with the smallest size. If multiple objects share the smallest size, 
it selects the one whose top-left pixel has the minimum row index. If there's still a tie, 
it selects the one whose top-left pixel has the minimum column index. 
This selected 'target' object is recolored to red (2) in the output grid. 
All other original azure objects are recolored to blue (1). 
The background (white, 0) remains unchanged.
"""

def find_objects(grid, target_color):
    """
    Finds all distinct contiguous objects of a specific color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'pixels' (list of (r, c) tuples), 'size' (int),
              and 'top_left' (tuple (r, c)).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start BFS to find a new object
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c_for_min_r = r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))

                    # Update top-left pixel tracking
                    if row < min_r:
                        min_r = row
                        min_c_for_min_r = col
                    elif row == min_r and col < min_c_for_min_r:
                        min_c_for_min_r = col
                        
                    # Explore neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_pixels:
                    objects.append({
                        'pixels': obj_pixels,
                        'size': len(obj_pixels),
                        'top_left': (min_r, min_c_for_min_r)
                    })
    return objects

def transform(input_grid):
    """
    Transforms the input grid by recoloring azure objects based on size and position.

    Args:
        input_grid (np.ndarray): The 2D input grid.

    Returns:
        np.ndarray: The transformed 2D output grid.
    """
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    azure_color = 8
    blue_color = 1
    red_color = 2

    # Find all azure objects
    azure_objects = find_objects(input_grid, azure_color)

    # If no azure objects, return the original grid copy
    if not azure_objects:
        return output_grid

    # Find the minimum size
    min_size = min(obj['size'] for obj in azure_objects)

    # Filter objects with the minimum size
    min_size_objects = [obj for obj in azure_objects if obj['size'] == min_size]

    target_object = None
    # Determine the target object based on size and tie-breaking rules
    if len(min_size_objects) == 1:
        target_object = min_size_objects[0]
    else:
        # Tie-breaking rule 1: Minimum row index of top-left pixel
        min_row = min(obj['top_left'][0] for obj in min_size_objects)
        min_row_objects = [obj for obj in min_size_objects if obj['top_left'][0] == min_row]

        if len(min_row_objects) == 1:
            target_object = min_row_objects[0]
        else:
            # Tie-breaking rule 2: Minimum column index of top-left pixel
            min_col = min(obj['top_left'][1] for obj in min_row_objects)
            # There should be exactly one object matching this final criterion
            target_object = [obj for obj in min_row_objects if obj['top_left'][1] == min_col][0]

    # Recolor the objects in the output grid
    for obj in azure_objects:
        color_to_use = red_color if obj == target_object else blue_color
        for r, c in obj['pixels']:
            output_grid[r, c] = color_to_use

    return output_grid
```