"""
Examine the input grid and identify all the unique colors present.
Select a single color from the set of unique colors found in the input grid. The choice of which color is dependent on the most frequently occuring non-zero colors.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier processing.
    grid = np.array(input_grid)
    
    # Flatten the grid to a 1D array and count the occurrences of each color.
    color_counts = Counter(grid.flatten())
    
    # Remove the count for color 0 (background color, white), as we are interested in non-background colors.
    if 0 in color_counts:
        del color_counts[0]
    
    # Find the most frequent color(s).
    if color_counts:  # Make sure color_counts is not empty, i.e. some non-zero colors were on the grid
       most_common_colors = color_counts.most_common()
       max_count = most_common_colors[0][1]
       
       # gather all colors with the same max_count, and select the largest value
       candidates = [color for color, count in most_common_colors if count == max_count ]
       output_color = max(candidates)
    else:  # handles edge case if color_counts IS empty, i.e. the whole grid was '0'
        output_color = 0
    
    # Return the selected output color.
    return output_color