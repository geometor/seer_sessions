"""
1.  **Find the Target Pixel:** Identify all single-pixel objects (objects with a size of 1) in the input grid.
2.  **Check for Isolation:** For each single-pixel object, verify that it has no adjacent neighbors of the same color.
3. **Output:** If an isolated single-pixel object is found, output a 1x1 grid containing the color of that pixel. If no such object, output an empty list.
"""

import numpy as np

def find_all_objects(grid):
    # Find all objects (contiguous regions of the same color) in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, coords):
        # Depth-first search to find all connected pixels of the same color.
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        coords.append((row, col))
        dfs(row + 1, col, color, coords)
        dfs(row - 1, col, color, coords)
        dfs(row, col + 1, color, coords)
        dfs(row, col - 1, color, coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                coords = []
                dfs(row, col, grid[row, col], coords)
                if coords:
                    # Calculate bounding box and size for each object
                    min_row, max_row = min(coords, key=lambda x: x[0])[0], max(coords, key=lambda x: x[0])[0]
                    min_col, max_col = min(coords, key=lambda x: x[1])[1], max(coords, key=lambda x: x[1])[1]
                    size = (max_row - min_row + 1) * (max_col - min_col + 1)
                    objects.append({
                        'color': grid[row, col],
                        'coords': coords,
                        'bbox': (min_row, max_row, min_col, max_col),
                        'size': size
                    })
    return objects

def is_isolated(grid, coords, color):
    # Check if a pixel at given coordinates is isolated (no neighbors of the same color).
    row, col = coords[0]
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                if grid[nr, nc] == color:
                    return False  # Found a neighbor of the same color
    return True

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find all objects in the input grid.
    objects = find_all_objects(input_grid)

    # Find single-pixel objects.
    single_pixels = [obj for obj in objects if obj['size'] == 1]

    # Check for isolation and output the color if found.
    for pixel in single_pixels:
        if is_isolated(input_grid, pixel['coords'], pixel['color']):
            return [[pixel['color']]]

    return []