"""
The transformation rule identifies a connected blue shape and a single non-blue, non-white pixel.
If the single pixel is within the blue shape, the blue shape's pixels and it's white borders are changed to the single pixel's color.
"""

import numpy as np

def find_connected_shape(grid, color):
    """Finds a connected shape of the specified color."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    shape_pixels = []

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        shape_pixels.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                dfs(r, c)
                return shape_pixels  # Return after finding the first connected shape
    return shape_pixels

def find_single_pixel(grid, excluded_colors):
    """Finds the first single pixel not matching the excluded colors."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] not in excluded_colors:
                return (r, c), grid[r, c]
    return None, None

def get_neighbors(grid, row, col):
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row-1,col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row,col-1))
    if col < cols - 1:
        neighbors.append((row, col+1))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Find the connected blue shape.
    blue_shape_pixels = find_connected_shape(input_grid, 1)

    # Find the single pixel of a different color.
    single_pixel_coords, single_pixel_color = find_single_pixel(input_grid, [0, 1])

    if not blue_shape_pixels or single_pixel_coords is None:
        return output_grid # Handles edge cases of missing shapes

    # Check if the single pixel is within the blue shape.
    if single_pixel_coords in blue_shape_pixels:
        # fill blue shape
        for r, c in blue_shape_pixels:
            output_grid[r, c] = single_pixel_color

        #border fill
        for r,c in blue_shape_pixels:
            neighbors = get_neighbors(input_grid,r,c)
            for nr, nc in neighbors:
                if input_grid[nr,nc] == 0:
                    output_grid[nr,nc] = single_pixel_color

    return output_grid.tolist()