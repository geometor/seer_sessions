```python
"""
1.  **Identify Objects:** Locate all contiguous blocks of pixels of the same color, considering azure (8) as the background and excluding it from object identification.

2.  **Initial Red Pixels:** Identify all pixels that are initially red (2) in the input grid.

3.  **Transform Non-Red Objects:** Change the color of all objects that are not initially red (2) to red (2).

4.  **Iterative Red Expansion:**
    - Create a set of 'active' red pixels, initially containing only the originally red pixels.
    - Iterate:
        - Find all azure (8) pixels that are orthogonally adjacent to the 'active' red pixels.
        - Change these adjacent azure pixels to red (2).
        - Add the newly changed red pixels to a 'newly_active' set.
        - If no azure pixels were changed in this iteration, stop.
        - Otherwise, update the 'active' pixels to be the 'newly_active' pixels, and repeat.

5.  **Output:** Construct the output grid, combining all red pixels (original, transformed, and expanded).
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of the same color, excluding a specified background color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape
    background_color = 8

    def dfs(row, col, color, obj_coords):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col] and grid[row, col] != background_color:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if obj_coords:
                    objects.append((color, obj_coords))
    return objects

def find_initial_red_pixels(grid):
    """Finds the coordinates of all pixels that are initially red (2)."""
    red_pixels = []
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 2:
                red_pixels.append((row, col))
    return red_pixels

def iterative_red_expansion(grid, initial_red_pixels):
    """Expands red pixels iteratively to adjacent azure pixels."""
    rows, cols = grid.shape
    output_grid = grid.copy()
    active_red_pixels = set(initial_red_pixels)
    background_color = 8
    red_color = 2

    while active_red_pixels:
        newly_active_pixels = set()
        for row, col in active_red_pixels:
            output_grid[row, col] = red_color  # Ensure current active pixels are red

            # Check orthogonal neighbors
            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            for nr, nc in neighbors:
                if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == background_color:
                    output_grid[nr, nc] = red_color
                    newly_active_pixels.add((nr, nc))
        active_red_pixels = newly_active_pixels

    return output_grid


def transform(input_grid):
    # Find objects, excluding azure (8)
    objects = find_objects(input_grid)

    # Find initial red pixels
    initial_red_pixels = find_initial_red_pixels(input_grid)
    
    # Initialize output_grid with azure
    output_grid = np.full(input_grid.shape, 8, dtype=int)
    
    #place initial red pixels into the output
    for r,c in initial_red_pixels:
        output_grid[r,c] = 2

    # Transform non-red objects to red
    for color, coords in objects:
        if color != 2:  # If the object is not initially red
            for row, col in coords:
                output_grid[row,col] = 2 #change the objects that were not originally red, to red
                
    # Expand red pixels iteratively
    output_grid = iterative_red_expansion(output_grid, initial_red_pixels)

    return output_grid
```