"""
1.  **Identify Connected Components:** Find all connected components of green (3) pixels in the input grid.
2.  **Transform Each Component:** For *each* connected component of green pixels, change the *top-leftmost* green pixel to azure (8). The top-leftmost pixel is defined as the pixel with the smallest row index, and among those, the smallest column index.
3. **Output Grid**: All other pixels remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def get_connected_component(grid, start_row, start_col, color):
    """Gets a connected component of a given color starting from a given cell."""
    rows, cols = grid.shape
    component = []
    visited = set()
    queue = [(start_row, start_col)]

    while queue:
        row, col = queue.pop(0)
        if (row, col) in visited or grid[row, col] != color:
            continue
        visited.add((row, col))
        component.append((row, col))
        neighbors = get_neighbors(grid, row, col)
        for neighbor_row, neighbor_col in neighbors:
            queue.append((neighbor_row, neighbor_col))
    return component

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = set()

    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 3 and (row, col) not in visited:
                # Get the connected component
                component = get_connected_component(input_grid, row, col, 3)
                visited.update(component)

                # Find the top-leftmost pixel
                top_leftmost_pixel = min(component, key=lambda p: (p[0], p[1]))

                # Change the top-leftmost pixel to azure
                output_grid[top_leftmost_pixel] = 8

    return output_grid