"""
Counts the occurrences of azure (8), red (2), yellow (4), and green (3) pixels in the input grid.
Creates a 1xN grid where N is the sum of the counts of these colors. The output grid is then populated
with the identified colors in the same order and counts as they appear in the targeted colors list.
"""

import numpy as np

def count_specific_colors(grid):
    # Define the colors to count.
    colors_to_count = [8, 2, 4, 3]  # Azure, Red, Yellow, Green
    counts = {}
    for color in colors_to_count:
        counts[color] = np.sum(grid == color)
    return counts

def transform(input_grid):
    # Count the occurrences of the specific colors.
    color_counts = count_specific_colors(input_grid)

    # Calculate the total width of the output grid.
    total_width = sum(color_counts.values())

    # Create a 1xN output grid filled with zeros (or any default value).
    output_grid = np.zeros((1, total_width), dtype=int)

    # Populate the output grid with the specific colors.
    current_index = 0
    for color in [8, 2, 4, 3]: # Maintain specified color order
        count = color_counts[color]
        if count > 0:
            output_grid[0, current_index:current_index + count] = color
            current_index += count

    return output_grid