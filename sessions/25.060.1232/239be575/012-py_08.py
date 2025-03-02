"""
1. Count Colors: Examine the input grid and count how many times each color (0-9) appears.
2. Exclude White: Disregard the count for color 0 (white).
3. Find Maximum: Determine the color that occurred most frequently among the remaining colors.
4. Create Output: Create a new 1x1 grid.  The single cell in this grid should have the value of the most frequent color identified in the previous step. If there are no other colors, the output will be 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by extracting the most frequent color (excluding 0)
    and returning a 1x1 grid with that color.
    """
    # Convert input_grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Count the occurrences of each color.
    unique_colors, color_counts = np.unique(input_array, return_counts=True)

    # Create a dictionary to store color counts, excluding 0.
    color_counts_dict = {}
    for color, count in zip(unique_colors, color_counts):
        if color != 0:
            color_counts_dict[color] = count

    # Find the most frequent color.
    if color_counts_dict:  # Check if the dictionary is not empty
        most_frequent_color = max(color_counts_dict, key=color_counts_dict.get)
    else:
        most_frequent_color=0 #default if no colors other than zero
    # Create the 1x1 output grid.
    output_grid = np.array([[most_frequent_color]])

    return output_grid