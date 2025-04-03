import numpy as np
from collections import Counter

"""
Homogenize the non-white part of the array to its most frequent non-white color, leaving white pixels unchanged.
1. Receive the input grid (a 1xN array).
2. Identify all pixels with non-white colors (values 1 through 9).
3. If no non-white pixels exist, return the input grid unchanged.
4. Count the occurrences of each distinct non-white color found.
5. Determine the single non-white color that has the highest count (the "dominant color").
6. Create a new output grid of the same dimensions as the input grid.
7. Iterate through each position in the input grid:
    a. If the pixel at the current position in the input grid is white (0), place a white pixel (0) in the corresponding position in the output grid.
    b. If the pixel at the current position in the input grid is non-white (1-9), place the determined dominant color in the corresponding position in the output grid.
8. Return the completed output grid.
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
    # .most_common(1) returns a list like [(color, count)], so access [0][0]
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid by replacing all non-white pixels with the
    single most frequent non-white color found in the input, preserving
    white pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Handle empty input case
    if not input_grid or not input_grid[0]:
        return []

    # Convert input list of lists to a NumPy array
    input_array = np.array(input_grid)
    original_shape = input_array.shape # Store original shape for output

    # Flatten the array for easier processing of all pixels
    input_array_1d = input_array.flatten()

    # Find the dominant non-white color in the flattened input array
    dominant_color = find_dominant_non_white_color(input_array_1d)

    # If no dominant non-white color exists (e.g., all pixels are white or grid is empty)
    # return the original grid.
    if dominant_color is None:
        return input_grid

    # Initialize the output array as a copy of the input 1D array
    # This ensures white pixels (0) are preserved by default
    output_array_1d = np.copy(input_array_1d)

    # Iterate through the flattened input array
    for i in range(input_array_1d.size):
        # If the pixel in the original input is non-white (value > 0)
        if input_array_1d[i] > 0:
            # Set the corresponding pixel in the output array to the dominant color
            output_array_1d[i] = dominant_color

    # Reshape the modified 1D array back to the original grid shape
    output_grid = output_array_1d.reshape(original_shape).tolist()

    return output_grid