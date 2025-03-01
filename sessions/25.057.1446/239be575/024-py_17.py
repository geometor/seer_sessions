"""
The input grid is reduced to a single pixel. The output pixel's color is the most frequent color in the input grid.  If there's more than one color, use the one that occurs most.  If all are equal, use what is present.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Transforms the input grid to a single-pixel output grid. The color of the output
    pixel is the most frequent color in the input grid.
    """
    # Flatten the input grid into a 1D array to count color occurrences.
    flat_grid = input_grid.flatten()

    # Use Counter to find the most common color.
    color_counts = Counter(flat_grid)

    # Get the most common color (mode).
    most_common_color = color_counts.most_common(1)[0][0]

    # Create a 1x1 output grid with the most common color.
    output_grid = np.array([[most_common_color]])

    return output_grid