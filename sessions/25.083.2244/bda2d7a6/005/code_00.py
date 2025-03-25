"""
Transforms an input grid by swapping the border color with the most frequent inner color.
The border color of the input becomes the inner color of the output, and the most
frequent inner color of the input becomes the border color of the output. All instances
of these colors are swapped throughout the grid.
"""

import numpy as np

def get_border_color(grid):
    """Gets the border color of the grid (top-left pixel)."""
    return grid[0, 0]

def get_inner_colors(grid):
    """Gets the unique inner colors of the grid."""
    grid = np.array(grid)
    border_color = get_border_color(grid)
    inner_colors = np.unique(grid[1:-1, 1:-1])
    inner_colors = inner_colors[inner_colors != border_color]
    return inner_colors

def get_most_frequent_inner_color(grid):
    """Gets most frequent inner color"""
    inner_colors = get_inner_colors(grid)
    if len(inner_colors) == 0:
        return None
    
    counts = []
    for color in inner_colors:
        counts.append(np.sum(np.array(grid) == color))

    most_frequent_index = np.argmax(counts)
    return inner_colors[most_frequent_index]

def transform(input_grid):
    """Transforms the input grid by swapping border and the most frequent inner color."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Get the border color of the input grid.
    input_border_color = get_border_color(input_grid)

    # Find the most frequent inner color
    most_frequent_inner_color = get_most_frequent_inner_color(input_grid)
    
    if most_frequent_inner_color is None:
      return output_grid.tolist()

    # Swap the colors
    output_grid[input_grid == input_border_color] = most_frequent_inner_color
    output_grid[input_grid == most_frequent_inner_color] = input_border_color
    
    return output_grid.tolist()