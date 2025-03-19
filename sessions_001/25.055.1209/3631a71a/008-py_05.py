"""
1.  **Identify** all pixels with the value '9' (maroon).
2.  **Remove** every pixel of value '9'. In effect, replace those pixels with one of the surrounding colors. Where the '9' value is present, it forms a cluster of one or more pixels. This region is replaced, using a majority color logic from its surroundings to fill the region where value '9' previously occupied.
"""

import numpy as np
from collections import Counter

def get_neighbors(grid, row, col):
    """Gets the valid neighbor coordinates and values for a given cell."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j, grid[i, j]))
    return neighbors

def most_common_neighbor_color(grid, row, col):
    """Finds the most common color among the neighbors, excluding color 9."""
    neighbors = get_neighbors(grid, row, col)
    neighbor_colors = [color for r, c, color in neighbors if color != 9]
    if not neighbor_colors:
        return 0  # Default to 0 if no neighbors other than 9
    most_common = Counter(neighbor_colors).most_common(1)
    return most_common[0][0]

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify pixels with the value '9'
    nine_pixels = []
    for i in range(rows):
        for j in range(cols):
          if input_grid[i,j] == 9:
            nine_pixels.append((i,j))

    # Iterate over '9' pixels and replace them
    for row, col in nine_pixels:
        # find the most common neighboring color (excluding 9)
        replacement_color = most_common_neighbor_color(input_grid, row, col)
        output_grid[row, col] = replacement_color

    return output_grid