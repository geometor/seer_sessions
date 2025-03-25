"""
The output grid is a 3x3 grid where every cell is filled with a single color.
The color to use is the most frequent color from the input grid.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Transforms the input grid into a 3x3 output grid filled with the most frequent color from the input.
    """
    # Flatten the input grid to easily count color frequencies.
    flattened_grid = input_grid.flatten()

    # Count the frequency of each color.
    color_counts = Counter(flattened_grid)

    # Find the most frequent color.
    most_frequent_color = color_counts.most_common(1)[0][0]

    # Create a new 3x3 grid filled with the most frequent color.
    output_grid = np.full((3, 3), most_frequent_color)

    return output_grid