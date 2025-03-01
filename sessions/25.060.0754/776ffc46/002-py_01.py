"""
The transformation rule involves identifying objects (contiguous blocks of pixels of the same color) within the input grid, and, for each, check if the color is blue and replace it with another shape's color.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all contiguous objects in the grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A list of objects, where each object is a dictionary containing:
          - 'color': The color of the object.
          - 'pixels': A list of (row, col) tuples representing the pixel coordinates.
          - 'shape': plus or rectangle
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def get_neighbors(r, c):
        neighbors = []
        if r > 0:
            neighbors.append((r - 1, c))  # Up
        if r < rows - 1:
            neighbors.append((r + 1, c))  # Down
        if c > 0:
            neighbors.append((r, c - 1))  # Left
        if c < cols - 1:
            neighbors.append((r, c + 1))  # Right
        return neighbors

    def dfs(row, col, color, pixels):
        if (row, col) in visited or grid[row, col] != color:
            return
        visited.add((row, col))
        pixels.append((row, col))
        for neighbor_row, neighbor_col in get_neighbors(row, col):
            dfs(neighbor_row, neighbor_col, color, pixels)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                pixels = []
                dfs(row, col, color, pixels)
                
                # Determine shape
                if len(pixels) > 1 :
                    min_row = min(p[0] for p in pixels)
                    max_row = max(p[0] for p in pixels)
                    min_col = min(p[1] for p in pixels)
                    max_col = max(p[1] for p in pixels)

                    height = max_row - min_row + 1
                    width = max_col - min_col + 1

                    if height * width == len(pixels):
                       shape = "rectangle"
                    elif (len(pixels) - 1) % 4 == 0 :
                        shape = "plus" # assumes no degenerate plus shapes
                    
                    objects.append({'color': color, 'pixels': pixels, "shape":shape})
                elif len(pixels) == 1 :
                    objects.append({'color': color, 'pixels': pixels, "shape":"single"})

    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Find objects in input
    objects = find_objects(grid)
    
    
    blue_object = None
    other_object_color = None

    
    for obj in objects:
       if obj['color'] == 1: #blue
          blue_object = obj
       elif obj['color'] != 5 and obj['color'] != 0 and obj['color'] != 1: #not gray or white or blue
            other_object_color = obj['color']
    
    if blue_object is not None and other_object_color is not None:
        for r, c in blue_object['pixels']:
           output_grid[r,c] = other_object_color
    

    return output_grid.tolist()