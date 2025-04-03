"""
Homogenizes the main color sequence in a 1D grid by replacing interrupting pixels 
with the sequence's dominant non-background color, while preserving the 
background (white) pixels.
"""

import numpy as np
from collections import Counter

def find_dominant_non_background_color(grid):
    """
    Finds the most frequent color in the grid, excluding the background color (0).

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The dominant non-background color. Returns -1 if no non-background
             colors are found or if there's a tie without a clear majority.
             (Note: Based on examples, a clear dominant color is expected).
    """
    # Flatten the grid if it's 2D, otherwise assume it's 1D
    if grid.ndim > 1:
        flat_grid = grid.flatten()
    else:
        flat_grid = grid

    # Filter out background pixels (color 0)
    non_background_pixels = [pixel for pixel in flat_grid if pixel != 0]

    if not non_background_pixels:
        return -1 # Or handle as appropriate, maybe return 0 if background is the only color?

    # Count frequencies
    color_counts = Counter(non_background_pixels)

    # Find the most common color
    # The most_common(1) method returns a list of tuples [(color, count)]
    dominant_color, count = color_counts.most_common(1)[0]

    # Consider tie-breaking if necessary, though examples don't show ties.
    # If there are multiple colors with the same highest count, this picks one.
    # A more robust solution might be needed if ties are possible and meaningful.

    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid by replacing pixels that are not the background
    color (0) and not the dominant non-background color with the dominant
    non-background color.

    Args:
        input_grid (list or np.array): A 1D list or a 1xN numpy array representing the input grid.

    Returns:
        np.array: The transformed grid as a numpy array.
    """
    # Ensure input is a numpy array for easier processing
    input_grid_np = np.array(input_grid)

    # Find the dominant color (excluding background color 0)
    dominant_color = find_dominant_non_background_color(input_grid_np)

    # Handle the case where no non-background color was found
    if dominant_color == -1:
        return input_grid_np.copy() # Return the original grid if only background exists

    # Create a copy of the input grid to modify
    output_grid = input_grid_np.copy()

    # Iterate through the grid and apply the transformation
    # Using np.nditer for potentially multi-dimensional arrays, though examples are 1D
    with np.nditer(output_grid, op_flags=['readwrite']) as it:
        for pixel in it:
            # Check if the current pixel is NOT background (0) and NOT the dominant color
            if pixel != 0 and pixel != dominant_color:
                # Replace it with the dominant color
                pixel[...] = dominant_color # Ellipsis modifies the element in place

    return output_grid
