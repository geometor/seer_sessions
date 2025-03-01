"""
1.  **Border Preservation and Gap Filling:**
    *   Identify any gaps in the border. A gap is defined as a border position where the pixel color is different from the *most frequent* color along the entire border.
    *   Fill any border gaps with the most frequent border color.

2.  **Clear Interior Pixels:**
    *   Set all non-border pixels to color 0 (white).

3. **Place new pixel**
    *   If any gaps were filled, do not place a new pixel.
    *   If no gaps were filled, place one new pixel of the same color as the top left border pixel.
    *   The location is at row=2, column=1.
"""

import numpy as np
from collections import Counter

def get_border_pixels(grid):
    """Returns a list of border pixel coordinates."""
    rows, cols = grid.shape
    border = []
    for i in range(rows):
        border.extend([(i, 0), (i, cols - 1)])
    for j in range(1,cols-1):
        border.extend([(0, j), (rows - 1, j)])
    return list(set(border))  # Remove duplicates

def get_most_frequent_border_color(grid):
    """Finds the most frequent color along the border."""
    border_pixels = get_border_pixels(grid)
    border_colors = [grid[r, c] for r, c in border_pixels]
    color_counts = Counter(border_colors)
    most_frequent_color = color_counts.most_common(1)[0][0]
    return most_frequent_color

def fill_border_gaps(grid):
    """Fills gaps in the border with the most frequent border color.
       Returns a tuple (new_grid, gaps_filled)
    """
    most_frequent_color = get_most_frequent_border_color(grid)
    border_pixels = get_border_pixels(grid)
    gaps_filled = False
    new_grid = np.copy(grid)

    for r, c in border_pixels:
        if new_grid[r, c] != most_frequent_color:
            new_grid[r, c] = most_frequent_color
            gaps_filled = True
    return new_grid, gaps_filled
def transform(input_grid):
    # Initialize output_grid by filling border gaps
    output_grid, gaps_filled = fill_border_gaps(input_grid)
    rows, cols = output_grid.shape

    # Get border pixels *after* gap filling
    border_pixels = get_border_pixels(output_grid)

    # Clear non-border pixels
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in border_pixels:
                output_grid[i, j] = 0

    # Place a new pixel if no gaps were filled
    if not gaps_filled:
        top_left_color = output_grid[0,0]
        if rows > 2: #make sure row 2 exists
          output_grid[2, 1] = top_left_color

    return output_grid