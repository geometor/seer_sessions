"""
Homogenize the non-white pixels of an input grid to the most frequent non-white color found within that grid, while preserving the positions and values of white (0) pixels.
1. Receive the input grid.
2. Create an output grid initialized as a copy of the input grid.
3. Identify all non-white pixels (values 1 through 9) across the entire input grid.
4. If there are no non-white pixels in the input grid, return the initial output grid (which is a copy of the input).
5. Count the frequency of each distinct non-white color found in the input grid.
6. Determine the single non-white color that occurs most frequently (the "dominant color").
7. Identify the locations (row and column indices) of *all* pixels in the input grid that are non-white (value > 0).
8. For each of these identified locations, update the corresponding pixel in the output grid to the determined dominant color. (White pixels remain unchanged from the initial copy).
9. Return the modified output grid.
"""

import numpy as np
from collections import Counter

def find_dominant_non_white_color(arr):
    """
    Finds the most frequent non-white color in a numpy array.

    Args:
        arr: A numpy array of integers (colors).

    Returns:
        The integer value of the dominant non-white color, or None if no
        non-white colors are present.
    """
    # Filter out white pixels (0) and flatten for counting
    non_white_pixels = arr[arr > 0].flatten()

    # Check if there are any non-white pixels
    if non_white_pixels.size == 0:
        return None

    # Count occurrences of each non-white color
    counts = Counter(non_white_pixels)

    # Find the color with the maximum count
    # .most_common(1) returns a list like [(color, count)], so access [0][0]
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid according to the homogenization rule described above.
    """
    # Handle empty input case
    if not input_grid or not input_grid[0]:
        return []

    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)

    # Find the dominant non-white color in the input array
    dominant_color = find_dominant_non_white_color(input_array)

    # If no dominant non-white color exists (e.g., all pixels are white),
    # return the original grid as a list of lists.
    if dominant_color is None:
        return input_grid

    # Create the output array initially as a copy of the input array.
    # This ensures that white pixels (0) are preserved by default.
    output_array = np.copy(input_array)

    # Identify the locations (indices) of all non-white pixels (value > 0)
    # in the original input array. np.where returns a tuple of arrays (one for each dimension).
    non_white_indices = np.where(input_array > 0)

    # Update the values in the output array at these identified non-white locations
    # setting them to the determined dominant color.
    output_array[non_white_indices] = dominant_color

    # Convert the modified NumPy array back to a list of lists format for the output.
    output_grid = output_array.tolist()

    return output_grid