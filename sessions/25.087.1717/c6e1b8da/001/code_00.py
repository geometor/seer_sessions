import numpy as np
import copy

"""
Identify each white pixel in the input grid.
For each white pixel, examine its 8 neighbors (including diagonals).
Collect the colors of all non-white neighbors.
If there is exactly one unique non-white neighbor color, change the white pixel in the output grid to that unique color.
If there are zero non-white neighbors or more than one unique non-white neighbor color, the pixel remains white.
Pixels that are not white in the input grid retain their original color in the output grid.
"""

def get_neighbors(grid, r, c):
    """Gets the values of the 8 neighbors of a cell."""
    neighbors = []
    height, width = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append(grid[nr, nc])
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid based on neighbor rules for white pixels.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = copy.deepcopy(input_grid)
    height, width = input_grid.shape

    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white (0)
            if input_grid[r, c] == 0:
                # Get the colors of its neighbors
                neighbors = get_neighbors(input_grid, r, c)
                
                # Filter out white neighbors and find unique non-white neighbor colors
                non_white_neighbors = set(n for n in neighbors if n != 0)
                
                # If there is exactly one unique non-white neighbor color
                if len(non_white_neighbors) == 1:
                    # Change the corresponding pixel in the output grid to that color
                    output_grid[r, c] = list(non_white_neighbors)[0]
            # If the pixel is not white, it remains unchanged (already copied)

    return output_grid