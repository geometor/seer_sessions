# 22233c11 • 020 • refine_coder

---
```python
"""
1.  **Identify Green Objects:** Locate all contiguous groups of green (value 3) pixels. Consider these as distinct objects.
2.  **Copy Green Objects:** Copy all identified green objects to the output grid, maintaining their original positions and shapes.
3.  **Place Azure Pixels (Conditional):** For each green object, examine its edge pixels. An edge pixel is one that is directly adjacent (not diagonally) to a pixel of a different color or to the edge of the grid.
    *   Place an azure pixel (value 8) adjacent to *every* green edge pixel, extending *outward* from the green object. The azure placement will always be in the direction that makes the green pixel an edge pixel:
        *   To the *right* if the green edge pixel can see a non-green pixel or grid edge to its *right*.
        *   To the *left* if the green edge pixel can see a non-green pixel or grid edge to its *left*.
        *   *Above* if the green edge pixel can see a non-green pixel or grid edge *above* it.
        *   *Below* if the green edge pixel can see a non-green pixel or grid edge *below* it.
4.  **Zero Out**: Fill all remaining empty cells in the output_grid with 0.
"""

import numpy as np

def get_objects(grid, color):
    """
    Identifies contiguous objects of a specified color in the grid.
    Returns a list of sets, where each set contains the coordinates of an object's pixels.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def is_valid(row, col, color):
        return 0 <= row < rows and 0 <= col < cols and grid[row, col] == color

    def dfs(row, col, current_object):
        if not is_valid(row, col, color) or visited[row, col]:
            return
        visited[row, col] = True
        current_object.add((row, col))

        # Explore adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == color and not visited[i, j]:
                current_object = set()
                dfs(i, j, current_object)
                objects.append(current_object)
    return objects

def is_edge_pixel(grid, row, col, object_pixels):
    """
    Checks if a pixel is an edge pixel of its object.
    Returns (is_edge, neighbor_coords) where:
        is_edge is True if the pixel is an edge pixel, False otherwise.
        neighbor_coords is a list of (r, c) tuples representing the coordinates of the
                        neighboring cells that cause the pixel to be considered an edge.
    """
    rows, cols = grid.shape
    
    # Check if the pixel is part of the specified object
    if (row, col) not in object_pixels:
        return False, []

    # Check for adjacent pixels of a different color or grid boundary
    neighbors = [
        (row - 1, col),  # Up
        (row + 1, col),  # Down
        (row, col - 1),  # Left
        (row, col + 1),  # Right
    ]

    edge_neighbors = []
    for r, c in neighbors:
        if not (0 <= r < rows and 0 <= c < cols) or (r, c) not in object_pixels:
            edge_neighbors.append((r,c))

    return len(edge_neighbors) > 0, edge_neighbors



def transform(input_grid):
    # Initialize output_grid with zeros
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Identify green objects
    green_objects = get_objects(input_grid, 3)

    # Copy green objects to output_grid
    for obj in green_objects:
        for row, col in obj:
            output_grid[row, col] = 3

    # Place azure pixels conditionally
    for obj in green_objects:
        for row, col in obj:
            is_edge, edge_neighbors = is_edge_pixel(input_grid, row, col, obj)
            if is_edge:
                for r, c in edge_neighbors:
                    # Ensure we don't write outside the grid boundaries
                    if 0 <= r < rows and 0 <= c < cols:
                      output_grid[r, c] = 8

    return output_grid
```
