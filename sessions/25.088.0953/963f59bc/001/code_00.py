import numpy as np
from collections import deque

"""
Identifies the largest contiguous object (pattern) and all single-pixel objects (targets) in the input grid.
For each target pixel, copies the pattern object, colors it with the target's color, and places the colored copy onto the grid such that the top-left pixel of the pattern aligns with the target pixel's location.
The original objects remain in the output grid.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of objects. Each object is a dictionary containing:
              'color': The color of the object.
              'coords': A set of (row, col) tuples representing the object's pixels.
              'min_r': The minimum row index.
              'min_c': The minimum column index.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    coords.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'color': color,
                    'coords': coords,
                    'min_r': min_r,
                    'min_c': min_c
                })
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on identifying a pattern object and target pixels.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier handling
    grid = np.array(input_grid)
    rows, cols = grid.shape
    
    # Initialize output grid as a copy of the input
    output_grid = grid.copy()

    # Find all non-background objects
    objects = find_objects(grid)

    if not objects:
        return output_grid # No objects, return copy of input

    # Find the largest object (pattern) and single-pixel objects (targets)
    pattern_object = None
    target_pixels = []
    max_size = 0

    for obj in objects:
        size = len(obj['coords'])
        if size == 1:
            # It's a target pixel
            # Get the single coordinate from the set
            target_coord = next(iter(obj['coords'])) 
            target_pixels.append({
                'color': obj['color'],
                'loc': target_coord # (row, col)
            })
        if size > max_size:
            max_size = size
            pattern_object = obj

    # If no multi-pixel object found, or no targets, return the original grid (or potentially just targets?)
    # Based on examples, if there's no pattern, nothing happens. If no targets, nothing happens.
    if pattern_object is None or not target_pixels:
         # Check if any single pixel object was misidentified as pattern
        if max_size == 1 and len(objects) > 0:
             # Handle edge case where the 'largest' object is size 1
             # In this specific task's logic, a size 1 pattern wouldn't replicate
             # Or perhaps the first object found of size 1 becomes the pattern?
             # Let's stick to largest > 1 rule based on examples.
             pass # No pattern > 1 pixel found
        else:
            return output_grid


    # Calculate relative coordinates of the pattern object
    pattern_min_r = pattern_object['min_r']
    pattern_min_c = pattern_object['min_c']
    relative_pattern_coords = set()
    for r, c in pattern_object['coords']:
        relative_pattern_coords.add((r - pattern_min_r, c - pattern_min_c))

    # For each target pixel, copy the pattern
    for target in target_pixels:
        target_color = target['color']
        target_r, target_c = target['loc']

        # Place the colored pattern copy onto the output grid
        for rel_r, rel_c in relative_pattern_coords:
            output_r = target_r + rel_r
            output_c = target_c + rel_c

            # Check bounds before writing
            if 0 <= output_r < rows and 0 <= output_c < cols:
                output_grid[output_r, output_c] = target_color

    return output_grid.tolist() # Convert back to list of lists if necessary for testing framework
