"""
1.  **Identify Background:** Determine the background color, potentially by finding the most frequent color or a color in a corner.
2.  **Identify Objects:** Find all contiguous regions (objects) that are *not* the background color.
3.  **Find Two Most Prominent Colors:** Among the non-background pixels, identify the two colors that appear most frequently.
4.  **Color Swap:** Replace all pixels of the first prominent color with the second prominent color, and vice-versa.
5.  **Leave Background Unchanged:** Ensure the background pixels are not modified.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    # Check corners first, then most frequent
    corners = [grid[0, 0], grid[0, -1], grid[-1, 0], grid[-1, -1]]
    corner_counts = Counter(corners)
    most_common_corner = corner_counts.most_common(1)
    if most_common_corner:
        return most_common_corner[0][0]
    
    # else return most frequent overall
    all_colors = grid.flatten().tolist()
    color_counts = Counter(all_colors)
    return color_counts.most_common(1)[0][0]

def find_objects(grid, background_color):
    # Use a flood-fill algorithm to find contiguous regions
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def flood_fill(row, col, color, current_object):
        if (row < 0 or row >= grid.shape[0] or
            col < 0 or col >= grid.shape[1] or
            visited[row, col] or grid[row, col] != color):
            return

        visited[row, col] = True
        current_object.append((row, col))

        flood_fill(row + 1, col, color, current_object)
        flood_fill(row - 1, col, color, current_object)
        flood_fill(row, col + 1, color, current_object)
        flood_fill(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != background_color:
                current_object = []
                flood_fill(row, col, grid[row, col], current_object)
                objects.append(current_object)

    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Identify Background
    background_color = get_background_color(output_grid)

    # Identify Objects
    objects = find_objects(output_grid, background_color)

    # Find Two Most Prominent Colors
    non_background_pixels = [output_grid[row, col] for obj in objects for row, col in obj]
    color_counts = Counter(non_background_pixels)
    
    if len(color_counts) < 2:
      return output_grid

    most_common_colors = color_counts.most_common(2)
    color1 = most_common_colors[0][0]
    color2 = most_common_colors[1][0]    

    # Color Swap
    for row in range(output_grid.shape[0]):
        for col in range(output_grid.shape[1]):
            if output_grid[row, col] == color1:
                output_grid[row, col] = color2
            elif output_grid[row, col] == color2:
                output_grid[row, col] = color1

    return output_grid