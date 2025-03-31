import numpy as np
from typing import List

"""
Transforms the input grid according to the following rules:
1. Identifies the two non-background colors present in the input grid. One color is assumed to be red (2), designated as the 'marker' color. The other non-background color is designated as the 'primary' color.
2. Creates an output grid of the same dimensions as the input grid.
3. Iterates through each pixel of the input grid:
    a. If the pixel color is white (0), sets the corresponding output pixel to green (3).
    b. If the pixel color is red (2), sets the corresponding output pixel to the identified 'primary' color.
    c. If the pixel color is the 'primary' color, keeps the color the same in the output pixel.
    d. Any other color (if present, though not expected based on examples) is treated like the background and set to green (3).
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input grid
    output_array = np.copy(input_array)

    # Define known colors
    background_color_in = 0
    background_color_out = 3
    marker_color = 2

    # Find unique non-background colors in the input grid
    unique_colors = np.unique(input_array)
    non_background_colors = [c for c in unique_colors if c != background_color_in]

    # Identify the primary color (the non-background color that isn't the marker color)
    primary_color = -1 # Initialize with an invalid value
    for color in non_background_colors:
        if color != marker_color:
            primary_color = color
            break

    # Apply the transformation rules pixel by pixel
    rows, cols = input_array.shape
    for r in range(rows):
        for c in range(cols):
            input_color = input_array[r, c]

            if input_color == background_color_in:
                # Rule 3a: Change background color
                output_array[r, c] = background_color_out
            elif input_color == marker_color:
                # Rule 3b: Change marker color to primary color
                # This assumes a primary color was found, which is true for all examples.
                if primary_color != -1:
                    output_array[r, c] = primary_color
                else:
                    # If no primary color found (e.g., only background and red exist),
                    # treat red like background based on default transformation logic.
                    # This scenario is not present in training examples.
                    output_array[r, c] = background_color_out
            elif input_color == primary_color:
                # Rule 3c: Keep primary color
                # Since output_array started as a copy, no action needed here.
                pass
            else:
                # Rule 3d: Handle any other unexpected colors like background
                # This case should not occur based on the provided examples.
                output_array[r, c] = background_color_out

    # Convert the NumPy array back to a list of lists for the final output
    return output_array.tolist()