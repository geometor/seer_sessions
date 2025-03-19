"""
1.  **Identify Target Colors:** Find all pixels with colors orange (7), azure (8), yellow (4), and magenta (6) within the input grid.
2.  **Select Target Pixels**: Select the *first* occurrences of these colors when scanning the grid row by row, from left to right, and top to bottom.
3.  **Construct Output Grid:** Create a 2x2 output grid.
4.  **Populate Output Grid:** Fill the 2x2 grid with the selected pixels, *row by row*. The order of selection (based on the row-by-row scan) determines the placement in the output grid.
"""

import numpy as np

def find_first_occurrences(grid, target_colors):
    """Finds the first occurrences of target colors in a row-by-row scan."""
    rows, cols = grid.shape
    selected_pixels = []
    found_colors = set()

    for i in range(rows):
        for j in range(cols):
            color = grid[i, j]
            if color in target_colors and color not in found_colors:
                selected_pixels.append(color)
                found_colors.add(color)
            if len(found_colors) == len(target_colors): # all found
                return selected_pixels
    return selected_pixels


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((2, 2), dtype=int)

    # Identify and select target pixels (first occurrences).
    target_colors = [7, 8, 4, 6]
    selected_pixels = find_first_occurrences(input_grid, target_colors)
    
    # Populate the output grid.
    if len(selected_pixels) == 4:
      output_grid = np.array(selected_pixels).reshape(2, 2)

    return output_grid