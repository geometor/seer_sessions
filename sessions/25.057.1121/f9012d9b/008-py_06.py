"""
Transformation Rule:
1. Analyze the Input: Examine the input grid and identify all unique colors present.
2. Count Occurrences: Count the number of times each color appears in the input grid.
3. Ignore white (0): specifically do not count zero values.
4. Determine the next most frequent: Find the color with the highest count of the remaining.
5. Create Output: Create a 1x1 output grid.
6. Set Output Color: Set the color of the single pixel in the output grid to the second most frequent color identified in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into a 1x1 grid with the second most frequent color (excluding white/0).
    """
    # Count Occurrences
    unique, counts = np.unique(input_grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    
    # Ignore white (0)
    if 0 in color_counts:
        del color_counts[0]
    if not color_counts:
        return np.array([[0]])
    # find max color if tie for second place
    max_color = max(color_counts, key=color_counts.get)
    
    color_counts_no_max = {k:v for k,v in color_counts.items() if k != max_color}

    if not color_counts_no_max:
        #all values are the same
        # Determine the next most frequent
        most_frequent_color = max_color
    else:
       most_frequent_color = max(color_counts_no_max, key=color_counts_no_max.get)
   
    # Create Output: 1x1 grid
    output_grid = np.array([[most_frequent_color]])

    return output_grid