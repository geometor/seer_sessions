"""
This module transforms an input grid into an output grid of the same dimensions.
The output grid is filled entirely with a single color. This color is determined
by finding the color that appears most frequently in the input grid. If there is
a tie for the most frequent color, the color with the highest numerical value
among the tied colors is chosen as the fill color for the output grid.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Transforms the input grid based on color frequency analysis.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input grid to a numpy array for easier manipulation
    grid = np.array(input_grid)
    height, width = grid.shape

    # Flatten the grid to easily count color occurrences
    flat_grid = grid.flatten()

    # Count the frequency of each color
    color_counts = Counter(flat_grid)

    # If there are no colors (empty grid, though unlikely in ARC), return an empty grid of same shape
    if not color_counts:
        return np.zeros((height, width), dtype=int)

    # Find the maximum frequency
    max_frequency = 0
    for color, count in color_counts.items():
        if count > max_frequency:
            max_frequency = count

    # Identify all colors that have this maximum frequency
    most_frequent_colors = []
    for color, count in color_counts.items():
        if count == max_frequency:
            most_frequent_colors.append(color)

    # Resolve ties: select the color with the largest numerical value
    dominant_color = max(most_frequent_colors)

    # Create the output grid with the same dimensions as the input
    output_grid = np.zeros((height, width), dtype=int)

    # Fill the output grid with the dominant color
    output_grid.fill(dominant_color)

    return output_grid
