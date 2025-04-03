"""
Identifies the most frequent non-background color (0) in the input grid (flattened if necessary).
Defines a modification span from the first to the last occurrence of this dominant color in the flattened sequence.
Within this span, replaces any pixel that is neither the dominant color nor the background color (0) with the dominant color.
Pixels outside the span or pixels matching the dominant or background color remain unchanged.
The output grid retains the original dimensions of the input grid.
"""

import numpy as np
from collections import Counter

def find_dominant_non_background_color(grid_1d):
    """
    Finds the most frequent color in a 1D array, excluding the background color 0.

    Args:
        grid_1d (np.ndarray): A 1D numpy array of pixel values.

    Returns:
        int or None: The dominant color value, or None if no non-background colors exist.
    """
    # Count frequencies of non-background colors
    counts = Counter(c for c in grid_1d if c != 0)
    if not counts:
        return None  # No non-background colors found
    # Find the color with the maximum count
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list or np.ndarray): A potentially 2D grid representing the input.

    Returns:
        np.ndarray: The transformed grid with the same dimensions as the input.
    """
    # Convert input to a numpy array and store original shape
    input_array = np.array(input_grid)
    original_shape = input_array.shape

    # Flatten the array for 1D processing
    grid_1d = input_array.flatten()

    # Handle edge case: empty input
    if grid_1d.size == 0:
        return input_array.copy() # Return copy of original (empty) array

    # Initialize output_grid as a copy of the flattened input
    output_grid_1d = grid_1d.copy()

    # Identify the background color (assumed to be 0)
    background_color = 0

    # Find the dominant non-background color in the flattened grid
    dominant_color = find_dominant_non_background_color(grid_1d)

    # If no non-background color exists, return the original grid (reshaped)
    if dominant_color is None:
        return output_grid_1d.reshape(original_shape)

    # Find the first and last indices of the dominant color in the flattened grid
    indices = np.where(grid_1d == dominant_color)[0]

    # If dominant color is somehow not found (shouldn't happen if find_dominant_color returned a value)
    if indices.size == 0:
        return output_grid_1d.reshape(original_shape) # Return unmodified copy

    first_index = indices[0]
    last_index = indices[-1]

    # Define the modification span (inclusive)
    start_span = first_index
    end_span = last_index

    # Iterate through the modification span in the 1D output grid
    for i in range(start_span, end_span + 1):
        current_color = output_grid_1d[i]
        # Check if the color is an 'impurity' (not dominant and not background)
        if current_color != dominant_color and current_color != background_color:
            # Replace impurity with the dominant color
            output_grid_1d[i] = dominant_color

    # Reshape the modified 1D array back to the original input shape
    output_grid = output_grid_1d.reshape(original_shape)

    return output_grid