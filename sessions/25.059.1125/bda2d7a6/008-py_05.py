"""
1. Identify Objects:
    - Identify the *outer region*, which constitutes the perimeter pixels of the grid.
    - Identify the *center* as the contiguous block of white (color 0) pixels.
    - Identify the *inner_region*: Locate the inner region by finding the color of pixels directly adjacent to the center region.
2. Remove Center: Remove the central white square.
3. Shift Inwards (Fill): Expand the *inner region*'s color to fill the area previously occupied by the *center*.
4. Blank Boundary: Set all perimeter pixels of the *outer_region* to white (color 0) if they match the color of the *inner_region*.
"""

import numpy as np

def get_inner_region_color(grid):
    # Find the color of the inner region by checking neighbors of the white center
    center_coords = np.argwhere(grid == 0)
    if len(center_coords) == 0:
        return None

    # Consider neighbors of the first center pixel
    center_row, center_col = center_coords[0]
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            row = center_row + dr
            col = center_col + dc
            if 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]:
                neighbors.append(grid[row, col])

    # Filter and return the neighbor color
    inner_colors = [c for c in neighbors if c != 0]
    if len(inner_colors) > 0:
        return inner_colors[0]
    else:
        return None

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)

    # Remove Center
    center_coords = np.argwhere(output_grid == 0)

    # Shift Inwards - Find the color of the adjacent layer to the center
    inner_color = get_inner_region_color(input_grid)

    # Shift inwards - move inner color
    for coord in center_coords:
        if inner_color is not None:
            output_grid[coord[0], coord[1]] = inner_color

    # Blank the perimeter selectively.
    rows, cols = output_grid.shape
    for i in range(rows):
        for j in range(cols):
            if (i == 0 or i == rows - 1 or j == 0 or j == cols - 1) and output_grid[i,j] == inner_color:
                output_grid[i, j] = 0

    return output_grid