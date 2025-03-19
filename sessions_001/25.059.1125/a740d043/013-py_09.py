"""
1. Identify Background: Find the most frequent color in the input grid. This is the background color.
2. Identify Objects: Identify all colors other than the background color. These are the object colors.
3. Order Colors: Place object colors, excluding background color, from left to right in the order: green, red. Insert white color between.
4. Construct Output: Create a 2x3 grid.
5. Populate Output: Fill both rows with ordered colors.
"""

import numpy as np

def get_objects(grid):
    """Find distinct colored regions, excluding the most frequent color."""
    unique_colors = np.unique(grid)
    counts = [np.sum(grid == color) for color in unique_colors]
    most_frequent_color = unique_colors[np.argmax(counts)]
    
    objects = []
    for color in unique_colors:
        if color != most_frequent_color:
            objects.append(color)
    return objects, most_frequent_color

def transform(input_grid):
    # Identify Background and Objects
    objects, background_color = get_objects(input_grid)

    # Order Colors: green, white, red
    ordered_colors = []
    if 3 in objects:  # green
        ordered_colors.append(3)
    ordered_colors.append(0) # white
    if 2 in objects:  # red
        ordered_colors.append(2)

    # Construct Output: 2x3 grid and Populate
    output_grid = np.array([ordered_colors, ordered_colors])

    return output_grid