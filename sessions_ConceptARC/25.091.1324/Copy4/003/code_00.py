import numpy as np
from collections import deque

"""
Transforms an input grid by the following process:
1. Identify all distinct connected objects for each non-background color.
2. For each color with multiple objects, designate the largest object (by pixel count, tie-breaking with top-left reading order) as the 'prototype'.
3. Extract the rectangular pattern within the bounding box of the prototype from the original input grid.
4. Identify 'seed' objects: these are any objects of the same color as the prototype, but not the prototype itself.
5. Check each seed object: if it is exactly 1x1 pixel in size AND its top-left corner is positioned *after* the prototype's top-left corner in reading order (row-major), then replace it.
6. Replacement involves pasting the extracted prototype pattern onto the grid, aligning the pattern's top-left corner with the seed object's (which is just the single pixel).
7. Objects that are unique for their color, prototypes themselves, or seeds that do not meet the replacement criteria (not 1x1 or not positioned after the prototype) are left unchanged.
"""

def find_objects(grid, color):
    """
    Finds all connected components of a given color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color to search for.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'pixels' (set of (r, c) tuples), 'min_r', 'min_c',
              'max_r', 'max_c', 'size', 'top_left' (tuple (min_r, min_c)),
              and 'is_1x1' (boolean). Returns an empty list if no objects of the
              color are found.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                # Start BFS to find a connected component
                component_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                
                while q:
                    row, col = q.popleft()
                    component_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)
                    
                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if component_pixels:
                    obj_size = len(component_pixels)
                    objects.append({
                        'pixels': component_pixels,
                        'min_r': min_r,
                        'min_c': min_c,
                        'max_r': max_r,
                        'max_c': max_c,
                        'size': obj_size,
                        'top_left': (min_r, min_c),
                        'is_1x1': obj_size == 1
                    })
                    
    return objects

def get_pattern(grid, bbox):
    """
    Extracts a rectangular pattern from the grid based on the bounding box.

    Args:
        grid (np.array): The grid to extract from.
        bbox (dict): Dictionary containing 'min_r', 'min_c', 'max_r', 'max_c'.

    Returns:
        np.array: The extracted pattern.
    """
    # Ensure indices are valid before slicing
    min_r, max_r = max(0, bbox['min_r']), min(grid.shape[0], bbox['max_r'] + 1)
    min_c, max_c = max(0, bbox['min_c']), min(grid.shape[1], bbox['max_c'] + 1)
    if min_r >= max_r or min_c >= max_c: # Check for empty slice
        return np.array([[]], dtype=grid.dtype)
    return grid[min_r:max_r, min_c:max_c]


def paste_pattern(grid, pattern, top_left):
    """
    Pastes a pattern onto the grid at the specified top-left position.
    Handles boundary conditions by clipping.

    Args:
        grid (np.array): The target grid (mutable).
        pattern (np.array): The pattern to paste.
        top_left (tuple): The (row, column) to start pasting at.
    """
    start_r, start_c = top_left
    if pattern.size == 0: # Handle empty pattern
        return
        
    pattern_h, pattern_w = pattern.shape
    grid_h, grid_w = grid.shape

    # Calculate the actual region to paste onto, clipping to grid boundaries
    end_r = min(start_r + pattern_h, grid_h)
    end_c = min(start_c + pattern_w, grid_w)

    # Calculate the portion of the pattern to use based on clipping
    # Adjust pattern slice end indices based on how much was clipped
    paste_h = end_r - start_r
    paste_w = end_c - start_c

    # Ensure we don't try to paste negative or zero dimensions after clipping
    if paste_h <= 0 or paste_w <= 0:
        return

    # Paste the valid (potentially clipped) portion of the pattern
    grid[start_r:end_r, start_c:end_c] = pattern[0:paste_h, 0:paste_w]


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Find unique colors present, excluding background (0)
    unique_colors = np.unique(input_np)
    unique_colors = unique_colors[unique_colors != 0]

    # Process each color
    for color in unique_colors:
        # Find all distinct connected components (objects) of the current color
        objects = find_objects(input_np, color)

        # Skip if only one or zero objects of this color exist (no prototype/seed distinction needed)
        if len(objects) < 2:
            continue

        # Determine the prototype object
        # Sort by size (descending), then by top-left row (ascending), then by top-left col (ascending)
        objects.sort(key=lambda obj: (-obj['size'], obj['top_left'][0], obj['top_left'][1]))
        prototype = objects[0]
        proto_r, proto_c = prototype['top_left']

        # Extract the pattern from the prototype's bounding box in the *original* input grid
        pattern_to_copy = get_pattern(input_np, prototype)
        
        # Iterate through all other components (seeds) of the same color
        for i in range(1, len(objects)):
            seed = objects[i]
            seed_r, seed_c = seed['top_left']

            # Check the replacement conditions:
            # 1. Is the seed object exactly 1x1 pixel?
            is_1x1 = seed['is_1x1']
            # 2. Is the seed positioned after the prototype in reading order?
            is_after_prototype = seed_r > proto_r or (seed_r == proto_r and seed_c > proto_c)

            # If both conditions are met, replace the seed
            if is_1x1 and is_after_prototype:
                # Paste the prototype's pattern onto the output grid, starting at the seed's top-left corner
                paste_pattern(output_np, pattern_to_copy, seed['top_left'])

    # Convert the result back to a list of lists for the expected output format
    return output_np.tolist()