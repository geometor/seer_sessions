"""
Counts the occurrences of each color in the input grid and returns the color value that appears most frequently, excluding zero (white).
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier processing.
    grid = np.array(input_grid)

    # Initialize a dictionary to store color counts.
    color_counts = {}

    # Iterate through the grid to count color occurrences.
    for row in grid:
        for cell in row:
            if cell != 0:  # Exclude white (0)
                if cell in color_counts:
                    color_counts[cell] += 1
                else:
                    color_counts[cell] = 1

    # Find the color with the maximum count.
    max_count = 0
    most_frequent_color = None
    for color, count in color_counts.items():
        if count > max_count:
            max_count = count
            most_frequent_color = color
    
    if most_frequent_color is None:
      return [0] # if the board only had zeros, then return zero
    else:
      return [most_frequent_color]