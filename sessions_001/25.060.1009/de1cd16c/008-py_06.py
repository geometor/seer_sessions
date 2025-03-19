"""
1. Examine the input grid and count the occurrences of each unique color.
2. Identify the most frequent non-white color.
3. Create a 1x1 output grid.
4. Set the color of the output grid to the most frequent non-white color found in the input grid.
5. If all of the colors in the input are white, set output to white.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """Transforms an input grid into a 1x1 output grid.

    The color of the output grid is the most frequent non-white color in the
    input grid. If only white is present, the output is white.
    """
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Count the occurrences of each color
    color_counts = Counter(input_grid.flatten())

    # Find the most frequent non-white color
    most_frequent_color = 0  # Initialize to white
    max_count = 0

    for color, count in color_counts.items():
        if color != 0 and count > max_count:
            most_frequent_color = color
            max_count = count
        elif color == 0 and max_count == 0:
            most_frequent_color = color
        
    # Create a 1x1 output grid with the most frequent non-white color
    output_grid = np.array([[most_frequent_color]])

    return output_grid