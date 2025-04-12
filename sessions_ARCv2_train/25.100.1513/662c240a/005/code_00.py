import numpy as np
from collections import Counter

"""
Calculates the total count of pixels for each distinct non-background color present in the 
input grid. Identifies the color(s) that have the maximum total pixel count. These are the 
"target colors". Initializes an output grid with the same dimensions as the input grid, 
filled entirely with the background color (black, 0). Iterates through each pixel of the 
input grid. If the color of the input pixel at a given coordinate is one of the target 
colors, copies this color to the corresponding coordinate in the output grid. Otherwise, 
the corresponding output pixel remains the background color. The final state of the 
output grid is the result.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by keeping only the pixels of the non-background color(s)
    that appear most frequently (highest total pixel count).

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid containing only the pixels
        of the most frequent non-background color(s).
    """
    # Convert input grid to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Define the background color (conventionally 0)
    background_color = 0

    # Initialize the output grid with the background color
    output_array = np.full((rows, cols), background_color, dtype=int)

    # Select all pixels that are not the background color
    non_background_pixels = input_array[input_array != background_color]

    # Handle the edge case where the grid contains only background pixels
    if non_background_pixels.size == 0:
        # Return the grid filled with background color
        return output_array.tolist()

    # Count the occurrences of each non-background color
    # Counter is efficient for this {color: count} mapping
    color_counts = Counter(non_background_pixels)

    # Find the maximum count among the non-background colors
    # Check if color_counts is not empty before finding max
    max_count = 0
    if color_counts:
        max_count = max(color_counts.values())

    # Identify all colors that achieved this maximum count (handles ties)
    # These are the colors we want to keep in the output
    target_colors = {color for color, count in color_counts.items() if count == max_count}

    # Iterate through the input grid coordinates
    for r in range(rows):
        for c in range(cols):
            # Get the color of the current pixel in the input grid
            pixel_color = input_array[r, c]
            # Check if this pixel's color is one of the target colors
            if pixel_color in target_colors:
                # If it is a target color, copy it to the output grid
                output_array[r, c] = pixel_color
            # Otherwise, the output grid pixel remains the background color (already initialized)

    # Convert the final output numpy array back to a list of lists format
    output_grid = output_array.tolist()

    return output_grid