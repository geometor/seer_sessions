"""
1.  **Identify Primary and Secondary Colors:** Determine the most frequent non-zero color in the input grid. This is the "primary color". All other non-zero colors are considered "secondary colors".

2.  **Locate Primary Color Instances:** Find all positions (row, column) where the primary color appears in the *input* grid.

3.  **Mirror Primary Color:** For *each* position (r, c) where the primary color appears in the input, set the cell at (c, r) in the *output* grid to the primary color. Note: this single step replaces placing at (r,c) in the original program.

4. **Output:** The modified grid is the final output.
"""

import numpy as np
from collections import Counter

def get_primary_color(grid):
    """Finds the most frequent non-zero color in the entire grid."""
    colors = Counter(grid.flatten())
    # Filter out the zero color and find the most common
    non_zero_colors = {color: count for color, count in colors.items() if color != 0}
    if not non_zero_colors:
        return 0
    return Counter(non_zero_colors).most_common(1)[0][0]

def find_color_positions(grid, color):
    """Finds all positions (row, col) of a given color in the grid."""
    return [(r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == color]

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.zeros_like(grid)  # Initialize with zeros
    primary_color = get_primary_color(grid)

    # Locate primary color instances in the input grid
    primary_color_positions = find_color_positions(grid, primary_color)

    # Mirror primary color positions to the output grid
    for r, c in primary_color_positions:
        if c < rows and r < cols:
          output_grid[c, r] = primary_color

    return output_grid.tolist()