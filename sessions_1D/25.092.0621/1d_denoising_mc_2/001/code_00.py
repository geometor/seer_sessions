import numpy as np
from collections import Counter

"""
Identify all non-white pixels (values 1-9) in the input 1D array.
Determine the most frequent color among these non-white pixels (the dominant color).
Create an output array where all original white pixels (0) remain white,
and all original non-white pixels are replaced with the identified dominant color.
"""

def find_dominant_non_white_color(arr_1d):
    """
    Finds the most frequent non-white color in a 1D numpy array.

    Args:
        arr_1d: A 1D numpy array of integers (colors).

    Returns:
        The integer value of the dominant non-white color, or None if no
        non-white colors are present.
    """
    # Filter out white pixels (0)
    non_white_pixels = arr_1d[arr_1d > 0]

    # Check if there are any non-white pixels
    if non_white_pixels.size == 0:
        return None

    # Count occurrences of each non-white color
    counts = Counter(non_white_pixels)

    # Find the color with the maximum count
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid by replacing all non-white pixels with the
    single most frequent non-white color found in the input.

    Args:
        input_grid: A list of lists representing the input grid (assumed 1xN).

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input grid (list of lists) to a 1D numpy array
    # Assuming input is always effectively 1D (e.g., 1xN)
    if not input_grid:
        return []
    input_array_1d = np.array(input_grid).flatten()

    # Initialize the output array as a copy of the input
    output_array_1d = np.copy(input_array_1d)

    # Find the dominant non-white color in the input
    dominant_color = find_dominant_non_white_color(input_array_1d)

    # If a dominant non-white color exists, proceed with replacement
    if dominant_color is not None:
        # Iterate through the input array
        for i in range(input_array_1d.size):
            # If the current pixel is non-white
            if input_array_1d[i] > 0:
                # Replace it with the dominant color in the output array
                output_array_1d[i] = dominant_color
            # White pixels (0) remain unchanged as per the copy initialization

    # Reshape the 1D output array back to the original input grid shape (1xN)
    # Assuming input was 1 row
    output_grid = output_array_1d.reshape(1, -1).tolist()

    return output_grid