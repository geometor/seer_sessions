"""
Counts the number of distinct objects in the input grid.  An object is a contiguous region of pixels of the same color.
The output grid is a 1x1 grid containing the most frequent color in the input.
"""

import numpy as np
from collections import Counter

def count_objects(grid):
    """Counts contiguous regions of the same color as distinct objects."""
    visited = set()
    count = 0
    color_counts = Counter()

    def explore(r, c, color):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        explore(r + 1, c, color)
        explore(r - 1, c, color)
        explore(r, c + 1, color)
        explore(r, c - 1, color)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r, c) not in visited:
                color = grid[r, c]
                explore(r, c, color)
                count += 1
                color_counts[color] +=1

    most_common_color = color_counts.most_common(1)[0][0] if color_counts else 0

    return count, most_common_color

def transform(input_grid):
    # Count objects and find most frequent color
    _, most_common_color = count_objects(input_grid)

    # Create 1x1 output grid with most common color
    output_grid = np.array([[most_common_color]])

    return output_grid