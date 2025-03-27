"""
Replaces gray (5) colored rectangular regions in the input grid with rectangular regions of other colors, 
maintaining the size and position of the original gray regions. The replacement color is determined by the most
frequent color adjacent to the grey shape, including diagonally adjacent colors. If a gray region has no
adjacent non-gray colors, it remains gray.
"""

import numpy as np
from collections import Counter

def find_objects(grid):
    """
    Finds connected regions (objects) of the same color in the grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A list of objects, where each object is a dictionary containing:
        - color: The color of the object.
        - pixels: A list of (row, col) tuples representing the pixels belonging to the object.
    """
    objects = []
    visited = set()

    def dfs(row, col, color, pixels):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        pixels.append((row, col))
        dfs(row + 1, col, color, pixels)
        dfs(row - 1, col, color, pixels)
        dfs(row, col + 1, color, pixels)
        dfs(row, col - 1, color, pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                color = grid[row, col]
                pixels = []
                dfs(row, col, color, pixels)
                if pixels:
                    objects.append({"color": color, "pixels": pixels})
    return objects

def get_object_bounds(pixels):
    """
    Finds min and max bounds

    Args:
      pixels: list of pixels
    """
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)

    return min_row, max_row, min_col, max_col

def get_adjacent_colors(grid, pixels):
    """
    Gets the colors adjacent to the given pixels, including diagonals.
    """
    adjacent_colors = []
    rows, cols = grid.shape
    checked_neighbors = set()  # Keep track of checked neighbors to avoid duplicates

    for r, c in pixels:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # Skip the current pixel
                neighbor_row, neighbor_col = r + i, c + j
                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    if (neighbor_row, neighbor_col) not in checked_neighbors:
                        adjacent_colors.append(grid[neighbor_row, neighbor_col])
                        checked_neighbors.add((neighbor_row,neighbor_col))

    return adjacent_colors



def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    for obj in objects:
        if obj["color"] == 5:  # gray objects
            # Get gray object boundaries.
            min_row, max_row, min_col, max_col = get_object_bounds(obj["pixels"])

            # Find replacement color using adjacent colors (including diagonals).
            adjacent_colors = get_adjacent_colors(input_grid, obj["pixels"])
            
            # count and get most frequent color, excluding grey
            color_counts = Counter(adjacent_colors)
            if 5 in color_counts:
                del color_counts[5] # don't copy grey
            
            if color_counts:
                replacement_color = color_counts.most_common(1)[0][0]
            else:
                replacement_color = 5  # default to grey if no other neighbors

            # replace the gray area with the replacement color
            for row in range(min_row, max_row + 1):
              for col in range(min_col, max_col + 1):
                output_grid[row,col] = replacement_color

    return output_grid