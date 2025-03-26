"""
Identify the most frequent non-background color (0) in the input grid. If there's a tie in frequency, choose the color with the lowest numerical value. Create an output grid of the same dimensions. For each pixel in the input grid, if its color matches the most frequent color, copy that color to the output grid. Otherwise, set the corresponding pixel in the output grid to gray (5).
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Transforms the input grid based on color frequency.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    
    # Flatten the grid to count colors easily
    flat_grid = input_grid.flatten()

    # Filter out background color (0) and count frequencies of other colors
    non_background_colors = [color for color in flat_grid if color != 0]
    
    # Handle edge case: grid contains only background or is empty
    if not non_background_colors:
        # If only background, return a grid of the same size filled with gray (5), 
        # or maybe return the input as is? Based on examples, replacement seems intended.
        # Let's fill with gray as per the general rule observed.
        return np.full_like(input_grid, 5)
        
    color_counts = Counter(non_background_colors)

    # Find the maximum frequency
    if not color_counts: # Should be covered by the above check, but for safety
         return np.full_like(input_grid, 5)
         
    max_freq = max(color_counts.values())

    # Find all colors with the maximum frequency
    most_frequent_colors = [color for color, freq in color_counts.items() if freq == max_freq]

    # Determine the protected color (lowest numerical value in case of a tie)
    protected_color = min(most_frequent_colors)

    # Initialize the output grid with the target color (gray, 5)
    output_grid = np.full_like(input_grid, 5)

    # Iterate through the input grid and apply the transformation rule
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            # If the input pixel color is the protected color, keep it
            if input_grid[r, c] == protected_color:
                output_grid[r, c] = protected_color
            # Otherwise, it remains gray (5) as initialized

    return output_grid