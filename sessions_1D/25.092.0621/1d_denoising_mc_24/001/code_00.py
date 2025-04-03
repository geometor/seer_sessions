"""
1. Analyze the input grid (which is a single row) to determine the frequency of each color, ignoring any white (0) pixels.
2. Identify the color with the highest frequency among the non-white pixels. This is the "dominant color".
3. Create a new grid, initially identical to the input grid.
4. Iterate through each pixel of the input grid.
5. For each pixel, check its color:
    * If the pixel's color is white (0), keep it as white (0) in the new grid.
    * If the pixel's color is the same as the "dominant color", keep it as the "dominant color" in the new grid.
    * If the pixel's color is *neither* white (0) *nor* the "dominant color", change its color to the "dominant color" in the new grid.
6. The resulting new grid is the output.
"""

import numpy as np
from collections import Counter

def find_dominant_color(grid_row):
    """Finds the most frequent color in a list, excluding white (0)."""
    non_white_pixels = [pixel for pixel in grid_row if pixel != 0]
    if not non_white_pixels:
        # Handle cases with only white pixels or empty input
        return None # Or a default color, but based on examples, None seems appropriate
    
    count = Counter(non_white_pixels)
    # Find the color with the maximum count
    dominant_color = count.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid by identifying the dominant non-white color
    and replacing all other non-white pixels with that dominant color.
    """
    # Convert input list of lists to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)

    # Check if the grid is empty or invalid
    if input_array.size == 0:
        return input_grid # Return original if empty

    # As per the examples, the grid is always 1xN
    # Extract the single row
    grid_row = input_array[0]

    # Find the dominant color in the row, excluding white (0)
    dominant_color = find_dominant_color(grid_row)

    # If no dominant color found (e.g., all white), return the original grid
    if dominant_color is None:
         return input_grid

    # Initialize the output grid as a copy of the input grid
    output_array = input_array.copy()
    output_row = output_array[0] # Get reference to the row in the output

    # Iterate through each pixel in the row
    for i, pixel_color in enumerate(grid_row):
        # Check if the pixel is neither white (0) nor the dominant color
        if pixel_color != 0 and pixel_color != dominant_color:
            # Replace the pixel with the dominant color in the output
            output_row[i] = dominant_color

    # Convert the numpy array back to a list of lists for the expected output format
    return output_array.tolist()