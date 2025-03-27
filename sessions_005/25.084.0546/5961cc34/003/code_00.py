"""
1.  **Identify Input Signals:** Locate all contiguous blocks of pixels that are blue (1), green (3), or yellow(4).

2.  **Identify Targets:** Locate all red (2) pixels.

3.  **Background:** Azure (8) pixels act as the background.

4.  **Transformation:**
    - Iterate through each object found in the input grid that is a color other than azure (8) or red (2).
    - Change the color of these objects to red (2).
    -  Expand the red color: If any red pixel (original or newly transformed) is orthogonally adjacent to an azure (8) pixel, change the azure pixel to red. Repeat this expansion until no more azure pixels are adjacent to red pixels.

5.  **Output:** Construct the output grid with the transformed red objects and the expanded red pixels. All remaining pixels are filled with azure (8).
"""

import numpy as np

def find_objects(grid):
    # Find contiguous regions of the same color, excluding azure (8)
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

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
            if not visited[row, col] and grid[row, col] != 8:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if obj_coords:
                    objects.append((color, obj_coords))
    return objects

def expand_red(grid):
    # Expand red pixels orthogonally to adjacent azure pixels
    rows, cols = grid.shape
    new_grid = grid.copy()
    changed = True

    while changed:
        changed = False
        temp_grid = new_grid.copy()
        for row in range(rows):
            for col in range(cols):
                if temp_grid[row, col] == 8:  # If azure
                    # Check orthogonal neighbors
                    neighbors = []
                    if row > 0:
                        neighbors.append(temp_grid[row - 1, col])
                    if row < rows - 1:
                        neighbors.append(temp_grid[row + 1, col])
                    if col > 0:
                        neighbors.append(temp_grid[row, col - 1])
                    if col < cols - 1:
                        neighbors.append(temp_grid[row, col + 1])

                    if 2 in neighbors:  # If any neighbor is red
                        new_grid[row, col] = 2
                        changed = True
    return new_grid

def transform(input_grid):
    # Initialize output_grid with azure
    output_grid = np.full(input_grid.shape, 8, dtype=int)

    # Find objects, excluding azure (8)
    objects = find_objects(input_grid)

    # Transform non-red objects to red and place in output
    for color, coords in objects:
        if color != 2:  # If the object is not already red
            for row, col in coords:
                output_grid[row, col] = 2  # convert object to red
        else:  # original red objects
            for row, col in coords:
               output_grid[row, col] = 2   # keep it red

    # Expand red pixels
    output_grid = expand_red(output_grid)

    return output_grid