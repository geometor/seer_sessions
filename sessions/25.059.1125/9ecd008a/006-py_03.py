"""
Determine the dominant color within the central 3x3 region of the input grid, or the whole grid if no single dominant color in the center.  Construct a 3x3 output grid filled with this dominant color.
"""

import numpy as np
from collections import Counter

def get_dominant_color(grid):
    # Flatten the grid to a 1D array and count color occurrences.
    counts = Counter(grid.flatten())
    # Return the most common color.
    return counts.most_common(1)[0][0]

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_array = np.array(input_grid)
    height, width = input_array.shape

    # Calculate the center coordinates.
    center_y = height // 2
    center_x = width // 2
    region_size = 3

    # Calculate starting indices for the central region.
    start_y = max(0, center_y - region_size // 2)  # Ensure start_y is within bounds
    start_x = max(0, center_x - region_size // 2)  # Ensure start_x is within bounds

    # Extract central region, handling edge cases.
    end_y = min(height, start_y + region_size)  # Ensure end_y is within bounds
    end_x = min(width, start_x + region_size)    # Ensure end_x is within bounds
    central_region = input_array[start_y:end_y, start_x:end_x]

    # Get the dominant color in the central region.
    dominant_color_center = get_dominant_color(central_region)

    #Check to ensure that central region had only one color
    if len(Counter(central_region.flatten())) > 1:
        dominant_color = get_dominant_color(input_array) #use whole array if not one color
    else:
        dominant_color = dominant_color_center


    # Create a 3x3 output grid filled with the dominant color.
    output_grid = np.full((3, 3), dominant_color, dtype=int)
    
    return output_grid.tolist()