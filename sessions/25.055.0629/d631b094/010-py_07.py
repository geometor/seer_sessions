"""
Identifies the most frequent color in the input grid (excluding white) and creates a 1xN output grid filled with that color, where N is the count of the most frequent color.
"""

import numpy as np

def get_dominant_color(grid):
    # Count the occurrences of each color (0-9)
    color_counts = np.bincount(grid.flatten(), minlength=10)
    
    # Set the count of white (0) to 0, to ignore it
    color_counts[0] = 0
    
    # Find the color with the maximum count
    dominant_color = np.argmax(color_counts)
    
    return dominant_color

def transform(input_grid):
    # Find the most frequent color in the input grid (excluding white).
    dominant_color = get_dominant_color(input_grid)

    # Count the number of pixels of the dominant color.
    dominant_color_count = np.count_nonzero(input_grid == dominant_color)

    # Create a new 1 x N grid, where N is the count of the dominant color.
    output_grid = np.full((1, dominant_color_count), dominant_color)

    return output_grid