"""
1. Identify the most frequent color: Count the occurrences of each color (digit) within the input grid.
2. Determine Maximum Occurrence:  The output is the color with most instances in the entire grid.
3. Output: The output is the single color code.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Transforms the input grid to the most frequent color.
    """
    # Flatten the grid to a 1D array
    flat_grid = input_grid.flatten()

    # Count the occurrences of each color
    color_counts = Counter(flat_grid)

    # Find the most frequent color
    most_frequent_color = color_counts.most_common(1)[0][0]
    
    #output
    output_grid = np.array([[most_frequent_color]])

    return output_grid