import numpy as np
from collections import Counter

"""
Calculates the total count of pixels for each distinct non-background color in the input grid.
Identifies the color(s) with the maximum total pixel count (target color(s)). Initializes an 
output grid of the same dimensions as the input, filled with the background color (black, 0). 
Copies only the pixels from the input grid whose color matches the target color(s) to the 
output grid at their original locations.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by keeping only the pixels of the color(s) that
    appear most frequently (highest total pixel count) among non-background colors.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid containing only the pixels
        of the most frequent non-background color(s).
    """
    # Convert input grid to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Define the background color
    background_color = 0

    # Initialize the output grid with the background color
    output_array = np.full((rows, cols), background_color, dtype=int)

    # Find all non-background pixels
    non_background_pixels = input_array[input_array != background_color]

    # Handle the edge case where the grid might only contain background pixels
    if non_background_pixels.size == 0:
        # If there are no non-background pixels, return the empty background grid
        return output_array.tolist()

    # Count the occurrences of each non-background color
    color_counts = Counter(non_background_pixels)

    # Find the maximum count
    max_count = 0
    if color_counts: # Check if color_counts is not empty
        max_count = max(color_counts.values())

    # Identify all colors that have the maximum count (handling ties)
    target_colors = {color for color, count in color_counts.items() if count == max_count}

    # Create a boolean mask for pixels in the input array that match any target color
    # We iterate through target colors and combine masks using logical OR
    # Start with a mask of all False
    combined_mask = np.zeros_like(input_array, dtype=bool)
    for color in target_colors:
        combined_mask |= (input_array == color)

    # Apply the combined mask: where the mask is True, copy the color from the
    # input array to the output array
    output_array[combined_mask] = input_array[combined_mask]

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid