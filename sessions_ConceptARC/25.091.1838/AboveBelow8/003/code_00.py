"""
Create an output grid of the same dimensions as the input grid, initialized with white (0). For each row in the input grid, determine the most frequent color, excluding white (0) and azure (8). If this dominant row color is green (3), then any azure (8) pixels in that row are ignored. Otherwise (if the dominant color is not green, or if there is no dominant color other than white/azure), azure (8) pixels from the input row are copied to the corresponding positions in the output grid. All other positions in the output grid remain white (0).
"""

import numpy as np
from collections import Counter

def get_dominant_color_in_row(row):
    """
    Finds the most common color in a row, excluding white (0) and azure (8).

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        int or None: The dominant color value (an integer) if found, otherwise None.
    """
    # Filter out white (0) and azure (8) pixels
    filtered_pixels = [pixel for pixel in row if pixel != 0 and pixel != 8]

    # If no other colors are present, return None
    if not filtered_pixels:
        return None

    # Count frequencies of the remaining colors
    counts = Counter(filtered_pixels)

    # Find the most common color
    # counts.most_common(1) returns a list like [ (color, count) ]
    dominant_color, _ = counts.most_common(1)[0]

    # Ensure the returned type is a standard Python int
    if isinstance(dominant_color, np.integer):
        dominant_color = int(dominant_color)
        
    return dominant_color

def transform(input_grid):
    """
    Filters the input grid, keeping azure (8) pixels only if their row's dominant color
    (excluding white and azure) is not green (3).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize an output grid of the same dimensions with white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Determine the dominant color for each row and identify rows where azure (8) should be discarded
    rows_to_discard_azure = set()
    for r in range(height):
        dominant_color = get_dominant_color_in_row(input_grid[r])
        # If the dominant color is green (3), mark this row for discarding azure pixels
        if dominant_color == 3:
            rows_to_discard_azure.add(r)

    # Iterate through the input grid and populate the output grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is azure (8)
            if input_grid[r, c] == 8:
                # Check if the current row is NOT marked for discarding azure pixels
                if r not in rows_to_discard_azure:
                    # If not discarded, copy the azure pixel to the output grid
                    output_grid[r, c] = 8
            # Otherwise (pixel is not azure, or it's azure in a discarded row),
            # the output grid pixel remains the default white (0)

    return output_grid