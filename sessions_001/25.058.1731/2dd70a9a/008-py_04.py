"""
1.  Identify azure (8) regions within the grid.
2.  Determine if each azure region is fully enclosed by other colors (not connected to the edge via white pixels). A region is considered "enclosed" if *no* pixel of that region can reach the grid edge via a path of adjacent same-colored pixels.
3. If the azure region is fully enclosed, no changes are made.
4. If not enclosed: Locate green (3) pixels. Expand the green pixels into adjacent white (0) pixels within the non-enclosed azure area.
5.  Iterate the green expansion until no more green pixels can expand into adjacent white pixels.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the row, col coordinates of all pixels of a given color."""
    return np.argwhere(grid == color)

def get_neighbors(grid, row, col):
    """Gets the valid neighbors (up, down, left, right) of a pixel."""
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

def is_fully_enclosed(grid, azure_pixels):
    """
    Checks if an azure region is fully enclosed using a flood-fill approach.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    
    # Create a queue for the flood fill, starting with edge pixels that are not azure
    queue = []
    for r in range(rows):
        for c in [0, cols - 1]:  # Left and right edges
            if grid[r,c] != 8 and not visited[r,c]:
              queue.append((r, c))
              visited[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]: # Top and Bottom Edges
            if grid[r,c] != 8 and not visited[r,c]:
                queue.append((r,c))
                visited[r,c] = True

    # Perform flood fill
    while queue:
        r, c = queue.pop(0)
        neighbors = get_neighbors(grid, r, c)
        for nr, nc in neighbors:
            if not visited[nr, nc] and grid[nr,nc] != 8:
                visited[nr, nc] = True
                queue.append((nr, nc))

    # Check if any azure pixel is reachable from the edge (i.e., not enclosed)
    for r, c in azure_pixels:
        if visited[r,c]:
            return False  # Not fully enclosed

    return True  # Fully enclosed


def transform(input_grid):
    """Transforms the input grid according to the expansion rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure pixels
    azure_pixels = find_pixels_by_color(output_grid, 8)

    # Determine if the azure region is fully enclosed
    if is_fully_enclosed(output_grid, azure_pixels):
        return output_grid # no changes if enclosed

    green_pixels = find_pixels_by_color(output_grid, 3)
    if len(green_pixels) == 0:
      return output_grid

    while True:
        new_green_pixels = []
        pixels_to_change = []

        for r, c in green_pixels:
            neighbors = get_neighbors(output_grid, r, c)
            for nr, nc in neighbors:
                if output_grid[nr, nc] == 0:
                    pixels_to_change.append( (nr,nc) )

        if len(pixels_to_change) == 0:
            break;

        for (r,c) in pixels_to_change:
            output_grid[r,c] = 3
            new_green_pixels.append( (r, c) )

        green_pixels = new_green_pixels


    return output_grid