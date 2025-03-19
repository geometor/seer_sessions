"""
Determine the output color by identifying the most frequent color on the perimeter of the input grid. If there's a tie on the perimeter, prioritize colors that appear in the corners. If a corner color is present among the tied perimeter colors, select it. Otherwise, choose the color with the highest overall count in the grid.
"""

import numpy as np

def get_perimeter_colors(grid):
    """Extracts colors from the perimeter of the grid."""
    perimeter = []
    rows, cols = grid.shape
    perimeter.extend(grid[0, :])  # Top row
    perimeter.extend(grid[rows - 1, :])  # Bottom row
    perimeter.extend(grid[1:rows - 1, 0])  # Left column (excluding corners)
    perimeter.extend(grid[1:rows - 1, cols - 1])  # Right column (excluding corners)
    return perimeter

def count_occurrences(grid, color):
    """Counts the number of times a color appears in the grid."""
    return np.sum(grid == color)

def get_corner_colors(grid):
    """Returns a list of the colors at the four corners of the grid."""
    rows, cols = grid.shape
    return [grid[0, 0], grid[0, cols - 1], grid[rows - 1, 0], grid[rows - 1, cols - 1]]


def transform(input_grid):
    """Transforms the input grid to the output grid based on the described rule."""
    perimeter_colors = get_perimeter_colors(input_grid)
    unique_perimeter_colors = list(set(perimeter_colors))
    
    color_counts = {}
    for color in unique_perimeter_colors:
        color_counts[color] = perimeter_colors.count(color)

    max_count = max(color_counts.values())
    most_frequent_perimeter_colors = [color for color, count in color_counts.items() if count == max_count]

    if len(most_frequent_perimeter_colors) == 1:
        output_color = most_frequent_perimeter_colors[0]
    else:
        # Tiebreaker: Check for corner colors
        corner_colors = get_corner_colors(input_grid)
        corner_color_present = None
        for color in most_frequent_perimeter_colors:
            if color in corner_colors:
                corner_color_present = color
                break

        if corner_color_present is not None:
            output_color = corner_color_present
        else:
            # If no corner color is present, use overall count
            overall_counts = {}
            for color in most_frequent_perimeter_colors:
                overall_counts[color] = count_occurrences(input_grid, color)
            
            max_overall_count = max(overall_counts.values())
            output_color = [color for color, count in overall_counts.items() if count == max_overall_count][0]

    output_grid = np.array([[output_color]])
    return output_grid