```python
import numpy as np
from collections import Counter

"""
Identifies all distinct non-background colors present in the input grid. For each distinct 
non-background color, calculates its total count (number of pixels of that color). 
Determines the maximum count found among these colors. Identifies all non-background 
color(s) that have this maximum count (target colors). Initializes an output grid with 
the same dimensions as the input grid, filled entirely with the background color (black, 0). 
Iterates through each pixel coordinate (row, column) of the input grid. If the color of 
the input pixel at the current coordinate is one of the target colors, sets the color of 
the pixel at the corresponding coordinate in the output grid to this target color. Otherwise, 
the corresponding output pixel remains the background color. The final state of the output 
grid is the result.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by retaining only the pixels corresponding to the
    non-background color(s) that appear most frequently (highest total pixel count).

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid containing only the pixels
        of the most frequent non-background color(s).
    """
    # Convert input grid to a numpy array for efficient array operations
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Define the background color (assumed to be 0)
    background_color = 0

    # Initialize the output grid with the same dimensions as the input,
    # filled entirely with the background color.
    output_array = np.full((rows, cols), background_color, dtype=int)

    # --- Step 1 & 2: Calculate Color Frequencies for non-background pixels ---
    # Select only the pixels that are not the background color
    non_background_pixels = input_array[input_array != background_color]

    # Edge case: If there are no non-background pixels, return the empty grid
    if non_background_pixels.size == 0:
        return output_array.tolist()

    # Use collections.Counter to count occurrences of each color value
    color_counts = Counter(non_background_pixels)

    # --- Step 3: Determine the maximum count ---
    # Find the highest frequency count among the non-background colors
    # Check if color_counts is not empty (handles case if somehow non_background_pixels was empty despite size > 0)
    max_count = 0
    if color_counts:
        max_count = max(color_counts.values())

    # --- Step 4: Identify Target Color(s) ---
    # Create a set of all colors that have the maximum count
    # This handles potential ties for the most frequent color
    target_colors = {color for color, count in color_counts.items() if count == max_count}

    # --- Step 5 & 6 & 7 & 8: Filter Pixels ---
    # Iterate through each pixel coordinate of the input grid
    for r in range(rows):
        for c in range(cols):
            # Get the color of the pixel at the current coordinate
            pixel_color = input_array[r, c]
            # Check if this color is one of the identified target colors
            if pixel_color in target_colors:
                # If it's a target color, copy it to the output grid at the same coordinate
                output_array[r, c] = pixel_color
            # No 'else' needed because the output grid is already filled with the background color

    # --- Step 9: Return the result ---
    # Convert the output numpy array back to the required list of lists format
    output_grid = output_array.tolist()

    return output_grid
```