import collections

"""
Transform the input array by identifying the most frequent non-white (non-zero)
color and replacing all non-white pixels with that dominant color. White (zero)
pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid: A list of integers representing the input grid pixels.

    Returns:
        A list of integers representing the transformed output grid pixels.
    """

    # 1. Identify all non-white pixels in the input array.
    foreground_pixels = [pixel for pixel in input_grid if pixel != 0]

    # Handle the case where there are no non-white pixels
    if not foreground_pixels:
        return input_grid # Output is identical to input if only white pixels

    # 2. Count the occurrences of each distinct color among these non-white pixels.
    color_counts = collections.Counter(foreground_pixels)

    # 3. Determine the color that occurs most frequently (the dominant color).
    # most_common(1) returns a list of tuples [(element, count)], so we get the element [0][0].
    dominant_color = color_counts.most_common(1)[0][0]

    # 4. Construct the output array.
    output_grid = []
    for pixel in input_grid:
        # a. If the current pixel is white (0), copy it.
        if pixel == 0:
            output_grid.append(0)
        # b. If the current pixel is non-white, place the dominant color.
        else:
            output_grid.append(dominant_color)

    return output_grid