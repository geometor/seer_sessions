import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Analyzes the input grid to determine the output grid based on color frequencies.

    1. Count the occurrences of each non-white (non-zero) color in the input grid.
    2. Count the occurrences of the white color (0).
    3. Sort the non-white colors first by frequency (descending) and then by color value (descending) in case of ties.
    4. Check for a tie in frequency between the top two most frequent non-white colors (or if there's only one non-white color).
       - If there is a tie (or only one color): The output is a 1x1 grid containing the color value among the tied colors that is numerically largest.
       - If there is no tie:
         - Identify the most frequent non-white color (C1) and the second most frequent non-white color (C2).
         - Let Count(C1), Count(C2), and Count(0) be their respective counts.
         - If Count(C1) > Count(C2) + Count(0):
           - The output is a 2x2 grid: [[C1, C1], [C2, C1]]
         - Else:
           - The output is a 2x2 grid: [[C1, C1], [C1, C2]]
    """

    # Convert input list of lists to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)

    # Flatten the array to easily count all pixels
    pixels = input_array.flatten()

    # Count occurrences of each color
    color_counts = Counter(pixels)

    # Separate white count and non-white counts
    white_count = color_counts.get(0, 0)
    non_white_counts = {color: count for color, count in color_counts.items() if color != 0}

    # If there are no non-white colors, return an empty grid or handle as an edge case
    # Based on examples, assume at least one non-white color exists or the tie-breaking covers it.
    if not non_white_counts:
        # This case isn't covered by examples, returning 1x1 white as a guess.
        # Or perhaps an empty grid? Let's follow the tie logic if possible.
        # If only white exists, Counter is {0: count}. non_white_counts is empty.
        # Let's assume the task guarantees non-white pixels if output is expected.
        # For safety, returning a minimal grid.
         return [[0]] 


    # Sort non-white colors: primary key = count (desc), secondary key = color (desc)
    # Creates a list of tuples: [(color, count), ...]
    sorted_colors = sorted(non_white_counts.items(), key=lambda item: (item[1], item[0]), reverse=True)

    # Check for tie condition
    # Tie if only one non-white color exists, or if top two have same count
    is_tie = len(sorted_colors) < 2 or sorted_colors[0][1] == sorted_colors[1][1]

    if is_tie:
        # Find the highest color value among those tied for the max count
        max_count = sorted_colors[0][1]
        tied_colors = [color for color, count in sorted_colors if count == max_count]
        output_color = max(tied_colors)
        output_grid = [[output_color]]
    else:
        # No tie, determine the 2x2 grid pattern
        c1 = sorted_colors[0][0]
        count_c1 = sorted_colors[0][1]
        c2 = sorted_colors[1][0]
        count_c2 = sorted_colors[1][1]

        # Apply the condition based on counts
        if count_c1 > count_c2 + white_count:
            # Pattern: [[C1, C1], [C2, C1]]
            output_grid = [[c1, c1], [c2, c1]]
        else:
            # Pattern: [[C1, C1], [C1, C2]]
            output_grid = [[c1, c1], [c1, c2]]

    # Return the result as a list of lists
    return output_grid