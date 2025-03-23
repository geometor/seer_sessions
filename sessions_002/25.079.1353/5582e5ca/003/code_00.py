"""
The output grid is filled entirely with the most frequent color in the input grid.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    # Flatten the input grid to easily count color occurrences.
    flat_grid = input_grid.flatten()

    # Count the occurrences of each color.
    color_counts = Counter(flat_grid)

    # Find the most frequent color.
    most_frequent_color = color_counts.most_common(1)[0][0]

    # Create an output grid of the same size, filled with the most frequent color.
    output_grid = np.full(input_grid.shape, most_frequent_color)

    return output_grid