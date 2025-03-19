"""
The transformation rule is as follows:

1. Count the occurrences of each color (digit) in the input grid.
2. Determine if there's a dominant color: A color is considered "dominant" if its count is greater than or equal to the sum of all *other* colors - 1.
3. If a dominant color exists, create a 1x1 output grid with the value '1'.
4. If no dominant color exists the output grid will be none.

"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid based on color dominance.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list: A 1x1 grid containing '1' if a dominant color exists, otherwise None.
    """
    # Convert input grid to numpy array
    input_array = np.array(input_grid)

    # Count occurrences of each color
    unique, counts = np.unique(input_array, return_counts=True)
    color_counts = dict(zip(unique, counts))

    # Find the color with the maximum count
    max_count = 0
    dominant_color = None
    for color, count in color_counts.items():
        if count > max_count:
            max_count = count
            dominant_color = color

    # Check if the dominant color count is >= sum of other color counts - 1
    sum_other_colors = sum(count for color, count in color_counts.items() if color != dominant_color)
    
    if max_count >= sum_other_colors + 1: # key change: added +1
      output_grid = [[1]]
      return output_grid
    else:
      return None # no transformation