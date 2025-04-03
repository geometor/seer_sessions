import collections
import numpy as np # Although not strictly needed for 1D lists, it's standard for ARC tasks

"""
Transformation Rule:

1. Examine the input sequence of pixels (represented as a 1D list of color integers).
2. Identify all pixels that are not white (color 0).
3. Count the occurrences of each non-white color present in the sequence.
4. Determine the non-white color that appears most frequently; this is the "target color". If there are no non-white colors, the input is returned unchanged.
5. Create a new output sequence, initially identical to the input sequence.
6. Iterate through each pixel in the input sequence:
    *   If the pixel's color is not white (0), change the color of the corresponding pixel in the output sequence to the determined "target color".
    *   If the pixel's color is white (0), leave the color of the corresponding pixel in the output sequence unchanged (it remains white).
7. The final modified sequence is the result.
"""


def find_dominant_non_white_color(pixel_sequence):
    """
    Finds the most frequent non-white color in a sequence.

    Args:
        pixel_sequence: A list of integers representing pixel colors.

    Returns:
        The integer value of the most frequent non-white color,
        or None if no non-white colors are present.
    """
    # Filter out white pixels (color 0)
    non_white_pixels = [pixel for pixel in pixel_sequence if pixel != 0]

    # If there are no non-white pixels, return None
    if not non_white_pixels:
        return None

    # Count the frequency of each non-white color
    color_counts = collections.Counter(non_white_pixels)

    # Find the color with the highest count
    # most_common(1) returns a list of tuples [(color, count)], we take the first element's color
    dominant_color = color_counts.most_common(1)[0][0]

    return dominant_color

def transform(input_sequence):
    """
    Transforms the input sequence by replacing all non-white pixels
    with the most frequent non-white color found in the sequence.

    Args:
        input_sequence: A list of integers representing pixel colors.

    Returns:
        A new list representing the transformed sequence.
    """
    # Make a copy to avoid modifying the original input
    output_sequence = list(input_sequence)

    # Find the dominant non-white color in the input sequence
    target_color = find_dominant_non_white_color(input_sequence)

    # If no non-white pixels were found, return the original sequence copy
    if target_color is None:
        return output_sequence

    # Iterate through the sequence and apply the transformation
    for i in range(len(output_sequence)):
        # If the current pixel is not white (0)
        if output_sequence[i] != 0:
            # Change its color to the target dominant color
            output_sequence[i] = target_color

    # Return the modified sequence
    return output_sequence