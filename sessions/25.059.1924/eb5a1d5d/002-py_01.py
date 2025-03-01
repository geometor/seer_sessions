"""
The transformation rule extracts a smaller, central portion of the input grid, focusing on nested colored rectangles. It identifies the background color (most frequent on the edges) and then extracts the central colored region, discarding the background.
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    # Collect all border pixels
    border_pixels = []
    height, width = grid.shape
    for x in range(width):
        border_pixels.append(grid[0, x])
        border_pixels.append(grid[height - 1, x])
    for y in range(1, height - 1):
        border_pixels.append(grid[y, 0])
        border_pixels.append(grid[y, width - 1])

    # Find the most common color
    color_counts = Counter(border_pixels)
    background_color = color_counts.most_common(1)[0][0]
    return background_color

def find_inner_rectangle(grid, background_color):
    # Find the bounding box of the non-background pixels

    rows, cols = np.where(grid != background_color)
    if len(rows) == 0:  # Handle case where there's no content
        return None, None, None, None
    
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Extracts the central colored region from the input grid.
    """
    grid = np.array(input_grid)

    # 1. Identify Background
    background_color = find_background_color(grid)

    # 2 & 3. Find Inner rectangle and content.
    min_row, max_row, min_col, max_col = find_inner_rectangle(grid, background_color)

    if min_row is None:
        return [[]] #return empty grid.

    # 4. Extract Innermost Content
    output_grid = grid[min_row:max_row+1, min_col:max_col+1]

    # 5. Output
    return output_grid.tolist()