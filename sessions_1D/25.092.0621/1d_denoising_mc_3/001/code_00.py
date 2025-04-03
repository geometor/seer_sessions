import numpy as np
from collections import Counter

"""
Transforms the input grid based on the following rules:
1. Identify the most frequent non-black (color value not 0) color in the input grid. Call this `dominant_color`.
2. Create an output grid of the same dimensions as the input.
3. Iterate through each pixel of the input grid:
    a. If the pixel's color is black (0) or if its color is the `dominant_color`, keep the pixel's color the same in the output grid.
    b. Otherwise (if the pixel's color is not black and not the `dominant_color`), change the pixel's color to the `dominant_color` in the output grid.
"""

def find_dominant_color(grid_np):
    """
    Finds the most frequent non-black color in a grid.

    Args:
        grid_np: A numpy array representing the grid.

    Returns:
        The integer value of the most frequent non-black color.
        Returns None if there are no non-black colors.
    """
    # Flatten the grid to easily count colors
    flat_grid = grid_np.flatten()

    # Filter out black pixels (color 0)
    non_black_pixels = [pixel for pixel in flat_grid if pixel != 0]

    # If there are no non-black pixels, return None or handle as appropriate
    if not non_black_pixels:
        return None

    # Count the frequency of each non-black color
    color_counts = Counter(non_black_pixels)

    # Find the color with the highest frequency
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input grid to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)

    # Find the dominant non-black color
    dominant_color = find_dominant_color(input_np)

    # If there's no dominant color (e.g., grid is all black), return the input as is
    if dominant_color is None:
        return input_grid # Or potentially an empty grid or specific handling

    # Create a copy of the input grid to modify for the output
    output_np = np.copy(input_np)

    # Get grid dimensions
    height, width = input_np.shape

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_np[r, c]
            # Apply the transformation rule:
            # If the color is not black (0) and not the dominant color,
            # change it to the dominant color in the output grid.
            if pixel_color != 0 and pixel_color != dominant_color:
                output_np[r, c] = dominant_color
            # Otherwise (pixel is black or is the dominant color), it remains unchanged
            # (already copied correctly in output_np)

    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_np.tolist()

    return output_grid
