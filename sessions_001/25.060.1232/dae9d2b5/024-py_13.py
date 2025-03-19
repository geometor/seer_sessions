"""
Counts the number of non-white pixels in the input grid.
Identifies the most frequent non-white color in the input grid.
Creates a 3x3 output grid filled entirely with the most frequent non-white color.
"""

import numpy as np
from collections import Counter

def get_most_frequent_non_white_color(grid):
    # Flatten the grid and count color occurrences
    colors = grid.flatten()
    color_counts = Counter(colors)
    
    # Remove white (0) from consideration
    if 0 in color_counts:
        del color_counts[0]
    
    # Return the most common color
    if color_counts:
        return color_counts.most_common(1)[0][0]
    else:
        return 0  # Default to white if no non-white colors

def transform(input_grid):
    # Determine the most frequent non-white color
    fill_color = get_most_frequent_non_white_color(input_grid)

    # Create a 3x3 output grid filled with the identified color
    output_grid = np.full((3, 3), fill_color, dtype=int)

    return output_grid