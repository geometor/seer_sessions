"""
1. Identify all pixels with the color green (value 3).
2. For each green pixel, check its immediate neighbors (up, down, left, right).
3. If a green pixel has a non-green neighbor in the input grid, change the green pixel in the output grid to the color of that neighbor.
4. If a green pixel has multiple different colored non-green neighbors, prioritize: gray (5), then blue (1), then red(2).
5. If a green pixel is only surrounded by other green pixels and/or the edge of the grid, change it to white (0).
"""

import numpy as np

def get_neighbor_colors(grid, r, c):
    """Gets the colors of the immediate neighbors of a pixel."""
    rows, cols = grid.shape
    neighbor_colors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbor_colors.append(grid[nr, nc])
    return neighbor_colors

def transform(input_grid):
    """
    Transforms the input grid by removing green pixels based on their neighbors.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    green_pixels = np.where(input_grid == 3)
    green_coords = list(zip(green_pixels[0], green_pixels[1]))

    for r, c in green_coords:
        neighbor_colors = get_neighbor_colors(input_grid, r, c)
        non_green_neighbors = [color for color in neighbor_colors if color != 3]

        if non_green_neighbors:
            # Prioritize gray, then blue, then red.
            if 5 in non_green_neighbors:
                output_grid[r, c] = 5
            elif 1 in non_green_neighbors:
                output_grid[r, c] = 1
            elif 2 in non_green_neighbors:
                output_grid[r,c] = 2
            else:
                 output_grid[r,c] = 0 # should never happen, based on observation

        else:
            # If no non-green neighbors, change to white.
            output_grid[r, c] = 0

    return output_grid