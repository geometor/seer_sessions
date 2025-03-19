"""
1. Check for Orange: Examine the input grid to determine if the color orange (pixel value 7) is present.
2. If Orange Exists: If orange is found anywhere in the input grid, the output is a 1x1 grid containing a single orange pixel ([[7]]).
3. If Orange is Absent: If orange is not found, count the occurrences of each color (excluding orange) in the input grid. Identify the color with the highest count. Create an output grid of the *same dimensions as the input grid* where every pixel is of that most frequent color.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """Transforms the input grid based on the presence or absence of orange."""
    input_grid = np.array(input_grid)

    # Check for orange
    if np.any(input_grid == 7):
        # If orange exists, return a 1x1 orange grid
        output_grid = np.array([[7]])
    else:
        # If orange is absent, find the most frequent color
        output_grid = find_most_frequent_color_grid(input_grid)

    return output_grid

def find_most_frequent_color_grid(grid):
    """Finds the most frequent color in a grid (excluding orange) and returns a grid of the same dimensions filled with that color."""
    colors = grid.flatten().tolist()
    color_counts = Counter(colors)
    
    #Remove orange if it is an option
    if 7 in color_counts:
        del color_counts[7]

    # Get most frequent color
    most_common_color = color_counts.most_common(1)[0][0]
    
    #create an output grid of the input grid size will all pixels of most
    #common color
    output_grid = np.full(grid.shape, most_common_color)
    return output_grid