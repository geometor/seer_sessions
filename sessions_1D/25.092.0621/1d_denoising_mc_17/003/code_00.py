"""
Transforms the input grid by identifying the most frequent non-white color (dominant color) and replacing all non-white pixels in the grid with this dominant color. White pixels (color 0) remain unchanged. If the input grid contains only white pixels, it is returned unchanged.
"""

import numpy as np
import collections

def _find_dominant_color(pixels):
    """
    Finds the most frequent color among a list/array of pixel values.

    Args:
        pixels (np.ndarray or list): A collection of pixel color values.

    Returns:
        int: The most frequent color value. Returns 0 if the input is empty.
    """
    if len(pixels) == 0:
        return 0  # Default or signifies no non-white pixels found
    count = collections.Counter(pixels)
    dominant_color = count.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Applies the dominant color transformation to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)

    # Identify all non-white pixels (pixels with value != 0)
    non_white_mask = input_np != 0
    non_white_pixels = input_np[non_white_mask]

    # Check if there are any non-white pixels
    if non_white_pixels.size == 0:
        # If no non-white pixels, return the original grid as is (converted back to list of lists)
        return input_np.tolist()

    # Determine the dominant color among the non-white pixels
    dominant_color = _find_dominant_color(non_white_pixels)

    # Create the output grid initially as a copy of the input grid
    output_np = np.copy(input_np)

    # Replace all non-white pixels in the output grid with the dominant color
    # Use the previously created mask to efficiently target these pixels
    output_np[non_white_mask] = dominant_color

    # Convert the resulting NumPy array back to a list of lists for the final output
    return output_np.tolist()