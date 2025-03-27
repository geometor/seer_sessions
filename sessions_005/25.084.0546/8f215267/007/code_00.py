"""
Transforms an input grid by preserving only the largest vertically and horizontally connected component of each non-background color.
The background color is assumed to be the most frequent color in the grid.
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    """
    Finds the most frequent color in the grid, assumed to be the background.
    """
    flat_grid = grid.flatten()
    color_counts = Counter(flat_grid)
    return color_counts.most_common(1)[0][0]

def get_connected_component(grid, r, c, color, visited):
    """
    Performs a depth-first search to find a connected component.
    Returns a set of (row, col) tuples representing the component.
    """
    rows, cols = grid.shape
    if (r, c) in visited or grid[r, c] != color:
        return set()

    visited.add((r, c))
    component = {(r, c)}

    # Explore adjacent cells
    if r > 0:
        component.update(get_connected_component(grid, r - 1, c, color, visited))
    if r < rows - 1:
        component.update(get_connected_component(grid, r + 1, c, color, visited))
    if c > 0:
        component.update(get_connected_component(grid, r, c - 1, color, visited))
    if c < cols - 1:
        component.update(get_connected_component(grid, r, c + 1, color, visited))

    return component

def find_largest_component(grid, color):
    """
    Finds the largest connected component of a given color in the grid.
    """
    rows, cols = grid.shape
    visited = set()
    largest_component = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                component = get_connected_component(grid, r, c, color, visited)
                if len(component) > len(largest_component):
                    largest_component = component

    return largest_component

def transform(input_grid):
    """
    Transforms the input grid by eroding non-background shapes to their largest connected component.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    background_color = find_background_color(input_grid)

    rows, cols = input_grid.shape

    # Create a set of all colors present in the grid
    all_colors = set(input_grid.flatten())

    # For each non-background color, find the largest component
    for color in all_colors:
      if color != background_color:
        largest_component = find_largest_component(input_grid, color)

        #set all pixels of that color to background
        for r in range(rows):
            for c in range(cols):
                if input_grid[r,c] == color:
                    output_grid[r,c] = background_color

        #set largest component pixels back to correct color
        for r, c in largest_component:
            output_grid[r,c] = color


    return output_grid.tolist()