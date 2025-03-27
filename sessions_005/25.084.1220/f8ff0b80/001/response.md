```python
import numpy as np
from collections import Counter

"""
Identify unique non-white colors in the input grid. Count the total number of pixels 
for each unique non-white color. Sort the colors in descending order based on their 
pixel counts. Construct a single-column output grid containing the sorted colors.
"""

def transform(input_grid):
    """
    Transforms the input grid by identifying unique non-white colors, counting their occurrences,
    sorting them by count in descending order, and outputting them as a single column.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array (single column) containing the sorted colors.
    """

    # Flatten the grid to easily count all pixels
    flat_grid = input_grid.flatten()

    # Count occurrences of each color
    # We use Counter for convenience, but could also loop manually
    color_counts = Counter(flat_grid)

    # Filter out the background color (0) and store colors with their counts
    non_white_counts = []
    for color, count in color_counts.items():
        if color != 0:
            non_white_counts.append((color, count))

    # Sort the colors based on their counts in descending order
    # If counts are equal, the original order from Counter might be preserved,
    # but the problem description doesn't specify tie-breaking, so default sort is fine.
    sorted_colors_with_counts = sorted(non_white_counts, key=lambda item: item[1], reverse=True)

    # Extract just the sorted colors
    sorted_colors = [color for color, count in sorted_colors_with_counts]

    # Determine the dimensions of the output grid
    output_height = len(sorted_colors)
    output_width = 1

    # Create the output grid
    # Ensure it's a 2D array even if there's only one color
    output_grid = np.array(sorted_colors).reshape(output_height, output_width)

    return output_grid
```