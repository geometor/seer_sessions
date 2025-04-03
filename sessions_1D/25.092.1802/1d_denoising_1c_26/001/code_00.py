"""
Retain only the largest contiguous object of the primary non-background color. 
All other non-background pixels are changed to the background color (white, 0).
The size, shape, color, and position of the largest object remain unchanged.
"""

import numpy as np
from collections import deque

def find_objects(grid):
    """
    Identifies all distinct contiguous objects of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'size', and 'pixels' (a set of (row, col) tuples).
              Returns an empty list if no non-background objects are found.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []
    background_color = 0

    for r in range(height):
        for c in range(width):
            # If the pixel is not background and not visited yet, start a search
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object_pixels.add((row, col))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, if it's the same color, and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'color': color,
                    'size': len(current_object_pixels),
                    'pixels': current_object_pixels
                })

    return objects

def transform(input_grid):
    """
    Transforms the input grid by keeping only the largest contiguous non-background object.

    Args:
        input_grid (np.ndarray): A 2D NumPy array representing the input grid.

    Returns:
        np.ndarray: A 2D NumPy array representing the output grid.
    """
    # Convert input list of lists to numpy array if necessary
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    background_color = 0

    # initialize output_grid with background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # Find all non-background objects
    objects = find_objects(input_grid_np)

    # If no objects found, return the background grid
    if not objects:
        return output_grid.tolist() # Return as list of lists per ARC standard

    # Find the largest object based on the number of pixels (size)
    largest_object = max(objects, key=lambda obj: obj['size'])

    # Get the color and pixel coordinates of the largest object
    largest_color = largest_object['color']
    largest_pixels = largest_object['pixels']

    # Draw the largest object onto the output grid
    for r, c in largest_pixels:
        output_grid[r, c] = largest_color

    # Return the output grid as a list of lists
    return output_grid.tolist()