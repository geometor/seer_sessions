"""
1.  **Identify** all contiguous blocks (objects) of green (3) pixels in the input grid where the row number is less than or equal to 4.
2.  **Identify** the contiguous block of red (2) pixels.
3. **Preserve** and do not move the red region.
4.  **Create** a new horizontal block of azure (8) pixels across the entire width of row 10.
5.  **Move** the green objects to directly below the azure row, maintaining their original shapes and relative positions to each other. The green objects stack directly below the azure line.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of a specific color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return

        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find green objects
    green_objects = find_objects(input_grid, 3)

    # Find red object
    red_objects = find_objects(input_grid, 2)

    # Create azure row
    output_grid[10, :] = 8

    # Move green objects down, only if they are in the top section (row <= 4)
    row_offset = 11  # Start placing green objects at row 11 (directly below azure)
    for obj in green_objects:
        # Determine if the object is in the top section
        top_section = all(row <= 4 for row, _ in obj)

        if top_section:
            min_row = min(row for row, _ in obj)
            for row, col in obj:
                new_row = row_offset + (row - min_row)
                output_grid[new_row, col] = 3
            #update the row offset based on height of this green object
            row_offset += max(row for row, _ in obj) - min(row for row, _ in obj) + 1

    # Keep the red region where it is
    for obj in red_objects:
        for row, col in obj:
            output_grid[row, col] = 2

    return output_grid