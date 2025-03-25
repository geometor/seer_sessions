"""
The input 3x3 grid is transformed into a 3x3 output grid. Examine the input and
find the color counts for each color present. Then find the value of the center
cell. If value of the center cell has the highest count, then create the output
grid filled with the center value. Otherwise, create an output grid filled with
the most frequent value.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the color counts
    unique_colors, counts = np.unique(input_grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    # Find the most frequent color and its count
    most_frequent_color = unique_colors[np.argmax(counts)]
    max_count = np.max(counts)

    # Find the center value
    center_value = input_grid[1, 1]

    # Check if center value has the highest count
    if center_value in color_counts and color_counts[center_value] == max_count:
        fill_color = center_value
    else:
        fill_color = most_frequent_color

    # Fill the output grid
    output_grid[:] = fill_color

    return output_grid