```python
import numpy as np
from collections import deque

"""
1. Identify the single contiguous block of White (0) pixels.
2. Identify the single contiguous block of Red (2) pixels and its dimensions (height, width).
3. Identify all contiguous blocks of Blue (1) pixels and their dimensions.
4. In the output grid (initially a copy of the input), change the pixels of the original White block to Blue (1).
5. Search for a Blue block whose dimensions exactly match the Red block's dimensions.
6. If such a matching Blue block is found:
    Change the pixels of that specific Blue block to White (0) in the output grid.
7. Else (if no matching Blue block is found):
    Change the pixels of the original Red block to White (0) in the output grid.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (a set of (row, col) tuples) and
              'dims' (a tuple of (height, width)).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start BFS to find a new object
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                height = max_r - min_r + 1
                width = max_c - min_c + 1
                objects.append({'coords': obj_coords, 'dims': (height, width)})

    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the interaction between White, Red, and Blue objects.

    1. Changes the White object to Blue.
    2. Finds the Red object and all Blue objects.
    3. If a Blue object has the same dimensions as the Red object, that Blue object turns White.
    4. Otherwise, the Red object turns White.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find the White (0) object
    white_objects = find_objects(input_grid, 0)
    if not white_objects:
        # Handle cases where there might be no white object, though examples suggest there always is.
        # If necessary, return input_grid or raise error. For now, assume it exists.
        pass # Or maybe return input_grid? Let's assume it's guaranteed by the task structure.
    white_object = white_objects[0] # Assuming exactly one white object

    # 4. Change the White object's pixels to Blue (1) in the output grid
    for r, c in white_object['coords']:
        output_grid[r, c] = 1

    # 2. Find the Red (2) object
    red_objects = find_objects(input_grid, 2)
    if not red_objects:
        # Handle cases where there might be no red object. Assume it exists.
        pass
    red_object = red_objects[0] # Assuming exactly one red object
    red_dims = red_object['dims']
    red_coords = red_object['coords']

    # 3. Find all Blue (1) objects
    blue_objects = find_objects(input_grid, 1)

    # 5. Search for a Blue block with matching dimensions
    matching_blue_object = None
    for blue_obj in blue_objects:
        if blue_obj['dims'] == red_dims:
            matching_blue_object = blue_obj
            break # Found the match

    # 6. & 7. Conditional Transformation
    if matching_blue_object:
        # Change the matching Blue object's pixels to White (0)
        for r, c in matching_blue_object['coords']:
            # Check if this pixel wasn't part of the original white object
            # that we already turned blue. If it was, don't change it back to white.
            # This handles overlaps correctly if the matching blue object
            # happened to overlap the original white object.
            if (r, c) not in white_object['coords']:
                 output_grid[r, c] = 0
            # Note: Based on examples, it seems the rule prioritizes changing the blue
            # object to white, even if it overlaps the original white object location.
            # Let's simplify and just change the blue object pixels to white.
            # Revisit if validation fails.
        # Re-simplification: Change all matched blue pixels to white.
        for r, c in matching_blue_object['coords']:
             output_grid[r, c] = 0
    else:
        # Change the Red object's pixels to White (0)
        for r, c in red_coords:
            output_grid[r, c] = 0

    return output_grid
```